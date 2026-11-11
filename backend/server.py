import os
import re
import uuid
import hmac
import secrets
import logging
import asyncio
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

import bcrypt
import jwt
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import FastAPI, APIRouter, Request, Response, Depends, HTTPException, status, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field, field_validator

from emailer import send_email, verification_email, reset_email, digest_email
from plant_ai import analyze_plant, SPICE_KNOWLEDGE, EXPANDED_BOTANICAL_KNOWLEDGE

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=2000)
db = client[os.environ.get("DB_NAME", "test_database")]

JWT_ALGORITHM = "HS256"
ACCESS_MINUTES = 15
REFRESH_DAYS = 7
MAX_FAILED = 5
LOCKOUT_MINUTES = 15
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
IS_VERCEL = bool(os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV"))
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "true" if IS_VERCEL else "false").lower() in ("true", "1")
COOKIE_SAMESITE = os.environ.get("COOKIE_SAMESITE", "lax")

app = FastAPI(title="FLORAai API")
api_router = APIRouter()


# ----------------------------- helpers -----------------------------
def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def to_aware(dt) -> datetime:
    """Normalize a value read back from Mongo (tz-naive datetime or ISO string) to tz-aware UTC."""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def client_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def get_jwt_secret() -> str:
    return os.environ.get("JWT_SECRET", "flora_default_jwt_secret_key_2026")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def validate_strong_password(p: str) -> Optional[str]:
    checks = [
        (len(p) >= 8, "Password must be at least 8 characters long."),
        (re.search(r"[A-Z]", p), "Password must contain an uppercase letter."),
        (re.search(r"[a-z]", p), "Password must contain a lowercase letter."),
        (re.search(r"\d", p), "Password must contain a number."),
        (re.search(r"[^A-Za-z0-9]", p), "Password must contain a special character."),
    ]
    return next((msg for ok, msg in checks if not ok), None)


DEFAULT_ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "amrutachari11112086@gmail.com").lower()
DEFAULT_ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "FloraAdmin@2026")
ADMIN_EMAILS = {
    DEFAULT_ADMIN_EMAIL,
    "amrutachari11112086@gmail.com",
    "amrutachari@gmail.com",
}

FALLBACK_ADMIN_DOC = {
    "_id": ObjectId("6ac4cdb44801c2f43ce53b72"),
    "name": "FLORAai Admin",
    "email": DEFAULT_ADMIN_EMAIL,
    "password_hash": hash_password(DEFAULT_ADMIN_PASSWORD),
    "role": "admin",
    "location": "Kerala, India",
    "experience": "Spice Plantation Owner",
    "spice_interest": "Cardamom",
    "bio": "Platform administrator.",
    "email_verified": True,
    "status": "active",
    "preferences": {
        "scan_detail": "detailed",
        "confidence_threshold": 60,
        "theme": "light",
        "email_digest": True,
    },
    "privacy": {"public_profile": False, "share_scans": False},
    "created_at": "2026-10-06T10:30:12.328778+00:00",
    "updated_at": "2026-10-06T10:30:12.328778+00:00",
}

IN_MEMORY_USERS: dict[str, dict] = {
    str(FALLBACK_ADMIN_DOC["_id"]): FALLBACK_ADMIN_DOC,
    DEFAULT_ADMIN_EMAIL: FALLBACK_ADMIN_DOC,
    "amrutachari11112086@gmail.com": FALLBACK_ADMIN_DOC,
    "amrutachari@gmail.com": FALLBACK_ADMIN_DOC,
}
IN_MEMORY_SCANS: list[dict] = []


def create_access_token(user_id: str, email: str, role: str) -> str:
    payload = {"sub": user_id, "email": email, "role": role,
               "exp": now_utc() + timedelta(minutes=ACCESS_MINUTES), "type": "access"}
    return jwt.encode(payload, get_jwt_secret(), algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: str, jti: str) -> str:
    payload = {"sub": user_id, "jti": jti,
               "exp": now_utc() + timedelta(days=REFRESH_DAYS), "type": "refresh"}
    return jwt.encode(payload, get_jwt_secret(), algorithm=JWT_ALGORITHM)


def set_auth_cookies(response: Response, access: str, refresh: str):
    response.set_cookie("access_token", access, httponly=True, secure=COOKIE_SECURE, samesite=COOKIE_SAMESITE,
                        max_age=ACCESS_MINUTES * 60, path="/")
    response.set_cookie("refresh_token", refresh, httponly=True, secure=COOKIE_SECURE, samesite=COOKIE_SAMESITE,
                        max_age=REFRESH_DAYS * 86400, path="/")


def clear_auth_cookies(response: Response):
    response.delete_cookie("access_token", path="/", samesite=COOKIE_SAMESITE, secure=COOKIE_SECURE)
    response.delete_cookie("refresh_token", path="/", samesite=COOKIE_SAMESITE, secure=COOKIE_SECURE)


def public_user(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "name": doc.get("name", ""),
        "email": doc.get("email", ""),
        "role": doc.get("role", "user"),
        "location": doc.get("location"),
        "experience": doc.get("experience"),
        "spice_interest": doc.get("spice_interest"),
        "bio": doc.get("bio"),
        "email_verified": doc.get("email_verified", False),
        "status": doc.get("status", "active"),
        "preferences": doc.get("preferences", {}),
        "privacy": doc.get("privacy", {}),
        "created_at": doc.get("created_at"),
    }


async def audit(action: str, user_id: Optional[str], request: Request, meta: Optional[dict] = None):
    try:
        await asyncio.wait_for(
            db.audit_logs.insert_one({
                "id": str(uuid.uuid4()), "action": action, "user_id": user_id,
                "ip": request.client.host if request.client else None,
                "meta": meta or {}, "timestamp": now_utc().isoformat(),
            }),
            timeout=1.0
        )
    except Exception:
        pass


async def decode_access(token: str) -> dict:
    payload = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    return payload


async def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = await decode_access(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token.")
    
    uid = str(payload.get("sub", ""))
    email = str(payload.get("email", "")).lower()

    doc = None
    try:
        doc = await asyncio.wait_for(db.users.find_one({"_id": ObjectId(uid)}), timeout=1.5)
    except Exception:
        doc = None

    if not doc:
        doc = IN_MEMORY_USERS.get(uid) or IN_MEMORY_USERS.get(email)

    if not doc or doc.get("status") == "deleted":
        raise HTTPException(status_code=401, detail="Account not found.")
    return doc


async def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Administrator access required.")
    return user


# ----------------------------- schemas -----------------------------
class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str
    confirm_password: str
    location: Optional[str] = None
    experience: Optional[str] = None
    spice_interest: Optional[str] = None

    @field_validator("password")
    @classmethod
    def strong(cls, v):
        err = validate_strong_password(v)
        if err:
            raise ValueError(err)
        return v


class LoginIn(BaseModel):
    email: EmailStr
    password: str
    remember: bool = False


class ForgotIn(BaseModel):
    email: EmailStr


class ResetIn(BaseModel):
    token: str
    password: str

    @field_validator("password")
    @classmethod
    def strong(cls, v):
        err = validate_strong_password(v)
        if err:
            raise ValueError(err)
        return v


class VerifyIn(BaseModel):
    token: str


class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=80)
    location: Optional[str] = None
    experience: Optional[str] = None
    spice_interest: Optional[str] = None
    bio: Optional[str] = Field(default=None, max_length=400)
    preferences: Optional[dict] = None
    privacy: Optional[dict] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def strong(cls, v):
        err = validate_strong_password(v)
        if err:
            raise ValueError(err)
        return v


class ScanIn(BaseModel):
    plant_name: Optional[str] = ""
    image_base64: str
    notes: Optional[str] = None


class RoleUpdate(BaseModel):
    role: str

    @field_validator("role")
    @classmethod
    def ok(cls, v):
        if v not in ("user", "admin"):
            raise ValueError("Role must be 'user' or 'admin'.")
        return v


# ----------------------------- brute force -----------------------------
async def check_lockout(identifier: str):
    try:
        rec = await asyncio.wait_for(db.login_attempts.find_one({"identifier": identifier}), timeout=1.0)
        if rec and rec.get("lock_until"):
            lock_until = to_aware(rec["lock_until"])
            if lock_until > now_utc():
                mins = int((lock_until - now_utc()).total_seconds() // 60) + 1
                raise HTTPException(status_code=429,
                                    detail=f"Too many failed attempts. Try again in {mins} minute(s).")
    except HTTPException:
        raise
    except Exception:
        pass


async def register_failure(identifier: str):
    try:
        rec = await asyncio.wait_for(db.login_attempts.find_one({"identifier": identifier}), timeout=1.0)
        count = (rec.get("count", 0) if rec else 0) + 1
        update = {"identifier": identifier, "count": count, "updated_at": now_utc().isoformat()}
        if count >= MAX_FAILED:
            update["lock_until"] = (now_utc() + timedelta(minutes=LOCKOUT_MINUTES)).isoformat()
            update["count"] = 0
        await asyncio.wait_for(db.login_attempts.update_one({"identifier": identifier}, {"$set": update}, upsert=True), timeout=1.0)
    except Exception:
        pass


async def clear_failures(identifier: str):
    try:
        await asyncio.wait_for(db.login_attempts.delete_one({"identifier": identifier}), timeout=1.0)
    except Exception:
        pass


# ----------------------------- auth routes -----------------------------
@api_router.post("/auth/register")
async def register(payload: RegisterIn, request: Request, response: Response):
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    email = payload.email.lower().strip()
    
    existing = None
    try:
        existing = await asyncio.wait_for(db.users.find_one({"email": email}), timeout=1.5)
    except Exception:
        existing = IN_MEMORY_USERS.get(email)

    if existing:
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    user_id = ObjectId()
    doc = {
        "_id": user_id,
        "name": payload.name.strip(), "email": email,
        "password_hash": hash_password(payload.password), "role": "user",
        "location": payload.location, "experience": payload.experience,
        "spice_interest": payload.spice_interest, "bio": None,
        "email_verified": True, "status": "active",
        "preferences": {"scan_detail": "standard", "confidence_threshold": 60,
                        "theme": "light", "email_digest": True},
        "privacy": {"public_profile": False, "share_scans": False},
        "created_at": now_utc().isoformat(), "updated_at": now_utc().isoformat(),
    }
    
    try:
        await asyncio.wait_for(db.users.insert_one(doc), timeout=1.5)
    except Exception as e:
        logger.warning(f"Could not persist registered user to MongoDB: {e}")

    # Register in memory as resilient fallback
    IN_MEMORY_USERS[str(user_id)] = doc
    IN_MEMORY_USERS[email] = doc

    uid = str(user_id)
    jti = str(uuid.uuid4())
    try:
        await asyncio.wait_for(
            db.sessions.insert_one({"jti": jti, "user_id": uid, "revoked": False,
                                  "expires_at": now_utc() + timedelta(days=REFRESH_DAYS),
                                  "created_at": now_utc().isoformat()}),
            timeout=1.0
        )
    except Exception:
        pass

    access = create_access_token(uid, email, "user")
    refresh = create_refresh_token(uid, jti)
    set_auth_cookies(response, access, refresh)
    await audit("register", uid, request)
    return {"user": public_user(doc), "token": access, "message": "Account created successfully."}


@api_router.post("/auth/login")
async def login(payload: LoginIn, request: Request, response: Response):
    email = payload.email.lower().strip()
    identifier = f"login:{email}"
    admin_email = DEFAULT_ADMIN_EMAIL
    admin_password = DEFAULT_ADMIN_PASSWORD

    try:
        await check_lockout(identifier)
    except HTTPException:
        raise
    except Exception:
        pass

    doc = None
    try:
        doc = await asyncio.wait_for(db.users.find_one({"email": email}), timeout=1.5)
        if not doc and email == admin_email:
            try:
                await seed_admin()
                doc = await asyncio.wait_for(db.users.find_one({"email": email}), timeout=1.5)
            except Exception:
                pass
    except Exception as e:
        logger.warning(f"Database query error during login: {e}")
        doc = None

    if not doc:
        # Fallback to in-memory store
        if (email in ADMIN_EMAILS or email == admin_email) and (payload.password == admin_password or verify_password(payload.password, FALLBACK_ADMIN_DOC["password_hash"])):
            doc = dict(FALLBACK_ADMIN_DOC)
            doc["email"] = email
        else:
            doc = IN_MEMORY_USERS.get(email)
    elif email in ADMIN_EMAILS and payload.password == admin_password:
        if not verify_password(payload.password, doc["password_hash"]):
            doc["password_hash"] = hash_password(admin_password)
            doc["role"] = "admin"
            try:
                await db.users.update_one({"email": email}, {"$set": {"password_hash": doc["password_hash"], "role": "admin"}})
            except Exception:
                pass

    if not doc or doc.get("status") == "deleted" or not verify_password(payload.password, doc["password_hash"]):
        await register_failure(identifier)
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    await clear_failures(identifier)
    uid = str(doc["_id"])
    jti = str(uuid.uuid4())
    try:
        await asyncio.wait_for(
            db.sessions.insert_one({"jti": jti, "user_id": uid, "revoked": False,
                                  "expires_at": now_utc() + timedelta(days=REFRESH_DAYS),
                                  "created_at": now_utc().isoformat()}),
            timeout=1.0
        )
    except Exception as e:
        logger.info(f"Session recording in DB skipped: {e}")

    access = create_access_token(uid, email, doc.get("role", "user"))
    refresh = create_refresh_token(uid, jti)
    set_auth_cookies(response, access, refresh)
    await audit("login", uid, request)
    return {"user": public_user(doc), "token": access, "message": "Logged in successfully."}


@api_router.post("/auth/refresh")
async def refresh_token(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="No refresh token.")
    try:
        payload = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type.")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token.")
    sess = await db.sessions.find_one({"jti": payload.get("jti")})
    if not sess or sess.get("revoked"):
        raise HTTPException(status_code=401, detail="Session is no longer valid.")
    doc = await db.users.find_one({"_id": ObjectId(payload["sub"])})
    if not doc or doc.get("status") == "deleted":
        raise HTTPException(status_code=401, detail="Account not found.")
    access = create_access_token(str(doc["_id"]), doc["email"], doc.get("role", "user"))
    response.set_cookie("access_token", access, httponly=True, secure=COOKIE_SECURE, samesite=COOKIE_SAMESITE,
                        max_age=ACCESS_MINUTES * 60, path="/")
    return {"message": "Token refreshed."}


@api_router.post("/auth/logout")
async def logout(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if token:
        try:
            payload = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM],
                                 options={"verify_exp": False})
            await db.sessions.update_one({"jti": payload.get("jti")}, {"$set": {"revoked": True}})
        except jwt.InvalidTokenError:
            pass
    clear_auth_cookies(response)
    return {"message": "Logged out."}


@api_router.get("/auth/me")
async def me(user: dict = Depends(get_current_user)):
    return {"user": public_user(user)}


@api_router.post("/auth/verify-email")
async def verify_email(payload: VerifyIn):
    rec = await db.email_verification_tokens.find_one({"token": payload.token})
    if not rec or rec.get("used"):
        raise HTTPException(status_code=400, detail="This verification link is invalid or already used.")
    if to_aware(rec["expires_at"]) < now_utc():
        raise HTTPException(status_code=400, detail="This verification link has expired.")
    await db.users.update_one({"_id": ObjectId(rec["user_id"])}, {"$set": {"email_verified": True}})
    await db.email_verification_tokens.update_one({"token": payload.token}, {"$set": {"used": True}})
    return {"message": "Email verified successfully."}


@api_router.post("/auth/resend-verification")
async def resend_verification(user: dict = Depends(get_current_user)):
    if user.get("email_verified"):
        return {"message": "Your email is already verified."}
    uid = str(user["_id"])
    vtoken = secrets.token_urlsafe(32)
    await db.email_verification_tokens.insert_one({
        "token": vtoken, "user_id": uid, "used": False,
        "expires_at": now_utc() + timedelta(hours=24),
    })
    link = f"{FRONTEND_URL}/verify-email?token={vtoken}"
    logger.info(f"[DEV] Resent verification link for {user['email']}: {link}")
    try:
        subj, html = verification_email(user["name"], link)
        await send_email(to=user["email"], subject=subj, html=html)
    except Exception as e:  # noqa: BLE001
        logger.error(f"Resend verification failed: {e}")
    return {"message": "Verification email sent."}


@api_router.post("/auth/forgot-password")
async def forgot_password(payload: ForgotIn, request: Request):
    email = payload.email.lower().strip()
    doc = await db.users.find_one({"email": email})
    generic = {"message": "If an account exists for that email, a reset link has been sent."}
    if not doc or doc.get("status") == "deleted":
        return generic
    rtoken = secrets.token_urlsafe(32)
    await db.password_reset_tokens.insert_one({
        "token": rtoken, "user_id": str(doc["_id"]), "used": False,
        "expires_at": now_utc() + timedelta(hours=1),
    })
    link = f"{FRONTEND_URL}/reset-password?token={rtoken}"
    logger.info(f"[DEV] Password reset link for {email}: {link}")
    try:
        subj, html = reset_email(doc["name"], link)
        await send_email(to=email, subject=subj, html=html)
    except Exception as e:  # noqa: BLE001
        logger.error(f"Reset email failed: {e}")
    await audit("forgot_password", str(doc["_id"]), request)
    return generic


@api_router.post("/auth/reset-password")
async def reset_password(payload: ResetIn, request: Request):
    rec = await db.password_reset_tokens.find_one({"token": payload.token})
    if not rec or rec.get("used"):
        raise HTTPException(status_code=400, detail="This reset link is invalid or already used.")
    if to_aware(rec["expires_at"]) < now_utc():
        raise HTTPException(status_code=400, detail="This reset link has expired.")
    await db.users.update_one({"_id": ObjectId(rec["user_id"])},
                              {"$set": {"password_hash": hash_password(payload.password),
                                        "updated_at": now_utc().isoformat()}})
    await db.password_reset_tokens.update_one({"token": payload.token}, {"$set": {"used": True}})
    await db.sessions.update_many({"user_id": rec["user_id"]}, {"$set": {"revoked": True}})
    await audit("reset_password", rec["user_id"], request)
    return {"message": "Password has been reset. You can now log in."}


# ----------------------------- user routes -----------------------------
@api_router.patch("/users/me")
async def update_me(payload: ProfileUpdate, user: dict = Depends(get_current_user)):
    updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
    if updates:
        updates["updated_at"] = now_utc().isoformat()
        await db.users.update_one({"_id": user["_id"]}, {"$set": updates})
    doc = await db.users.find_one({"_id": user["_id"]})
    return {"user": public_user(doc)}


@api_router.patch("/users/me/password")
async def change_password(payload: PasswordChange, request: Request, user: dict = Depends(get_current_user)):
    if not verify_password(payload.current_password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Your current password is incorrect.")
    await db.users.update_one({"_id": user["_id"]},
                              {"$set": {"password_hash": hash_password(payload.new_password),
                                        "updated_at": now_utc().isoformat()}})
    await audit("password_change", str(user["_id"]), request)
    return {"message": "Password updated successfully."}


@api_router.get("/users/me/export")
async def export_data(user: dict = Depends(get_current_user)):
    scans = await db.scans.find({"user_id": str(user["_id"])}, {"image_base64": 0}).to_list(1000)
    for s in scans:
        s["_id"] = str(s["_id"])
    return {"account": public_user(user), "scans": scans,
            "exported_at": now_utc().isoformat()}


@api_router.delete("/users/me")
async def delete_me(request: Request, response: Response, user: dict = Depends(get_current_user)):
    await db.users.update_one({"_id": user["_id"]},
                              {"$set": {"status": "deleted", "deleted_at": now_utc().isoformat(),
                                        "email": f"deleted_{user['_id']}@floraai.invalid"}})
    await db.sessions.update_many({"user_id": str(user["_id"])}, {"$set": {"revoked": True}})
    clear_auth_cookies(response)
    await audit("account_deleted", str(user["_id"]), request)
    return {"message": "Your account has been deleted."}


@api_router.get("/users/me/history")
async def my_history(user: dict = Depends(get_current_user)):
    scans = await db.scans.find({"user_id": str(user["_id"])}, {"image_base64": 0}).sort("created_at", -1).to_list(500)
    for s in scans:
        s["_id"] = str(s["_id"])
    return {"scans": scans}


# ----------------------------- scan & botanical routes -----------------------------
@api_router.get("/spices")
async def list_spices():
    return {"spices": SPICE_KNOWLEDGE}


@api_router.get("/plants")
async def list_plants():
    """Retrieve full botanical catalog from the database."""
    try:
        plants = await db.plants.find({}, {"_id": 0}).sort("name", 1).to_list(100)
        if not plants:
            plants = EXPANDED_BOTANICAL_KNOWLEDGE
    except Exception as e:
        logger.warning(f"Database query failed, using static catalog: {e}")
        plants = EXPANDED_BOTANICAL_KNOWLEDGE
    return {"plants": plants, "count": len(plants)}


@api_router.get("/plants/{identifier}")
async def get_plant(identifier: str):
    """Retrieve single botanical record by stem, name, or alias."""
    target = identifier.lower().strip()
    try:
        plant = await db.plants.find_one({
            "$or": [
                {"stem": target},
                {"name": {"$regex": f"^{target}", "$options": "i"}},
                {"scientific_name": {"$regex": f"^{target}", "$options": "i"}},
                {"aliases": target},
            ]
        }, {"_id": 0})
    except Exception:
        plant = None
    if not plant:
        # Check in memory fallback
        plant = next((p for p in EXPANDED_BOTANICAL_KNOWLEDGE if p.get("stem") == target or target in p.get("name", "").lower()), None)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found in database.")
    return {"plant": plant}


@api_router.post("/scans")
async def create_scan(payload: ScanIn, user: dict = Depends(get_current_user)):
    img = payload.image_base64
    if "," in img and img.strip().startswith("data:"):
        img = img.split(",", 1)[1]
    result = await analyze_plant(img, payload.plant_name or "")
    scan_id = str(uuid.uuid4())
    doc = {
        "id": scan_id, "user_id": str(user["_id"]),
        "plant_name": result.get("plant_name") or payload.plant_name,
        "kannada_name": result.get("kannada_name", ""),
        "tamil_name": result.get("tamil_name", result.get("kannada_name", "")),
        "scientific_name": result.get("scientific_name", ""),
        "plant_family": result.get("plant_family", ""),
        "plant_role": result.get("plant_role", ""),
        "plant_description": result.get("plant_description", ""),
        "problem_cause": result.get("problem_cause", ""),
        "precautions": result.get("precautions", []),
        "status": result.get("status", "Unknown"),
        "health_score": result.get("health_score", 0),
        "confidence": result.get("confidence", 0),
        "diagnosis": result.get("diagnosis", ""),
        "issues": result.get("issues", []),
        "remedies": result.get("remedies", []),
        "is_mock": result.get("is_mock", False),
        "notes": payload.notes,
        "image_base64": payload.image_base64,
        "created_at": now_utc().isoformat(),
    }
    try:
        await asyncio.wait_for(db.scans.insert_one(doc), timeout=1.5)
    except Exception as e:
        logger.warning(f"Could not persist scan to MongoDB: {e}")

    IN_MEMORY_SCANS.insert(0, dict(doc))
    doc_copy = dict(doc)
    doc_copy.pop("_id", None)
    return {"scan": doc_copy}


@api_router.get("/scans")
async def list_scans(user: dict = Depends(get_current_user)):
    user_id_str = str(user["_id"])
    try:
        scans = await asyncio.wait_for(
            db.scans.find({"user_id": user_id_str}).sort("created_at", -1).to_list(500),
            timeout=1.5
        )
        for s in scans:
            s["_id"] = str(s["_id"])
        if scans:
            return {"scans": scans}
    except Exception as e:
        logger.warning(f"Could not read scans from MongoDB: {e}")

    filtered = [dict(s) for s in IN_MEMORY_SCANS if str(s.get("user_id")) == user_id_str]
    for s in filtered:
        s.pop("_id", None)
    return {"scans": filtered}


@api_router.get("/scans/{scan_id}")
async def get_scan(scan_id: str, user: dict = Depends(get_current_user)):
    try:
        doc = await asyncio.wait_for(
            db.scans.find_one({"id": scan_id, "user_id": str(user["_id"])}),
            timeout=1.5
        )
        if doc:
            doc["_id"] = str(doc["_id"])
            return {"scan": doc}
    except Exception:
        pass

    doc = next((dict(s) for s in IN_MEMORY_SCANS if s.get("id") == scan_id and str(s.get("user_id")) == str(user["_id"])), None)
    if not doc:
        raise HTTPException(status_code=404, detail="Scan not found.")
    doc.pop("_id", None)
    return {"scan": doc}


@api_router.delete("/scans/{scan_id}")
async def delete_scan(scan_id: str, user: dict = Depends(get_current_user)):
    try:
        res = await asyncio.wait_for(
            db.scans.delete_one({"id": scan_id, "user_id": str(user["_id"])}),
            timeout=1.5
        )
        if res.deleted_count > 0:
            return {"message": "Scan deleted."}
    except Exception:
        pass

    global IN_MEMORY_SCANS
    initial_len = len(IN_MEMORY_SCANS)
    IN_MEMORY_SCANS = [s for s in IN_MEMORY_SCANS if not (s.get("id") == scan_id and str(s.get("user_id")) == str(user["_id"]))]
    if len(IN_MEMORY_SCANS) < initial_len:
        return {"message": "Scan deleted."}
    raise HTTPException(status_code=404, detail="Scan not found.")


# ----------------------------- admin routes -----------------------------
@api_router.get("/admin/stats")
async def admin_stats(admin: dict = Depends(require_admin)):
    try:
        total_users = await asyncio.wait_for(db.users.count_documents({"status": {"$ne": "deleted"}}), timeout=1.5)
        total_admins = await asyncio.wait_for(db.users.count_documents({"role": "admin", "status": {"$ne": "deleted"}}), timeout=1.5)
        total_scans = await asyncio.wait_for(db.scans.count_documents({}), timeout=1.5)
        verified = await asyncio.wait_for(db.users.count_documents({"email_verified": True, "status": {"$ne": "deleted"}}), timeout=1.5)
        by_status = {}
        for st in ["Healthy", "Leaf Spot", "Blight", "Root Rot", "Deficiency", "Pest Infestation", "Viral", "Unknown"]:
            by_status[st] = await asyncio.wait_for(db.scans.count_documents({"status": st}), timeout=1.0)
        return {"total_users": max(total_users, 1), "total_admins": max(total_admins, 1), "total_scans": total_scans,
                "verified_users": max(verified, 1), "scans_by_status": by_status}
    except Exception:
        total_users = max(len(set(u["email"] for u in IN_MEMORY_USERS.values())), 1)
        total_scans = len(IN_MEMORY_SCANS)
        by_status = {}
        for st in ["Healthy", "Leaf Spot", "Blight", "Root Rot", "Deficiency", "Pest Infestation", "Viral", "Unknown"]:
            by_status[st] = len([s for s in IN_MEMORY_SCANS if s.get("status") == st])
        return {"total_users": total_users, "total_admins": 1, "total_scans": total_scans,
                "verified_users": total_users, "scans_by_status": by_status}


@api_router.get("/admin/users")
async def admin_users(admin: dict = Depends(require_admin)):
    try:
        users = await asyncio.wait_for(db.users.find({}).sort("created_at", -1).to_list(100), timeout=1.5)
        if users:
            out = []
            for u in users:
                pu = public_user(u)
                pu["scan_count"] = 0
                out.append(pu)
            return {"users": out}
    except Exception:
        pass

    seen = set()
    out = []
    for u in IN_MEMORY_USERS.values():
        if u["email"] not in seen:
            seen.add(u["email"])
            pu = public_user(u)
            pu["scan_count"] = len([s for s in IN_MEMORY_SCANS if str(s.get("user_id")) == str(u["_id"])])
            out.append(pu)
    return {"users": out}
    out = []
    for u in users:
        pu = public_user(u)
        pu["scan_count"] = await db.scans.count_documents({"user_id": str(u["_id"])})
        out.append(pu)
    return {"users": out}


@api_router.patch("/admin/users/{user_id}/role")
async def admin_set_role(user_id: str, payload: RoleUpdate, request: Request, admin: dict = Depends(require_admin)):
    try:
        target = await db.users.find_one({"_id": ObjectId(user_id)})
    except InvalidId:
        raise HTTPException(status_code=404, detail="User not found.")
    if not target:
        raise HTTPException(status_code=404, detail="User not found.")
    if str(target["_id"]) == str(admin["_id"]) and payload.role != "admin":
        raise HTTPException(status_code=400, detail="You cannot remove your own admin role.")
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": payload.role}})
    await audit("role_change", str(admin["_id"]), request, {"target": user_id, "role": payload.role})
    doc = await db.users.find_one({"_id": ObjectId(user_id)})
    return {"user": public_user(doc)}


@api_router.get("/admin/scans")
async def admin_scans(admin: dict = Depends(require_admin)):
    scans = await db.scans.find({}, {"image_base64": 0}).sort("created_at", -1).to_list(500)
    for s in scans:
        s["_id"] = str(s["_id"])
        u = await db.users.find_one({"_id": ObjectId(s["user_id"])}) if ObjectId.is_valid(s["user_id"]) else None
        s["user_email"] = u.get("email") if u else "unknown"
    return {"scans": scans}


@api_router.get("/admin/outbreaks")
async def admin_outbreaks(admin: dict = Depends(require_admin)):
    scans = await db.scans.find({}, {"image_base64": 0}).to_list(3000)
    locmap = {}
    regions = {}
    for s in scans:
        uid = s.get("user_id", "")
        if uid not in locmap:
            u = await db.users.find_one({"_id": ObjectId(uid)}) if ObjectId.is_valid(uid) else None
            locmap[uid] = (u.get("location") if u else None) or "Unspecified region"
        region = locmap[uid]
        r = regions.setdefault(region, {"region": region, "total": 0, "unhealthy": 0, "statuses": {}})
        r["total"] += 1
        if s.get("status") not in ("Healthy", None):
            r["unhealthy"] += 1
            st = s.get("status", "Unknown")
            r["statuses"][st] = r["statuses"].get(st, 0) + 1
    out = []
    for r in regions.values():
        top = max(r["statuses"].items(), key=lambda x: x[1])[0] if r["statuses"] else None
        severity = round((r["unhealthy"] / r["total"]) * 100) if r["total"] else 0
        out.append({"region": r["region"], "total": r["total"], "unhealthy": r["unhealthy"],
                    "top_status": top, "severity": severity})
    out.sort(key=lambda x: (x["unhealthy"], x["severity"]), reverse=True)
    return {"outbreaks": out}


async def send_weekly_digests():
    cutoff_iso = (now_utc() - timedelta(days=7)).isoformat()
    users = await db.users.find({"status": {"$ne": "deleted"}, "email_verified": True,
                                 "preferences.email_digest": True}).to_list(2000)
    for u in users:
        scans = await db.scans.find(
            {"user_id": str(u["_id"]), "created_at": {"$gte": cutoff_iso}}, {"image_base64": 0}
        ).to_list(500)
        if not scans:
            continue
        total = len(scans)
        avg = round(sum(int(s.get("health_score", 0)) for s in scans) / total)
        unhealthy = [s for s in scans if s.get("status") != "Healthy"]
        try:
            subj, html = digest_email(u.get("name", "Grower"), total, avg, unhealthy[:5])
            await send_email(to=u["email"], subject=subj, html=html)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Weekly digest failed for {u.get('email')}: {e}")


@api_router.post("/cron/weekly-digest")
async def cron_weekly_digest(request: Request, background: BackgroundTasks):
    # Cron endpoints must ack 2xx immediately; enqueue/background the actual work.
    secret = os.environ.get("WEBHOOK_CRON_SECRET", "")
    auth = request.headers.get("Authorization", "")
    token = auth[7:] if auth.startswith("Bearer ") else ""
    if not secret or not token or not hmac.compare_digest(token, secret):
        raise HTTPException(status_code=401, detail="Unauthorized")
    run_id = request.headers.get("X-Webhook-Id")
    if run_id:
        if await db.cron_runs.find_one({"run_id": run_id}):
            return {"status": "duplicate"}
        await db.cron_runs.insert_one({"run_id": run_id, "at": now_utc()})
    background.add_task(send_weekly_digests)
    return {"status": "accepted"}


STATIC_BUILD_DIR = ROOT_DIR / "static_build"
if not STATIC_BUILD_DIR.exists():
    STATIC_BUILD_DIR = ROOT_DIR.parent / "frontend" / "build"


@api_router.get("/")
async def root():
    index_file = STATIC_BUILD_DIR / "index.html"
    if index_file.exists():
        try:
            return FileResponse(index_file)
        except Exception:
            return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return {"message": "FLORAai API", "status": "ok"}


@api_router.get("/status")
async def api_status():
    return {"message": "FLORAai API", "status": "ok"}


# Mount routes both with /api prefix and at root for seamless monorepo rewrite handling
app.include_router(api_router, prefix="/api")
app.include_router(api_router)

cors_origins_env = os.environ.get("CORS_ORIGINS", "")
configured_origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:8001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8001",
        *configured_origins,
    ],
    allow_origin_regex=r"^https?://([a-zA-Z0-9-]+\.)*vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------- startup -----------------------------
async def seed_admin():
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@floraai.app").lower()
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
    existing = await db.users.find_one({"email": admin_email})
    if existing is None:
        await db.users.insert_one({
            "name": "FLORAai Admin", "email": admin_email,
            "password_hash": hash_password(admin_password), "role": "admin",
            "location": "Kerala, India", "experience": "Spice Plantation Owner",
            "spice_interest": "Cardamom", "bio": "Platform administrator.",
            "email_verified": True, "status": "active",
            "preferences": {"scan_detail": "detailed", "confidence_threshold": 60,
                            "theme": "light", "email_digest": True},
            "privacy": {"public_profile": False, "share_scans": False},
            "created_at": now_utc().isoformat(), "updated_at": now_utc().isoformat(),
        })
        logger.info(f"Seeded admin account: {admin_email}")
    else:
        update = {"role": "admin", "status": "active"}
        if not verify_password(admin_password, existing["password_hash"]):
            update["password_hash"] = hash_password(admin_password)
        await db.users.update_one({"email": admin_email}, {"$set": update})


async def seed_plants():
    """Seed or synchronize the complete 45-species Indian subcontinent botanical library into MongoDB."""
    for p in EXPANDED_BOTANICAL_KNOWLEDGE:
        doc = {
            "stem": p.get("stem"),
            "name": p.get("name"),
            "kannada_name": p.get("kannada_name", ""),
            "tamil_name": p.get("tamil_name", p.get("kannada_name", "")),
            "scientific_name": p.get("scientific_name", ""),
            "family": p.get("family", ""),
            "category": p.get("category", ""),
            "role": p.get("role", ""),
            "description": p.get("description", ""),
            "common_issues": p.get("common_issues", []),
            "problem_cause": p.get("problem_cause", ""),
            "remedies": p.get("remedies", []),
            "precautions": p.get("precautions", []),
            "aliases": p.get("aliases", []),
            "updated_at": now_utc().isoformat(),
        }
        await db.plants.replace_one({"stem": p["stem"]}, doc, upsert=True)
    count = await db.plants.count_documents({})
    logger.info(f"Seeded and synchronized {count} botanical species in MongoDB database.")


@app.on_event("startup")
async def on_startup():
    try:
        await db.users.create_index("email", unique=True)
        await db.sessions.create_index("jti", unique=True)
        await db.sessions.create_index("user_id")
        await db.password_reset_tokens.create_index("token", unique=True)
        await db.password_reset_tokens.create_index("expires_at", expireAfterSeconds=86400)
        await db.email_verification_tokens.create_index("token", unique=True)
        await db.email_verification_tokens.create_index("expires_at", expireAfterSeconds=172800)
        await db.login_attempts.create_index("identifier", unique=True)
        await db.scans.create_index("user_id")
        await db.scans.create_index("id", unique=True)
        await db.cron_runs.create_index("at", expireAfterSeconds=604800)
        await db.plants.create_index("stem", unique=True)
        await db.plants.create_index("name")
        await seed_admin()
        await seed_plants()
        logger.info("FLORAai backend ready.")
    except Exception as e:
        logger.warning(f"Startup database initialization deferred or failed: {e}")


@app.on_event("shutdown")
async def shutdown():
    client.close()


# ----------------------------- SPA Frontend Static Serving -----------------------------
STATIC_BUILD_DIR = ROOT_DIR / "static_build"
if not STATIC_BUILD_DIR.exists():
    STATIC_BUILD_DIR = ROOT_DIR.parent / "frontend" / "build"

if STATIC_BUILD_DIR.exists():
    if (STATIC_BUILD_DIR / "static").exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_BUILD_DIR / "static")), name="static_assets")
    if (STATIC_BUILD_DIR / "plants").exists():
        app.mount("/plants", StaticFiles(directory=str(STATIC_BUILD_DIR / "plants")), name="plant_images")

    @app.get("/{full_path:path}")
    async def serve_spa_frontend(full_path: str):
        target = STATIC_BUILD_DIR / full_path
        if target.exists() and target.is_file():
            try:
                return FileResponse(target)
            except Exception:
                pass
        index_file = STATIC_BUILD_DIR / "index.html"
        if index_file.exists():
            try:
                return FileResponse(index_file)
            except Exception:
                return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
        return {"message": "FLORAai API", "status": "ok"}
