"""
Comprehensive Multi-Condition Dataset Generator & Neural Model Training Pipeline
Trains MobileNetV3 dual-head model on all 45 botanical species in both healthy and diseased states.
"""
from __future__ import annotations
import os
import sys
import random
import json
import logging
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import torchvision.models as models
from torchvision import transforms

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("train_plant_ai")

ROOT_DIR = Path(__file__).parent
DATASET_DIR = ROOT_DIR / "dataset"
MODELS_DIR = ROOT_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)
DATASET_DIR.mkdir(exist_ok=True)

# Add backend to path for plant_ai imports
sys.path.insert(0, str(ROOT_DIR))
from plant_ai import EXPANDED_BOTANICAL_KNOWLEDGE

CONDITIONS = [
    "Healthy",
    "Leaf Spot",
    "Blight",
    "Deficiency",
    "Pest Infestation",
    "Powdery Mildew",
]
CONDITION_TO_IDX = {c: i for i, c in enumerate(CONDITIONS)}
STEMS = [p["stem"] for p in EXPANDED_BOTANICAL_KNOWLEDGE]
STEM_TO_IDX = {s: i for i, s in enumerate(STEMS)}


def get_leaf_mask(im_pil: Image.Image, stem: str) -> np.ndarray:
    """Extract segmented living foliage mask from image."""
    arr = np.asarray(im_pil, dtype=np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    mask = (g > 35) & (g > r * 0.78) & (g > b * 0.78)
    if stem == "bismarck_palm":
        mask |= (r > 100) & (g > 110) & (b > 110) & (abs(r - g) < 25) & (abs(g - b) < 25)
    elif stem == "lipstick_palm":
        mask |= (r > 110) & (r > g * 1.5) & (b < 120)
    elif stem == "coleus":
        mask |= (r > 90) & (b > 60) & (r > g * 1.1)
    elif stem == "coconut":
        mask |= (r > 70) & (g > 70) & (b < 120) & (g > b * 1.1)
    elif stem == "rose" or stem == "hibiscus":
        mask |= (r > 110) & (r > g * 1.5)
    return mask


def synthesize_leaf_spots(im_pil: Image.Image, mask: np.ndarray, num_spots: int = 15, severity: str = "moderate") -> Image.Image:
    """Render realistic circular/elliptical necrotic fungal leaf spots with yellow chlorotic halos."""
    res = im_pil.copy()
    draw = ImageDraw.Draw(res, "RGBA")
    w, h = im_pil.size
    ys, xs = np.where(mask)
    if len(xs) < 50:
        return res

    spot_indices = np.random.choice(len(xs), size=min(num_spots, len(xs)), replace=False)
    for idx in spot_indices:
        cx, cy = int(xs[idx]), int(ys[idx])
        base_r = random.randint(3, 7) if severity == "mild" else random.randint(5, 14)
        
        # Yellow chlorotic halo (halo ring around the necrotic lesion)
        halo_r = base_r + random.randint(3, 6)
        halo_color = (random.randint(190, 220), random.randint(180, 205), random.randint(40, 80), 180)
        draw.ellipse([cx - halo_r, cy - halo_r, cx + halo_r, cy + halo_r], fill=halo_color)
        
        # Outer necrotic margin (dark brown ring)
        margin_color = (random.randint(60, 90), random.randint(40, 60), random.randint(20, 35), 230)
        draw.ellipse([cx - base_r, cy - base_r, cx + base_r, cy + base_r], fill=margin_color)
        
        # Inner necrotic dead center (pale tan or dark ash brown with concentric ring)
        core_r = max(1, base_r - 2)
        core_color = (random.randint(40, 65), random.randint(25, 45), random.randint(15, 30), 245)
        draw.ellipse([cx - core_r, cy - core_r, cx + core_r, cy + core_r], fill=core_color)

    # Slight blur to merge naturally into the cellular leaf grain
    res = Image.blend(res, res.filter(ImageFilter.SMOOTH_MORE), 0.25)
    return res


def synthesize_blight(im_pil: Image.Image, mask: np.ndarray, severity: float = 0.18) -> Image.Image:
    """Render spreading necrotic blight decay, foliar dieback, and water-soaked rot along leaf blades."""
    arr = np.asarray(im_pil, dtype=np.float32).copy()
    h, w, _ = arr.shape
    
    # Create irregular blight centers
    ys, xs = np.where(mask)
    if len(xs) < 100:
        return im_pil

    centers = np.random.choice(len(xs), size=random.randint(3, 6), replace=False)
    blight_map = np.zeros((h, w), dtype=np.float32)
    
    for c_idx in centers:
        cx, cy = xs[c_idx], ys[c_idx]
        sigma_x = random.randint(18, 45)
        sigma_y = random.randint(18, 45)
        y_grid, x_grid = np.ogrid[:h, :w]
        dist = ((x_grid - cx) ** 2 / (2 * sigma_x ** 2)) + ((y_grid - cy) ** 2 / (2 * sigma_y ** 2))
        blight_map += np.exp(-dist)

    blight_map = np.clip(blight_map, 0.0, 1.0)
    blight_affected = (blight_map > 0.35) & mask
    
    # Apply necrotic browning and cellular decay (dark scorched brown with water-soaked edges)
    decay_r = np.random.uniform(55, 85, size=(h, w))
    decay_g = np.random.uniform(40, 65, size=(h, w))
    decay_b = np.random.uniform(25, 45, size=(h, w))
    
    alpha = np.clip((blight_map - 0.35) / 0.65, 0.0, 1.0)
    for c in range(3):
        decay_c = decay_r if c == 0 else (decay_g if c == 1 else decay_b)
        arr[:, :, c] = np.where(blight_affected, arr[:, :, c] * (1 - alpha) + decay_c * alpha, arr[:, :, c])

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def synthesize_chlorosis(im_pil: Image.Image, mask: np.ndarray, intensity: float = 0.75) -> Image.Image:
    """Render interveinal chlorophyll depletion, fading green leaf lamina into golden-yellow."""
    arr = np.asarray(im_pil, dtype=np.float32).copy()
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    # Elevate red and reduce green chlorophyll saturation in the interveinal tissue
    yellow_r = np.clip(r * 1.55 + 35, 0, 240)
    yellow_g = np.clip(g * 1.15 + 20, 0, 245)
    yellow_b = np.clip(b * 0.65 - 10, 0, 120)

    for c, target in enumerate([yellow_r, yellow_g, yellow_b]):
        arr[:, :, c] = np.where(mask, arr[:, :, c] * (1 - intensity) + target * intensity, arr[:, :, c])

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def synthesize_pest_damage(im_pil: Image.Image, mask: np.ndarray) -> Image.Image:
    """Render insect stippling, mite puncture marks, and sooty mold speckling."""
    arr = np.asarray(im_pil, dtype=np.float32).copy()
    h, w, _ = arr.shape
    ys, xs = np.where(mask)
    if len(xs) < 100:
        return im_pil

    # Hundreds of fine stippling dots (pale bleached punctures from spider mites)
    stipple_idx = np.random.choice(len(xs), size=min(400, len(xs)), replace=False)
    for idx in stipple_idx:
        py, px = ys[idx], xs[idx]
        arr[py, px, :] = [210, 215, 160]

    # Black sooty mold speckles
    sooty_idx = np.random.choice(len(xs), size=min(120, len(xs)), replace=False)
    for idx in sooty_idx:
        py, px = ys[idx], xs[idx]
        arr[py, px, :] = [25, 25, 20]

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def synthesize_powdery_mildew(im_pil: Image.Image, mask: np.ndarray) -> Image.Image:
    """Render whitish-gray powdery fungal mycelium dusted over leaf surfaces."""
    arr = np.asarray(im_pil, dtype=np.float32).copy()
    h, w, _ = arr.shape
    ys, xs = np.where(mask)
    if len(xs) < 100:
        return im_pil

    centers = np.random.choice(len(xs), size=random.randint(4, 7), replace=False)
    mildew_map = np.zeros((h, w), dtype=np.float32)
    for c_idx in centers:
        cx, cy = xs[c_idx], ys[c_idx]
        sigma = random.randint(15, 30)
        y_grid, x_grid = np.ogrid[:h, :w]
        dist = ((x_grid - cx) ** 2 + (y_grid - cy) ** 2) / (2 * sigma ** 2)
        mildew_map += np.exp(-dist)

    mildew_map = np.clip(mildew_map, 0.0, 1.0)
    mildew_mask = (mildew_map > 0.3) & mask
    alpha = np.clip(mildew_map * 0.75, 0.0, 0.75)

    powder_color = 225.0
    for c in range(3):
        arr[:, :, c] = np.where(mildew_mask, arr[:, :, c] * (1 - alpha) + powder_color * alpha, arr[:, :, c])

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def generate_dataset() -> list[dict]:
    """Generate multi-condition dataset for all 45 botanical species with metadata."""
    manifest = []
    logger.info("Generating multi-condition dataset for 45 botanical species...")

    for plant_idx, plant in enumerate(EXPANDED_BOTANICAL_KNOWLEDGE):
        stem = plant["stem"]
        src_path = ROOT_DIR.parent / "frontend" / "public" / "plants" / f"{stem}.jpg"
        if not src_path.exists():
            logger.warning(f"Image not found: {src_path}")
            continue

        base_im = Image.open(src_path).convert("RGB").resize((256, 256))
        mask = get_leaf_mask(base_im, stem)

        # 1. Healthy variants
        # 1a. Standard
        h_std_path = DATASET_DIR / f"{stem}_healthy_std.jpg"
        base_im.save(h_std_path, quality=92)
        manifest.append({"path": str(h_std_path), "stem": stem, "condition": "Healthy"})

        # 1b. Sunlight
        h_sun = ImageEnhance.Brightness(base_im).enhance(1.15)
        h_sun = ImageEnhance.Contrast(h_sun).enhance(1.08)
        h_sun_path = DATASET_DIR / f"{stem}_healthy_sun.jpg"
        h_sun.save(h_sun_path, quality=92)
        manifest.append({"path": str(h_sun_path), "stem": stem, "condition": "Healthy"})

        # 1c. Shade
        h_shade = ImageEnhance.Brightness(base_im).enhance(0.88)
        h_shade_path = DATASET_DIR / f"{stem}_healthy_shade.jpg"
        h_shade.save(h_shade_path, quality=92)
        manifest.append({"path": str(h_shade_path), "stem": stem, "condition": "Healthy"})

        # 1d. Close-up Zoom (macro view of leaf blade)
        w, h = base_im.size
        h_zoom = base_im.crop((int(w * 0.12), int(h * 0.12), int(w * 0.88), int(h * 0.88))).resize((256, 256))
        h_zoom_path = DATASET_DIR / f"{stem}_healthy_zoom.jpg"
        h_zoom.save(h_zoom_path, quality=92)
        manifest.append({"path": str(h_zoom_path), "stem": stem, "condition": "Healthy"})

        # 1e. Angle flip & slight rotation
        h_rot = base_im.transpose(Image.FLIP_LEFT_RIGHT).rotate(random.choice([-6, 6]), resample=Image.BILINEAR)
        h_rot_path = DATASET_DIR / f"{stem}_healthy_angle.jpg"
        h_rot.save(h_rot_path, quality=92)
        manifest.append({"path": str(h_rot_path), "stem": stem, "condition": "Healthy"})

        # 2. Diseased: Leaf Spot (Cercospora / Alternaria)
        # 2a. Mild Leaf Spot
        ls_mild = synthesize_leaf_spots(base_im, mask, num_spots=random.randint(6, 12), severity="mild")
        ls_mild_path = DATASET_DIR / f"{stem}_leaf_spot_mild.jpg"
        ls_mild.save(ls_mild_path, quality=92)
        manifest.append({"path": str(ls_mild_path), "stem": stem, "condition": "Leaf Spot"})

        # 2b. Severe Leaf Spot
        ls_sev = synthesize_leaf_spots(base_im, mask, num_spots=random.randint(22, 38), severity="moderate")
        ls_sev_path = DATASET_DIR / f"{stem}_leaf_spot_severe.jpg"
        ls_sev.save(ls_sev_path, quality=92)
        manifest.append({"path": str(ls_sev_path), "stem": stem, "condition": "Leaf Spot"})

        # 3. Diseased: Blight (Early / Late Blight / Foliar Scorch)
        # 3a. Margin Dieback Blight
        bl_die = synthesize_blight(base_im, mask, severity=0.18)
        bl_die_path = DATASET_DIR / f"{stem}_blight_dieback.jpg"
        bl_die.save(bl_die_path, quality=92)
        manifest.append({"path": str(bl_die_path), "stem": stem, "condition": "Blight"})

        # 3b. Spreading Lesion Blight
        bl_rot = synthesize_blight(base_im, mask, severity=0.28)
        bl_rot_path = DATASET_DIR / f"{stem}_blight_rot.jpg"
        bl_rot.save(bl_rot_path, quality=92)
        manifest.append({"path": str(bl_rot_path), "stem": stem, "condition": "Blight"})

        # 4. Diseased: Nutrient Deficiency (Interveinal Chlorosis)
        # 4a. Mild Deficiency
        ch_mild = synthesize_chlorosis(base_im, mask, intensity=0.55)
        ch_mild_path = DATASET_DIR / f"{stem}_chlorosis_mild.jpg"
        ch_mild.save(ch_mild_path, quality=92)
        manifest.append({"path": str(ch_mild_path), "stem": stem, "condition": "Deficiency"})

        # 4b. Advanced Chlorosis
        ch_adv = synthesize_chlorosis(base_im, mask, intensity=0.82)
        ch_adv_path = DATASET_DIR / f"{stem}_chlorosis_adv.jpg"
        ch_adv.save(ch_adv_path, quality=92)
        manifest.append({"path": str(ch_adv_path), "stem": stem, "condition": "Deficiency"})

        # 5. Diseased: Pest Infestation
        pst = synthesize_pest_damage(base_im, mask)
        pst_path = DATASET_DIR / f"{stem}_pest.jpg"
        pst.save(pst_path, quality=92)
        manifest.append({"path": str(pst_path), "stem": stem, "condition": "Pest Infestation"})

        # 6. Diseased: Powdery Mildew
        mld = synthesize_powdery_mildew(base_im, mask)
        mld_path = DATASET_DIR / f"{stem}_mildew.jpg"
        mld.save(mld_path, quality=92)
        manifest.append({"path": str(mld_path), "stem": stem, "condition": "Powdery Mildew"})

        # 7. User Authentic Exemplars (if available for this species)
        user_exemplar_paths = list((ROOT_DIR / "user_exemplars").glob(f"{stem}*.jpg"))
        for u_idx, u_path in enumerate(user_exemplar_paths):
            u_im = Image.open(u_path).convert("RGB")
            is_mildew_exemplar = "mildew" in u_path.stem.lower()

            if is_mildew_exemplar:
                # Authentic diseased exemplar (e.g., Tomato leaf with real Powdery Mildew mycelium)
                u_std_path = DATASET_DIR / f"{stem}_user_mildew_ex_{u_idx}.jpg"
                u_im.resize((256, 256)).save(u_std_path, quality=92)
                manifest.append({"path": str(u_std_path), "stem": stem, "condition": "Powdery Mildew"})

                w_u, h_u = u_im.size
                u_c1 = u_im.crop((0, 0, int(w_u * 0.85), int(h_u * 0.85))).resize((256, 256))
                u_c1_path = DATASET_DIR / f"{stem}_user_mildew_c1_{u_idx}.jpg"
                u_c1.save(u_c1_path, quality=92)
                manifest.append({"path": str(u_c1_path), "stem": stem, "condition": "Powdery Mildew"})

                u_c2 = u_im.crop((int(w_u * 0.15), int(h_u * 0.1), w_u, h_u)).resize((256, 256))
                u_c2_path = DATASET_DIR / f"{stem}_user_mildew_c2_{u_idx}.jpg"
                u_c2.save(u_c2_path, quality=92)
                manifest.append({"path": str(u_c2_path), "stem": stem, "condition": "Powdery Mildew"})

                u_c3 = u_im.crop((int(w_u * 0.2), int(h_u * 0.2), int(w_u * 0.8), int(h_u * 0.8))).resize((256, 256))
                u_c3_path = DATASET_DIR / f"{stem}_user_mildew_c3_{u_idx}.jpg"
                u_c3.save(u_c3_path, quality=92)
                manifest.append({"path": str(u_c3_path), "stem": stem, "condition": "Powdery Mildew"})

                u_flip = u_im.transpose(Image.FLIP_LEFT_RIGHT).resize((256, 256))
                u_flip_path = DATASET_DIR / f"{stem}_user_mildew_flip_{u_idx}.jpg"
                u_flip.save(u_flip_path, quality=92)
                manifest.append({"path": str(u_flip_path), "stem": stem, "condition": "Powdery Mildew"})

                u_sun = ImageEnhance.Brightness(u_im.resize((256, 256))).enhance(1.15)
                u_sun_path = DATASET_DIR / f"{stem}_user_mildew_sun_{u_idx}.jpg"
                u_sun.save(u_sun_path, quality=92)
                manifest.append({"path": str(u_sun_path), "stem": stem, "condition": "Powdery Mildew"})

                u_shade = ImageEnhance.Brightness(u_im.resize((256, 256))).enhance(0.85)
                u_shade_path = DATASET_DIR / f"{stem}_user_mildew_shade_{u_idx}.jpg"
                u_shade.save(u_shade_path, quality=92)
                manifest.append({"path": str(u_shade_path), "stem": stem, "condition": "Powdery Mildew"})
            else:
                # Authentic healthy exemplar (snake plant, coleus, money plant, lipstick palm, badam, bismarck palm, areca, coconut)
                u_std_path = DATASET_DIR / f"{stem}_user_ex_{u_idx}.jpg"
                u_im.resize((256, 256)).save(u_std_path, quality=92)
                manifest.append({"path": str(u_std_path), "stem": stem, "condition": "Healthy"})

                w_u, h_u = u_im.size
                u_crop1 = u_im.crop((0, 0, int(w_u * 0.85), int(h_u * 0.85))).resize((256, 256))
                u_c1_path = DATASET_DIR / f"{stem}_user_crop1_{u_idx}.jpg"
                u_crop1.save(u_c1_path, quality=92)
                manifest.append({"path": str(u_c1_path), "stem": stem, "condition": "Healthy"})

                u_crop2 = u_im.crop((int(w_u * 0.15), int(h_u * 0.1), w_u, h_u)).resize((256, 256))
                u_c2_path = DATASET_DIR / f"{stem}_user_crop2_{u_idx}.jpg"
                u_crop2.save(u_c2_path, quality=92)
                manifest.append({"path": str(u_c2_path), "stem": stem, "condition": "Healthy"})

                u_crop3 = u_im.crop((int(w_u * 0.1), int(h_u * 0.1), int(w_u * 0.9), int(h_u * 0.9))).resize((256, 256))
                u_c3_path = DATASET_DIR / f"{stem}_user_crop3_{u_idx}.jpg"
                u_crop3.save(u_c3_path, quality=92)
                manifest.append({"path": str(u_c3_path), "stem": stem, "condition": "Healthy"})

                u_flip = u_im.transpose(Image.FLIP_LEFT_RIGHT).resize((256, 256))
                u_flip_path = DATASET_DIR / f"{stem}_user_flip_{u_idx}.jpg"
                u_flip.save(u_flip_path, quality=92)
                manifest.append({"path": str(u_flip_path), "stem": stem, "condition": "Healthy"})

                u_sun = ImageEnhance.Brightness(u_im.resize((256, 256))).enhance(1.15)
                u_sun_path = DATASET_DIR / f"{stem}_user_sun_{u_idx}.jpg"
                u_sun.save(u_sun_path, quality=92)
                manifest.append({"path": str(u_sun_path), "stem": stem, "condition": "Healthy"})

                u_shade = ImageEnhance.Brightness(u_im.resize((256, 256))).enhance(0.85)
                u_shade_path = DATASET_DIR / f"{stem}_user_shade_{u_idx}.jpg"
                u_shade.save(u_shade_path, quality=92)
                manifest.append({"path": str(u_shade_path), "stem": stem, "condition": "Healthy"})

                # Synthesized diseased variants on user exemplar crops
                u_mask = get_leaf_mask(u_im.resize((256, 256)), stem)
                u_spot = synthesize_leaf_spots(u_im.resize((256, 256)), u_mask, num_spots=15)
                u_spot_path = DATASET_DIR / f"{stem}_user_spot_{u_idx}.jpg"
                u_spot.save(u_spot_path, quality=92)
                manifest.append({"path": str(u_spot_path), "stem": stem, "condition": "Leaf Spot"})

                u_blight = synthesize_blight(u_im.resize((256, 256)), u_mask)
                u_blight_path = DATASET_DIR / f"{stem}_user_blight_{u_idx}.jpg"
                u_blight.save(u_blight_path, quality=92)
                manifest.append({"path": str(u_blight_path), "stem": stem, "condition": "Blight"})

                u_chlor = synthesize_chlorosis(u_im.resize((256, 256)), u_mask)
                u_chlor_path = DATASET_DIR / f"{stem}_user_chlor_{u_idx}.jpg"
                u_chlor.save(u_chlor_path, quality=92)
                manifest.append({"path": str(u_chlor_path), "stem": stem, "condition": "Deficiency"})

                u_mld = synthesize_powdery_mildew(u_im.resize((256, 256)), u_mask)
                u_mld_path = DATASET_DIR / f"{stem}_user_mildew_{u_idx}.jpg"
                u_mld.save(u_mld_path, quality=92)
                manifest.append({"path": str(u_mld_path), "stem": stem, "condition": "Powdery Mildew"})

    logger.info(f"Dataset generation complete. Total samples: {len(manifest)}")
    return manifest


class BotanicalDataset(Dataset):
    def __init__(self, manifest: list[dict], transform=None):
        self.manifest = manifest
        self.transform = transform or transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def __len__(self):
        return len(self.manifest)

    def __getitem__(self, idx):
        item = self.manifest[idx]
        im = Image.open(item["path"]).convert("RGB")
        tensor = self.transform(im)
        species_label = STEM_TO_IDX[item["stem"]]
        condition_label = CONDITION_TO_IDX[item["condition"]]
        return tensor, species_label, condition_label, item["stem"], item["condition"]


class FloraDualNet(nn.Module):
    """Dual-head neural classifier: Species Identification + Foliar Pathology Recognition."""
    def __init__(self, backbone, num_species: int = 45, num_conditions: int = 6):
        super().__init__()
        self.backbone = backbone
        self.backbone.classifier = nn.Identity()

        # Species head: Maps invariant deep features to species classes
        self.species_head = nn.Sequential(
            nn.Linear(576, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, num_species),
        )

        # Pathology head: Maps features to foliar health condition
        self.pathology_head = nn.Sequential(
            nn.Linear(576, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, num_conditions),
        )

    def forward(self, x):
        feat = self.backbone(x)
        feat_norm = F.normalize(feat, p=2, dim=1)
        species_logits = self.species_head(feat)
        pathology_logits = self.pathology_head(feat)
        return feat_norm, species_logits, pathology_logits


def train_model(manifest: list[dict]):
    """Train the dual-head botanical vision network with GPU acceleration."""
    device = torch.device("mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu"))
    logger.info(f"Training on device: {device}")

    # Random split 85% train, 15% validation
    random.seed(42)
    random.shuffle(manifest)
    split_idx = int(len(manifest) * 0.85)
    train_manifest = manifest[:split_idx]
    val_manifest = manifest[split_idx:]

    train_loader = DataLoader(BotanicalDataset(train_manifest), batch_size=32, shuffle=True)
    val_loader = DataLoader(BotanicalDataset(val_manifest), batch_size=32, shuffle=False)

    # Initialize pretrained MobileNetV3
    weights = models.MobileNet_V3_Small_Weights.DEFAULT
    backbone = models.mobilenet_v3_small(weights=weights)
    model = FloraDualNet(backbone, num_species=len(STEMS), num_conditions=len(CONDITIONS)).to(device)

    species_criterion = nn.CrossEntropyLoss()
    pathology_criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=25)

    num_epochs = 25
    best_acc = 0.0

    logger.info(f"Starting training for {num_epochs} epochs over {len(train_manifest)} training specimens...")
    for epoch in range(1, num_epochs + 1):
        model.train()
        total_loss = 0.0
        correct_species = 0
        correct_pathology = 0
        total_samples = 0

        for x, y_sp, y_cond, _, _ in train_loader:
            x = x.to(device)
            y_sp = y_sp.to(device)
            y_cond = y_cond.to(device)

            optimizer.zero_grad()
            feat_norm, sp_out, cond_out = model(x)
            loss_sp = species_criterion(sp_out, y_sp)
            loss_cond = pathology_criterion(cond_out, y_cond)
            loss = loss_sp + 1.2 * loss_cond

            loss.backward()
            optimizer.step()

            total_loss += loss.item() * len(x)
            correct_species += (sp_out.argmax(dim=1) == y_sp).sum().item()
            correct_pathology += (cond_out.argmax(dim=1) == y_cond).sum().item()
            total_samples += len(x)

        scheduler.step()

        # Validation
        model.eval()
        val_correct_sp = 0
        val_correct_cond = 0
        val_total = 0
        with torch.no_grad():
            for x, y_sp, y_cond, _, _ in val_loader:
                x = x.to(device)
                y_sp = y_sp.to(device)
                y_cond = y_cond.to(device)
                _, sp_out, cond_out = model(x)
                val_correct_sp += (sp_out.argmax(dim=1) == y_sp).sum().item()
                val_correct_cond += (cond_out.argmax(dim=1) == y_cond).sum().item()
                val_total += len(x)

        train_sp_acc = correct_species / total_samples * 100
        train_cond_acc = correct_pathology / total_samples * 100
        val_sp_acc = val_correct_sp / val_total * 100
        val_cond_acc = val_correct_cond / val_total * 100

        if epoch % 5 == 0 or epoch == num_epochs:
            logger.info(
                f"Epoch [{epoch:2d}/{num_epochs}] Loss: {total_loss/total_samples:.4f} | "
                f"Train Sp: {train_sp_acc:.1f}% Cond: {train_cond_acc:.1f}% | "
                f"Val Sp: {val_sp_acc:.1f}% Cond: {val_cond_acc:.1f}%"
            )

    # Save model weights
    model_save_path = MODELS_DIR / "flora_neural_engine.pt"
    torch.save(model.state_dict(), model_save_path)
    logger.info(f"Model saved to {model_save_path}")

    # Build comprehensive condition-aware prototype centroid matrix
    logger.info("Computing condition-aware prototype centroid matrix for all 45 species...")
    model.eval()
    species_condition_prototypes = {}
    full_loader = DataLoader(BotanicalDataset(manifest), batch_size=32, shuffle=False)

    embeddings_by_stem = {s: [] for s in STEMS}
    with torch.no_grad():
        for x, _, _, stems, conditions in full_loader:
            x = x.to(device)
            feat_norm, _, _ = model(x)
            feats = feat_norm.cpu().numpy()
            for i, st in enumerate(stems):
                embeddings_by_stem[st].append(feats[i])

    # Direct authentic user exemplar anchoring
    eval_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    user_embeddings = {s: [] for s in STEMS}
    for u_path in (ROOT_DIR / "user_exemplars").glob("*.jpg"):
        stem_match = next((s for s in STEMS if u_path.stem.startswith(s)), None)
        if stem_match:
            u_im = Image.open(u_path).convert("RGB")
            u_tensor = eval_transform(u_im).unsqueeze(0).to(device)
            with torch.no_grad():
                u_feat, _, _ = model(u_tensor)
            user_embeddings[stem_match].append(u_feat.squeeze().cpu().numpy())

    prototypes_v3 = {}
    for st, emb_list in embeddings_by_stem.items():
        if emb_list:
            gen_centroid = np.mean(emb_list, axis=0)
            if user_embeddings[st]:
                user_centroid = np.mean(user_embeddings[st], axis=0)
                # 40% dataset spread + 60% authentic field anchor
                centroid = 0.4 * gen_centroid + 0.6 * user_centroid
            else:
                centroid = gen_centroid
            centroid = centroid / (np.linalg.norm(centroid) + 1e-6)
            prototypes_v3[st] = centroid.astype(np.float32)

    proto_path = ROOT_DIR / "plant_prototypes_v3.npy"
    np.save(proto_path, prototypes_v3)
    logger.info(f"Updated prototype centroids for {len(prototypes_v3)} species in {proto_path}")

    # Save metadata mapping
    metadata = {
        "species_count": len(STEMS),
        "conditions": CONDITIONS,
        "species": STEMS,
        "val_species_accuracy": val_sp_acc,
        "val_pathology_accuracy": val_cond_acc,
    }
    with open(MODELS_DIR / "flora_model_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Training successfully completed with Validation Species Accuracy: {val_sp_acc:.1f}% and Pathology Accuracy: {val_cond_acc:.1f}%")


if __name__ == "__main__":
    manifest = generate_dataset()
    train_model(manifest)

