# Railway Deployment Guide - Sign Language Interpreter

## Why Railway?

- ✅ **Linux-based infrastructure** - No Windows DLL issues
- ✅ **Python 3.11 support** - TensorFlow works reliably
- ✅ **Simple GitHub integration** - Auto-deploy on push
- ✅ **Free tier available** - Start for free ($5 credit/month)
- ✅ **Better Python version handling** than Render

## Step 1: Push Code to GitHub

Your code is already in GitHub: `https://github.com/ishayadav191205-prog/translator`

Verify latest code is pushed:
```bash
cd C:\Users\PC\OneDrive\Desktop\TRANSLATOR\Sign-Language-Interpreter-using-Deep-Learning
git status
git add .
git commit -m "Railway deployment setup"
git push origin main
```

## Step 2: Create Railway Account

1. Go to **https://railway.app**
2. Click **"Start Project"**
3. Sign up with GitHub (recommended)
4. Authorize Railway to access your repositories

## Step 3: Create New Project on Railway

### Option A: Deploy from GitHub (Recommended)
1. Click **"New Project"** → **"Deploy from GitHub"**
2. Select your repository: **translator**
3. Select the **main** branch
4. Railway will auto-detect it's a Python project

### Option B: Manual Project Creation
1. Click **"New Project"**
2. Select **Python** as the service
3. Railway will ask for repository details
4. Connect your GitHub repo

## Step 4: Configure Environment Variables

In Railway dashboard:

1. Go to your project → **Settings** → **Variables**
2. Add these environment variables:

```
FLASK_ENV=production
MODEL_PATH=/app/Code/cnn_model_keras2.h5
PORT=5000
DEBUG_MODE=false
```

## Step 5: Configure Build & Start Commands

Railway should auto-detect, but if not:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
cd Code && gunicorn --bind 0.0.0.0:$PORT app:app
```

## Step 6: Deploy

1. Commit and push any changes:
```bash
git add .
git commit -m "Deploy to Railway"
git push origin main
```

2. Railway will automatically:
   - Detect the push
   - Build the project
   - Deploy to production
   - Generate a public URL

3. View deployment logs in Railway dashboard to monitor process

## Step 7: Get Your Public URL

1. In Railway dashboard, open your project
2. Click the service (Python)
3. Look for **"Generate Domain"** or copy the Railway URL
4. Your app is now public! Example: `https://your-project.railway.app`

## Step 8: Test the Deployment

```bash
# Replace with your Railway URL
curl https://your-project.railway.app/health

# Should return:
# {"status":"ok","model_loaded":true,"timestamp":"2026-03-23T..."}
```

## Step 9: Access the Web UI

Open in browser:
```
https://your-project.railway.app/
```

All 5 features should work:
- ✅ Dark Mode
- ✅ Sound Effects
- ✅ Confidence Meter
- ✅ Gesture Counter
- ✅ Confidence Graph

## Troubleshooting

### Build Fails with TensorFlow Error
Railway uses Linux, so TensorFlow should work fine. If issues:
1. Check build logs in Railway dashboard
2. Ensure `requirements.txt` has `tensorflow-cpu==2.13.0`
3. If it persist, try: `tensorflow==2.14.0`

### Model Loading Fails
Check your environment variable:
```
MODEL_PATH=/app/Code/cnn_model_keras2.h5
```

Ensure the model file exists in repository!

### 502 Bad Gateway Error
Usually means the Flask app is crashing. Check logs:
1. Go to Railway dashboard
2. Click project → Logs
3. Look for Python error messages

### Port or Binding Issues
Railway uses dynamic PORT variable. App already handles this in Procfile:
```
gunicorn --bind 0.0.0.0:$PORT app:app
```

Leave as-is, don't hardcode port 5000.

## Auto-Redeploy on Changes

Railway automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add Code/app.py
git commit -m "Fix prediction logic"
git push origin main

# Railway will automatically rebuild and deploy!
```

## Monitor Your Deployment

Railway dashboard shows:
- **Logs** - Real-time server output
- **Metrics** - CPU, memory, network usage
- **Deployments** - History of builds
- **Settings** - Environment variables, domains, etc.

## Differences from Local (ngrok)

| Feature | Local + ngrok | Railway |
|---------|-----|---------|
| Runtime | Windows | Linux |
| URL Changes | Yes (new on restart) | Permanent domain |
| Always Online | No (your PC must be on) | Yes (24/7) |
| Setup Time | ~5 minutes | ~10 minutes |
| TensorFlow Support | 🔴 DLL Issues | ✅ Works perfectly |
| Sharing | Need to restart for fresh URL | Just share permanent domain |

## Next Steps

If Railway deployment doesn't work:
1. Share build logs from Railway dashboard
2. We can try alternative: Heroku, Fly.io, or DigitalOcean

Happy deploying! 🚀
