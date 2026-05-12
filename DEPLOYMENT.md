# ZORQ AI Deployment Guide

Complete guide for deploying ZORQ AI to production platforms.

## 📋 Pre-Deployment Checklist

Before pushing to GitHub and deploying, ensure:

- [ ] All files added to git
- [ ] No `.env` file committed (API key protected)
- [ ] `.gitignore` includes `.env`, `__pycache__`, `venv/`
- [ ] `requirements.txt` up to date
- [ ] All dependencies installed locally and tested
- [ ] No debug mode enabled in production
- [ ] API key moved to environment variables
- [ ] README.md updated with your info
- [ ] CONTRIBUTING.md updated with your contact
- [ ] LICENSE file included
- [ ] No hardcoded credentials anywhere

## 🚀 Deployment Platforms

### 1. Render (RECOMMENDED - Free & Easy)

Render is the easiest option for Python Flask apps with a free tier.

**Advantages:**
- ✅ Completely free tier (with limitations)
- ✅ Auto-deploys on Git push
- ✅ Great documentation
- ✅ Easy environment variables
- ✅ Custom domains available

**Steps:**

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial ZORQ deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/zorq.git
   git push -u origin main
   ```

2. **Create Render Account:**
   - Go to https://render.com
   - Sign up with GitHub
   - Click "New +" → Web Service
   - Select your `zorq` repository
   - Enter details:
     - Name: `zorq` (or your choice)
     - Environment: `Python 3.11`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python server.py`
   - Click Create Web Service

3. **Set Environment Variable:**
   - In dashboard, go to Environment
   - Add new variable:
     - Key: `GROQ_API_KEY`
     - Value: `gsk_your_actual_key`
   - Save and deploy

4. **Wait for Deployment:**
   - Takes ~2 minutes
   - You'll get a URL: `https://zorq-xxxxx.onrender.com`
   - Your app is live! 🎉

**Free Tier Limits:**
- Auto-spins down after 15 minutes of inactivity
- 0.5 GB RAM
- 750 hours/month (free tier)
- Upgrade to paid for always-on service

---

### 2. Railway (Easy Alternative)

Simple Python deployment with good free tier.

**Steps:**

1. **Connect GitHub:**
   - Go to https://railway.app
   - Sign up with GitHub
   - Click "Create Project"
   - Select "GitHub Repo" → Find `zorq`

2. **Add Variables:**
   - In project settings, add:
     - `GROQ_API_KEY` = your key
     - `PORT` = 5000

3. **Deploy:**
   - Railway auto-deploys on push
   - Get your project URL
   - Done!

**Free Tier:** $5 credit/month (usually covers light usage)

---

### 3. PythonAnywhere

Dedicated Python hosting platform.

**Steps:**

1. Go to https://www.pythonanywhere.com
2. Create account (free tier available)
3. Upload your files or clone from GitHub
4. Create new web app (Flask)
5. Configure WSGI file
6. Add environment variables in web app settings
7. Reload web app

**Free Tier:** Limited but works for testing

---

### 4. Heroku (Classic but More Expensive)

Traditional hosting platform (now paid only).

**Steps:**

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: python server.py
   ```
3. Create `runtime.txt`:
   ```
   python-3.11.4
   ```
4. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   heroku config:set GROQ_API_KEY=your_key
   git push heroku main
   ```

---

### 5. DigitalOcean (Full Control)

VPS with more control (paid, ~$5/month).

**Steps:**

1. Create DigitalOcean account
2. Create Droplet (Ubuntu 22.04, Basic $4/month)
3. SSH into server
4. Install Python, pip, Flask, requirements
5. Use Gunicorn + Nginx
6. Set up environment variables
7. Configure Nginx reverse proxy

---

## 🔐 Environment Variables Setup

### For All Platforms:

Create `.env.example` (no real keys):
```
GROQ_API_KEY=gsk_your_api_key_here_replace_this
GROQ_MODEL=llama-3.1-8b-instant
PORT=5000
FLASK_DEBUG=false
```

User copies to `.env` locally (not committed to git).

### Platform-Specific:

**Render:**
```
Dashboard → Environment → Add Variable
GROQ_API_KEY = gsk_xxxxxxxxxxxxxx
```

**Railway:**
```
Variables section in project settings
GROQ_API_KEY = gsk_xxxxxxxxxxxxxx
```

**PythonAnywhere:**
```
Web app settings → Environment variables
GROQ_API_KEY = gsk_xxxxxxxxxxxxxx
```

**Heroku:**
```bash
heroku config:set GROQ_API_KEY=gsk_xxxxxxxxxxxxxx
```

---

## 📊 Performance Optimization

### Before Deployment:

1. **Minify CSS/JavaScript:**
   ```bash
   # Install minifier
   npm install -g csso-cli terser
   
   # Minify (optional - only if you want smaller files)
   csso dashboard.css -o dashboard.min.css
   terser dashboard.js -o dashboard.min.js
   ```

2. **Update HTML to use minified files:**
   ```html
   <link rel="stylesheet" href="dashboard.min.css">
   <script src="dashboard.min.js"></script>
   ```

3. **Enable caching in server.py:**
   ```python
   from flask import Flask
   app = Flask(__name__)
   
   @app.after_request
   def set_cache_headers(response):
       response.headers['Cache-Control'] = 'public, max-age=3600'
       return response
   ```

4. **Use compression:**
   ```bash
   pip install Flask-Compress
   ```
   
   ```python
   from flask_compress import Compress
   Compress(app)
   ```

---

## 🔒 Security Checklist

Before deploying:

- [ ] No API keys in code
- [ ] `.env` in `.gitignore`
- [ ] `FLASK_DEBUG = False`
- [ ] No verbose error messages
- [ ] HTTPS enabled (platforms provide this)
- [ ] Input validation in place
- [ ] Output sanitized
- [ ] CORS properly configured
- [ ] Rate limiting implemented (optional)
- [ ] No hardcoded credentials anywhere

---

## 🧪 Testing Before Deploy

### Local Testing:

```bash
# Simulate production
export FLASK_DEBUG=false
python server.py

# Test all features:
1. Load all pages
2. Complete auth flow
3. Send test messages
4. Check responses
5. Open DevTools (F12) - no errors
6. Test on mobile (DevTools → Responsive Design)
```

### Post-Deployment Testing:

1. **Visit live URL:**
   - Open `https://your-app-url.com`
   - Test all features again

2. **Performance:**
   - Check load time in DevTools
   - Should be <3 seconds

3. **Mobile Testing:**
   - Test on actual phone
   - Check responsiveness
   - Verify buttons work

4. **Chat Testing:**
   - Send multiple messages
   - Verify responses arrive
   - Check no errors in console

---

## 📈 Monitoring & Logs

### View Logs:

**Render:**
```
Dashboard → Logs tab → View all logs
```

**Railway:**
```
Project → Deployments → View logs
```

**Heroku:**
```bash
heroku logs --tail
```

### Check Errors:

1. Real-time monitoring
2. Check for connection errors
3. Monitor API calls
4. Track response times

---

## 🔄 Continuous Deployment

Most platforms auto-deploy on git push:

```bash
# Make changes locally
git add .
git commit -m "Fix responsive design"
git push origin main

# Platform automatically:
1. Pulls latest code
2. Installs dependencies
3. Restarts server
4. Updates live site
```

---

## 🆙 Updating Your App

To update your deployed app:

1. **Make local changes:**
   ```bash
   # Edit files...
   ```

2. **Test locally:**
   ```bash
   python server.py
   # Test all features in http://localhost:5000
   ```

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin main
   ```

4. **App auto-updates** (usually within 1-2 minutes)

---

## 💰 Cost Comparison

| Platform | Cost | Free Tier | Notes |
|----------|------|-----------|-------|
| Render | $7-12/mo | ✅ Limited | Best free tier |
| Railway | $5 credit/mo | ✅ Limited | Great value |
| Heroku | $7-50/mo | ❌ None | Most reliable |
| PythonAnywhere | $5-35/mo | ✅ Limited | Python-specific |
| DigitalOcean | $4-40/mo | ❌ None | Full control |

**Recommendation for Testing:** Render (free tier)
**Recommendation for Production:** Render (paid) or Railway (paid)

---

## 🚨 Troubleshooting Deployment

### App Won't Start

**Check:**
```
1. Are all requirements installed?
2. Is GROQ_API_KEY set?
3. Check logs for errors
4. Is port correct?
```

**Fix:**
```
1. Verify requirements.txt is complete
2. Set environment variables on platform
3. Restart deployment
```

### API Returns 404

**Check:**
```
1. Is server running?
2. Is /api/chat endpoint accessible?
3. Check logs
```

**Fix:**
```
1. Check server.py for typos
2. Verify Flask routes
3. Check platform logs
```

### Slow Performance

**Check:**
```
1. Response time in DevTools
2. Server logs
3. API call duration
```

**Fix:**
```
1. Upgrade platform tier
2. Optimize code
3. Enable caching
4. Use CDN for static files
```

---

## 📖 Additional Resources

- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Flask Deployment](https://flask.palletsprojects.com/deployment/)
- [Groq API Status](https://status.groq.com)

---

## ✅ Deployment Success Checklist

After successful deployment:

- [ ] App loads without errors
- [ ] Chat functionality works
- [ ] API responses appear
- [ ] Mobile view works
- [ ] No console errors (F12)
- [ ] Performance acceptable (<3s load)
- [ ] Environment variables set
- [ ] No API keys in logs
- [ ] HTTPS enabled
- [ ] Custom domain (optional)

---

## 🎉 You're Done!

Your ZORQ AI is now live on the internet!

**Share your deployment:**
- Post on GitHub
- Share on social media
- Tell friends and family
- Get feedback and improve

**Keep improving:**
- Monitor user feedback
- Fix bugs quickly
- Add new features
- Optimize performance

---

**Happy deploying! 🚀**
