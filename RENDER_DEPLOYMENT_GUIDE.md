# 🚀 Render Deployment Guide

## Quick Start (5 minutes)

### **Step 1: Push to GitHub**
```bash
# Initialize git repo (if not already done)
git init
git add .
git commit -m "Initial commit: Sign Language Interpreter"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Sign-Language-Interpreter-using-Deep-Learning.git
git push -u origin main
```

### **Step 2: Create Render Account**
1. Go to https://render.com
2. Sign up with GitHub (easiest)
3. Authorize Render to access your repos

### **Step 3: Deploy Backend**
1. Click **"New +"** → **"Web Service"**
2. Select your GitHub repo
3. Configure:
   - **Name:** `sign-language-interpreter`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --chdir Code app:app --bind 0.0.0.0:$PORT`
   - **Plan:** Free (or Starter for reliability)
4. Click **Deploy**
5. Wait 2-3 minutes for build to complete
6. Copy your Render URL (e.g., `https://sign-language-interpreter-xxxx.onrender.com`)

### **Step 4: Update Frontend API URL**
In `Code/static/index.html`, find:
```javascript
const API_URL = window.location.origin;
```

Replace with:
```javascript
const API_URL = 'https://your-render-url.onrender.com';
```

### **Step 5: Deploy Frontend on Vercel**
1. Go to https://vercel.com
2. Click **"Add New"** → **"Project"**
3. Import your GitHub repo
4. Configure:
   - **Build Command:** (leave empty)
   - **Output Directory:** `Code`
5. Click **Deploy**
6. Your frontend is live! 🎉

---

## What Gets Deployed

**Backend (Render):**
- ✅ `app.py` (Flask server)
- ✅ `cnn_model_keras2.h5` (ML model)
- ✅ `Code/static/index.html` (frontend files)
- ✅ All Python dependencies

**Frontend (Vercel):**
- ✅ `Code/static/index.html`
- ✅ CSS & JavaScript
- ✅ Calls Render backend API

---

## File Structure (for deployment)

```
Sign-Language-Interpreter/
├── requirements.txt          ← Dependencies
├── Procfile                  ← Start command
├── runtime.txt               ← Python version
├── render.yaml               ← Render config (optional)
├── .gitignore                ← Ignore files
├── Code/
│   ├── app.py                ← Flask backend
│   ├── cnn_model_keras2.h5   ← ML model
│   └── static/
│       └── index.html        ← Frontend
└── README.md
```

---

## Troubleshooting

### ❌ "Build Failed"
- Check `requirements.txt` format
- Ensure no version conflicts
- View logs in Render dashboard

### ❌ "TensorFlow build timeout"
- Switch to **Starter plan** (more build time)
- Or use pre-built wheels only

### ❌ "Model not found"
- Ensure `cnn_model_keras2.h5` is in `Code/` directory
- Check file path in `app.py`

### ❌ "CORS errors"
- Verify `flask-cors` installed
- Check `app.py` has `CORS(app)` enabled

---

## Cost

- **Render Free Plan:** $0/month (sleeps after 15 min inactivity)
- **Render Starter:** $7/month (always on)
- **Vercel:** Free tier excellent, or upgrade as needed

---

## After Deployment

✅ Your site is live!
- Backend: `https://your-render-url.onrender.com`
- Frontend: `https://your-vercel-url.vercel.app`

✅ Share with anyone:
- They can access from any browser
- No camera? Use upload feature
- Real-time gesture recognition! 🎉

---

## Environment Variables (Optional)

If you need to add secrets:
1. In Render dashboard → Environment
2. Add `KEY=VALUE` pairs
3. Access in `app.py` via `os.getenv('KEY')`

---

Need help? Check Render docs: https://render.com/docs
