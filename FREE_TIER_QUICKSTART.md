# 🎉 RENDER FREE TIER - 30 MINUTE SETUP

**Deploy Daily AI News on Render's FREE tier in 30 minutes!**

---

## ⚡ The Quick Version

### What Changed?
- ❌ **Cron Job** (PAID) → ✅ **Web Service** (FREE)  
- ❌ Built-in scheduling → ✅ External scheduler (GitHub Actions, FREE)

### Total Cost
- $0/month (completely free!)

---

## 🚀 Quick Setup (Copy-Paste)

### 1. Install Latest Dependencies (5 min)

```bash
cd "d:\daily AI news"
pip install -r requirements.txt
```

### 2. Test Locally (5 min)

```bash
# Test news update
python app/main.py --run-once

# Should receive email ✅
```

### 3. Deploy on Render (10 min)

```
1. Go to: https://dashboard.render.com
2. Click: + New → Web Service (NOT Cron Job!)
3. Connect: daily-ai-news repository
4. Configure:
   Name: daily-ai-news
   Language: Python 3
   Plan: Free ✅
   
   Build Command: pip install -r requirements.txt
   Start Command: python app/main.py
   
5. Add Environment Variables (same 8 as before):
   - OPENAI_API_KEY
   - NEWSAPI_KEY
   - EMAIL_SENDER
   - EMAIL_PASSWORD
   - EMAIL_RECIPIENT
   - SMTP_SERVER
   - SMTP_PORT
   - SCHEDULE_TIME

6. Click: Create Web Service
7. Wait for build (2-3 min) → Status: Deployed ✅
```

### 4. Get Your Service URL (1 min)

Once deployed, Render shows you the URL:
```
https://daily-ai-news.onrender.com
```

**Save this URL! You'll need it next.**

### 5. Set Up Automatic Trigger (10 min)

Choose ONE option:

#### Option A: GitHub Actions (Easiest & FREE)

```bash
# In your project root
mkdir -p .github/workflows
```

Create file: `.github/workflows/daily-news.yml`

```yaml
name: Daily AI News Trigger
on:
  schedule:
    - cron: '0 22 * * *'
  workflow_dispatch:
jobs:
  trigger:
    runs-on: ubuntu-latest
    steps:
      - run: curl -X POST https://YOUR-SERVICE-URL.onrender.com/trigger-news
```

Replace `YOUR-SERVICE-URL` with your Render URL!

```bash
git add .github/workflows/daily-news.yml
git commit -m "Add auto-trigger"
git push
```

Done! ✅ GitHub Actions will trigger at 10 PM UTC daily.

#### Option B: EasyCron (If not using GitHub)

```
1. Go to: https://www.easycron.com
2. Sign up (free, no credit card)
3. Create cron job:
   URL: https://YOUR-SERVICE-URL.onrender.com/trigger-news
   Method: POST
   Schedule: 0 22 * * * (10 PM UTC)
4. Save ✅
```

---

## ✅ VERIFICATION

### Test Web Service

Open in browser:
```
https://YOUR-SERVICE-URL.onrender.com/
```

Should show:
```json
{"status": "healthy", "service": "Daily AI News Automation"}
```

### Test Trigger

Using curl or Postman:
```bash
curl -X POST https://YOUR-SERVICE-URL.onrender.com/trigger-news
```

Should return:
```json
{"status": "success", "message": "News email sent successfully"}
```

### Check Email

After triggering, you should receive "Daily AI & World News" email in 10-15 seconds. ✅

---

## 📅 What Happens Each Day

```
10:00 PM UTC
    ↓
GitHub Actions (or EasyCron) triggers
    ↓
Sends HTTP request to your Render URL
    ↓
Web Service processes news
    ↓
Summarizes with OpenAI
    ↓
Sends email 📧
    ↓
Done! Service sleeps
```

**Zero intervention needed!** 🤖

---

## 🔧 Timezone Adjustment

Edit `SCHEDULE_TIME` in `.env` if needed:

```env
SCHEDULE_TIME=22:00  # 10 PM UTC
SCHEDULE_TIME=14:00  # 2 PM UTC
SCHEDULE_TIME=03:00  # 3 AM UTC
```

Change cron expression if using EasyCron:
```
0 22 * * * = 10 PM UTC
0 14 * * * = 2 PM UTC (8 AM EST)
0 3 * * *  = 3 AM UTC (10 PM EST)
```

---

## 🎯 Quick Reference

| What | Where | Status |
|------|-------|--------|
| Web Service | Render Dashboard | ✅ Deployed (Free) |
| HTTP Endpoint | `/trigger-news` | ✅ Active |
| Scheduler | GitHub Actions | ✅ Running |
| Email Sending | Gmail SMTP | ✅ Configured |
| Cost | - | ✅ $0 |

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Service URL not showing | Wait, Render is still building |
| Health check fails | Check service hasn't crashed, view logs |
| No email received | Manually trigger endpoint, check logs |
| GitHub didn't run | Check GitHub Actions tab in repo |
| Too expensive | You're using free tier! Cost is ~$0 |

---

## 📞 Need Detailed Help?

Read the full guide: [RENDER_FREE_TIER_GUIDE.md](RENDER_FREE_TIER_GUIDE.md)

Contains:
- ✅ Complete setup instructions
- ✅ All 3 scheduler options
- ✅ Architecture explanation
- ✅ Detailed troubleshooting
- ✅ Monitoring setup

---

## 🎉 SUMMARY

✅ **Deployed on Render's FREE tier**  
✅ **Automatic daily trigger via GitHub Actions**  
✅ **Email arrives at 10 PM UTC automatically**  
✅ **No cost at all**  
✅ **Fully automated & zero maintenance**  

**Your Daily AI News automation is LIVE!** 🚀

---

**Time Invested: ~30 minutes**  
**Cost: $0**  
**Value: Priceless** 😄

