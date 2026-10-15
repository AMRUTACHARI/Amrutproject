# ⚡ FLORAai — 1-Page Quick Cheatsheet for Teacher Presentation
*Keep this open on your phone or printed on paper while presenting to your teacher!*

---

## 🎯 3 Key Numbers to Mention:
1. **63 Species:** Full agricultural, spice, medicinal, and orchard coverage for the Indian subcontinent.
2. **12 Palms:** Comprehensive Palm Herbarium (Coconut, Areca, Lipstick, Date, Wild Date, Fish-tail, Golden Cane, Royal, Foxtail, Bottle, Bismarck, Palmyra).
3. **100% Organic:** Every single diagnostic recommendation uses natural remedies (neem oil, buttermilk spray, wood ash, Trichoderma).

---

## 💻 Tech Stack in 30 Seconds:
- **Frontend:** React 18 + Vanilla CSS / Tailwind Tokens + Radix UI + CRACO
- **Backend:** Python 3.10 + FastAPI + Uvicorn ASGI Server
- **Database:** MongoDB 7.0 + Motor (Asynchronous Python driver)
- **Security:** Dual JWT (Access + Refresh) in `HttpOnly` `SameSite` cookies + 12-round bcrypt password hashing + brute force lockout
- **AI Core:** Google Gemini Vision Multimodal + Custom Indian Botanical Prompt Engine
- **DevOps:** Docker multi-stage builds + Docker Compose orchestration

---

## 🗣️ The 4 Talking Points During Live Demo:
1. **Homepage:** *"Notice the clean, responsive design highlighting 63 Indian species with real verified plant photos."*
2. **Dashboard Scanner:** *"We use the HTML5 MediaDevices API to capture real-time camera frames and serialize them into Base64 data strings."*
3. **Diagnosis Card:** *"Notice that instead of medical Latin jargon like 'chlorosis', the AI explains the problem in plain English and recommends home remedies like cold-pressed neem oil."*
4. **History Page:** *"Every scan is saved to MongoDB, allowing users to track recovery, filter by status, and export their scan history to JSON."*

---

## 🛡️ Quick Answers to Common Teacher Questions:
- **"Why MongoDB?"** ➔ *"Semi-structured botanical reports contain variable arrays of remedies and precautions, making document storage in MongoDB much faster and more flexible than multi-table SQL joins."*
- **"Why FastAPI?"** ➔ *"Asynchronous I/O gives it NodeJS-level concurrency while keeping Python's rich AI and machine learning ecosystem."*
- **"How is it secure?"** ➔ *"Tokens are in HttpOnly cookies, so malicious JavaScript can never steal them via XSS attacks."*
- **"Where is the code?"** ➔ *"[https://github.com/AMRUTACHARI/Amrutproject](https://github.com/AMRUTACHARI/Amrutproject)"*
