# 🚀 RENDER FREE TIER DEPLOYMENT GUIDE (Web Service)

**Deploy Daily AI News on Render using the FREE tier with Web Service + External Scheduler.**

---

## ⚡ Quick Overview

Render's **Cron Jobs** require a paid plan, but **Web Services** are FREE! Here's the solution:

```
Your Application (Web Service - FREE)
    ↓
    HTTP endpoint: /trigger-news
    ↓
External Scheduler (Free options):
    • GitHub Actions (FREE)
    • EasyCron (FREE)
    • CRON-job.org (FREE)
    ↓
Triggers daily at 10:00 PM
    ↓
Sends email automatically
```

---

## 📋 Prerequisites

Same as before:
- ✅ GitHub account
- ✅ Render account
- ✅ API keys (OpenAI, NewsAPI)
- ✅ Gmail app password

---

## 🚀 STEP 1: Deploy on Render (Free Tier)

### 1.1 Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **+ New** → **Web Service** (⚠️ NOT Cron Job!)
3. Click **Connect Repository**
4. Select **daily-ai-news**
5. Click **Connect**

### 1.2 Configure Web Service

Fill in these fields:

```
Name:                      daily-ai-news
Language:                  Python 3
Region:                    Your closest region
Plan:                      FREE ✅

Build Command:             pip install -r requirements.txt
Start Command:             python app/main.py

Environment Variables:     (same 8 as before)
```

### 1.3 Add Environment Variables

Click **Environment** and add:

```
OPENAI_API_KEY          = sk-proj-xxxxx...
NEWSAPI_KEY             = 0fa5a91c...
EMAIL_SENDER            = your@gmail.com
EMAIL_PASSWORD          = xxxx xxxx xxxx xxxx
EMAIL_RECIPIENT         = recipient@example.com
SMTP_SERVER             = smtp.gmail.com
SMTP_PORT               = 587
SCHEDULE_TIME           = 22:00
PORT                    = 5000
```

### 1.4 Deploy

1. Click **Create Web Service**
2. Wait for build (2-3 minutes)
3. Check status → should show **Deployed** ✅

### 1.5 Get Your Service URL

Once deployed:
1. Go to your service page in Render
2. Copy the service URL → looks like: `https://daily-ai-news.onrender.com`
3. **Save this URL** - you'll need it!

---

## ✅ STEP 2: Test the Endpoint

### 2.1 Test Health Check

Open in browser:
```
https://your-service-url.onrender.com/
```

You should see:
```json
{
  "status": "healthy",
  "service": "Daily AI News Automation",
  "version": "1.0",
  "next_run": "Daily at 22:00 UTC"
}
```

### 2.2 Test Trigger Endpoint

Use a REST client (Postman, Insomnia) or curl:

```bash
curl -X POST https://your-service-url.onrender.com/trigger-news
```

You should see:
```json
{
  "status": "success",
  "message": "News email sent successfully"
}
```

And receive an email in your inbox!

### 2.3 View Logs

Open in browser:
```
https://your-service-url.onrender.com/logs
```

Shows last 50 lines of application logs.

---

## ⏰ STEP 3: Set Up Automatic Daily Trigger

You now have a working HTTP endpoint. Now you need something to call it **every day at 10:00 PM**.

### Option A: GitHub Actions (Recommended - FREE)

**Most reliable, integrated with GitHub, completely FREE**

#### Step A.1: Create GitHub Actions Workflow

1. Go to your GitHub repo
2. Click **Code** → Navigate to root directory
3. Create folder: `.github/workflows/`
4. Create file: `.github/workflows/daily-news.yml`

Add this content:

```yaml
name: Daily AI News Trigger

on:
  schedule:
    - cron: '0 22 * * *'  # Daily at 10 PM UTC
  workflow_dispatch:       # Allows manual trigger

jobs:
  trigger-news:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Daily News Update
        run: |
          curl -X POST https://your-service-url.onrender.com/trigger-news
```

**Important:** Replace `https://your-service-url.onrender.com` with your actual Render service URL!

#### Step A.2: Commit and Push

```bash
git add .github/workflows/daily-news.yml
git commit -m "Add GitHub Actions daily trigger"
git push
```

#### Step A.3: Verify

1. Go to GitHub repo
2. Click **Actions** tab
3. You should see "Daily AI News Trigger" workflow
4. It will run automatically at 10 PM UTC daily
5. You can click "Run workflow" to test manually

**Advantages:**
- ✅ Completely FREE
- ✅ No additional account needed
- ✅ Reliable (GitHub infrastructure)
- ✅ Easy to debug (see logs)
- ✅ Integrated with your code

---

### Option B: EasyCron (Alternative - FREE)

**If you prefer not to use GitHub Actions**

#### Step B.1: Create Free EasyCron Account

1. Go to https://www.easycron.com
2. Sign up with email
3. No credit card needed

#### Step B.2: Create New Cron Job

1. Click **Cron Jobs** → **Create a cron job**
2. Fill in:

```
Cron Job URL:   https://your-service-url.onrender.com/trigger-news
Method:         POST
Cron Expression: 0 22 * * *  (10 PM UTC)
```

3. Click **Save**

#### Step B.3: Verify

- You should see the cron job listed
- It will execute daily at 10 PM UTC

**Advantages:**
- ✅ Very simple setup
- ✅ No GitHub needed
- ✅ Good uptime

**Disadvantages:**
- ⚠️ Requires separate account
- ⚠️ Less integration

---

### Option C: CRON-job.org (Alternative - FREE)

**Another free option**

1. Go to https://cron-job.org
2. Sign up (free)
3. Create new job:

```
URL:             https://your-service-url.onrender.com/trigger-news
Schedule:        10 PM UTC daily (0 22 * * *)
Notification:    Email on failure (optional)
```

4. Click **Create**

---

## 🔄 How to Choose a Scheduler

| Scheduler | Setup | Reliability | Best For |
|-----------|-------|------------|----------|
| **GitHub Actions** | Easy | Excellent | GitHub users |
| **EasyCron** | Very easy | Good | Simple setup |
| **CRON-job.org** | Very easy | Good | Backup option |

**Recommendation:** Use **GitHub Actions** for best reliability and integration.

---

## 📊 Complete Architecture (Free Tier)

```
┌─────────────────────┐
│  Your Local PC      │
│  (test code)        │
└──────────┬──────────┘
           │ git push
           ↓
┌─────────────────────┐
│  GitHub Repository  │
│  + GitHub Actions   │ ← Triggers at 10 PM UTC
└──────────┬──────────┘
           │ HTTP POST
           ↓
┌─────────────────────────────┐
│  Render Web Service (FREE)  │ ← Your app running
│  /trigger-news endpoint     │
└──────────┬──────────────────┘
           │ Uses API keys
           ├─→ OpenAI API (summarize)
           ├─→ NewsAPI (fetch)
           └─→ Gmail SMTP (email)
                   ↓
           ┌──────────────────┐
           │  Your Inbox 📧   │
           └──────────────────┘
```

---

## ✅ FINAL VERIFICATION CHECKLIST

### Web Service Setup
- [ ] Render Web Service created
- [ ] All 8 environment variables added
- [ ] Status shows "Deployed"
- [ ] Service URL obtained

### Endpoint Testing
- [ ] Health check works: `GET /`
- [ ] Trigger works: `POST /trigger-news`
- [ ] Email received in inbox

### Scheduler Setup (Choose One)
- [ ] **GitHub Actions** configured, OR
- [ ] **EasyCron** configured, OR
- [ ] **CRON-job.org** configured

### Daily Automation
- [ ] Scheduler set to 10 PM UTC
- [ ] Can view scheduler status
- [ ] Email received in inbox from scheduler

---

## 🆘 TROUBLESHOOTING

### Issue: Service goes to sleep

**Why:** Render's free tier puts services to sleep after 15 minutes of inactivity.

**Solution:** The scheduler pings the service at 10 PM, waking it up automatically. No action needed!

### Issue: Endpoint returns 404

**Cause:** Service URL is wrong, or service not deployed.

**Solution:**
1. Check Render dashboard for service URL
2. Make sure it's fully deployed (not building)
3. Test health check first: `GET /`

### Issue: Cron doesn't trigger

**Cause:** Wrong service URL or scheduler not active.

**Solution:**
1. Verify URL is correct in scheduler
2. Check scheduler is active/enabled
3. View scheduler logs/history
4. Test manual trigger in Render logs

### Issue: Email not received

**Solution:**
1. Check email address in `.env`
2. Verify app password is correct
3. Manually trigger: `POST /trigger-news`
4. Check `/logs` endpoint for errors

### Issue: "Can't find module Flask"

**Cause:** requirements.txt not updated.

**Solution:**
```bash
# Locally test
pip install flask
pip install -r requirements.txt
python app/main.py --run-once
```

---

## 📈 COST BREAKDOWN (FREE TIER)

| Service | Cost | Notes |
|---------|------|-------|
| Render Web Service | **$0** | Free tier ✅ |
| GitHub Actions | **$0** | Free for public repos ✅ |
| OpenAI API | Variable | Pay as you use (~$0.50/month) |
| NewsAPI | **$0** | Free tier (100/day) |
| Gmail SMTP | **$0** | Gmail app password |
| **TOTAL** | **~$0.50/month** | Almost free! |

---

## 🔧 ADVANCED: Monitor Service Health

### Add Monitoring (Optional)

GitHub Actions can also check if service is healthy:

```yaml
name: Monitor Service Health

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - name: Check Service Health
        run: |
          STATUS=$(curl -s https://your-service-url.onrender.com/ | grep -o '"status":"[^"]*"')
          if [ -z "$STATUS" ]; then
            echo "❌ Service unhealthy!"
            exit 1
          else
            echo "✅ Service healthy: $STATUS"
          fi
```

---

## 🎯 YOUR DEPLOYMENT IS COMPLETE

### What You Have
- ✅ **Free Web Service** running on Render
- ✅ **HTTP Endpoint** that can be triggered
- ✅ **Automatic Daily Trigger** via GitHub Actions (or EasyCron)
- ✅ **Zero Maintenance** - Everything automated

### What Happens Daily
1. **10:00 PM UTC** → GitHub Actions triggers
2. **HTTP POST** sent to your endpoint
3. **Web Service** wakes up and processes
4. **News fetched** from NewsAPI
5. **Articles summarized** with OpenAI
6. **Email sent** to your inbox
7. **Service sleeps** until next trigger

---

## 📞 HELP & SUPPORT

- **Render Issues** → https://render.com/support
- **GitHub Actions Help** → https://docs.github.com/en/actions
- **EasyCron Help** → https://www.easycron.com/?aid=github
- **Your App Issues** → Check logs in Render dashboard

---

## 🚀 YOU'RE ALL SET!

Your **free tier deployment** is now complete. Emails will arrive automatically every day at 10:00 PM UTC.

**No credit card. No paid plans. Just free cloud automation! 🎉**

---

**Next Steps:**
1. If using GitHub Actions → Commit the workflow file
2. If using EasyCron → Verify scheduler is active
3. Wait for next scheduled time to confirm auto-trigger works
4. Done! 🎊

