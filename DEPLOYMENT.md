# Deployment Guide

## Option 1: Render.com (Recommended - Free Tier Available)

### Steps:

1. **Push your code to GitHub**
   - Create a GitHub repository
   - Push all your code to it

2. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Name**: notethetic-app (or any name)
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn server:app`

4. **Set Environment Variables**
   In Render dashboard, go to "Environment" and add:
   - `SECRET_KEY` - Generate a random secret key (you can use: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase anon key
   - `SUPABASE_SERVICE_KEY` - Your Supabase service role key
   - `REDIRECT_URL` - Your Render app URL (e.g., `https://your-app.onrender.com/signin`)
   - `FLASK_ENV` - Set to `production`

5. **Update Supabase Auth Settings**
   - Go to Supabase Dashboard → Authentication → URL Configuration
   - Add your Render URL to "Redirect URLs": `https://your-app.onrender.com/signin`

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (takes 2-3 minutes)
   - Your app will be live at `https://your-app.onrender.com`

---

## Option 2: Railway (Alternative - Free Tier)

1. **Push to GitHub** (same as above)

2. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

3. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

4. **Configure**
   - Railway auto-detects Python
   - Add environment variables (same as Render)
   - Set start command: `gunicorn server:app --bind 0.0.0.0:$PORT`

5. **Deploy**
   - Railway auto-deploys on push
   - Get your URL from dashboard

---

## Option 3: PythonAnywhere (Simple but Limited Free Tier)

1. **Sign up** at https://www.pythonanywhere.com

2. **Upload files** via Files tab

3. **Create Web App**
   - Go to Web tab
   - Click "Add a new web app"
   - Choose Flask and Python 3.10

4. **Configure**
   - Set source code path
   - Set WSGI file to point to your app
   - Add environment variables in Web tab

5. **Reload** the web app

---

## Important Notes:

### Environment Variables Needed:
```
SECRET_KEY=your-secret-key-here
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key
REDIRECT_URL=https://your-deployed-url.com/signin
FLASK_ENV=production
```

### Before Deploying:
1. ✅ Test locally first
2. ✅ Make sure all environment variables are set
3. ✅ Update Supabase redirect URLs
4. ✅ Remove any localhost URLs from code
5. ✅ Test the deployed app

### Troubleshooting:
- **App crashes**: Check logs in deployment platform
- **Database errors**: Verify Supabase keys are correct
- **Auth not working**: Check redirect URL matches Supabase settings
- **Static files not loading**: Ensure static folder is included in deployment

---

## Quick Deploy Checklist:

- [ ] Code pushed to GitHub
- [ ] All environment variables set
- [ ] Supabase redirect URLs updated
- [ ] Requirements.txt includes gunicorn
- [ ] Procfile created (for some platforms)
- [ ] Test deployment locally with production settings

