# Render Deployment Guide

Complete step-by-step guide to deploy the Daily AI News application on Render.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Render Account Setup](#render-account-setup)
4. [GitHub Repository Setup](#github-repository-setup)
5. [Deployment Steps](#deployment-steps)
6. [Environment Variables Configuration](#environment-variables-configuration)
7. [Verify Deployment](#verify-deployment)
8. [Monitoring & Logs](#monitoring--logs)
9. [Troubleshooting](#troubleshooting)

---

## Overview

This guide covers deploying the Daily AI News automation agent to Render, a modern cloud platform that supports:
- ✅ Cron jobs (scheduled tasks)
- ✅ Background workers
- ✅ Free tier available
- ✅ Zero-configuration deployment
- ✅ GitHub integration

**Deployment Type:** Cron Job (runs once daily at 10:00 PM UTC)

---

## Prerequisites

Before you start, ensure you have:

1. **Render Account** - Sign up at [render.com](https://render.com)
2. **GitHub Account** - For repository hosting
3. **API Keys**:
   - OpenAI API key
   - NewsAPI key
   - Gmail app password (for SMTP)
4. **Git** installed on your local machine

---

## Render Account Setup

### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Click **Sign Up**
3. Choose **Sign up with GitHub** (recommended)
4. Authorize Render to access your GitHub account
5. Complete profile setup

### Step 2: Get Render API Key

1. Log in to Render dashboard
2. Go to **Account Settings** → **API Keys**
3. Click **Create API Key**
4. Copy and save it securely
5. You'll use this for authentication if needed

---

## GitHub Repository Setup

### Step 1: Push Project to GitHub

If you haven't already, initialize and push your project:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Daily AI news automation agent"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/daily-ai-news.git
git branch -M main
git push -u origin main
```

### Step 2: Verify .gitignore

Ensure `.gitignore` includes:
```
.env
.env.local
logs/
__pycache__/
*.pyc
venv/
```

**Important:** Never commit `.env` with real API keys!

---

## Deployment Steps

### Step 1: Connect GitHub Repository

1. Log in to [Render Dashboard](https://dashboard.render.com)
2. Click **+ New** → **Cron Job**
3. Click **Connect Repository**
4. Search for your **daily-ai-news** repository
5. Click **Connect**

### Step 2: Configure Cron Job

**Basic Settings:**

```
Name: daily-ai-news
Language: Python
Region: Your closest region
```

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
python app/main.py --run-once
```

**Schedule:**
```
0 22 * * *  # Every day at 10:00 PM UTC
```

Or use cron presets (recommended):
- **Daily** - Runs once per day
- **Timezone:** UTC (convert to your preference)

### Step 3: Add Environment Variables

Click **Environment** section and add:

| Key | Value | Notes |
|-----|-------|-------|
| `OPENAI_API_KEY` | `sk-...` | Your OpenAI API key |
| `NEWSAPI_KEY` | `...` | Your NewsAPI key |
| `EMAIL_SENDER` | `your@gmail.com` | Gmail address |
| `EMAIL_PASSWORD` | `xxxx xxxx xxxx xxxx` | 16-char Gmail app password |
| `EMAIL_RECIPIENT` | `recipient@example.com` | Who receives the email |
| `SMTP_SERVER` | `smtp.gmail.com` | (Default) |
| `SMTP_PORT` | `587` | (Default) |
| `SCHEDULE_TIME` | `22:00` | (Default) |

**How to get Gmail App Password:**
1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Windows Computer"
3. Copy the 16-character password
4. Paste in Render

### Step 4: Deploy

1. Click **Create Cron Job**
2. Render starts building automatically
3. Wait for build to complete (2-3 minutes)
4. You'll see **Deployed** status

---

## Environment Variables Configuration

### Setting Variables in Render

**Method 1: Dashboard (Easy)**
1. Go to your cron job
2. Click **Environment** tab
3. Click **Add Environment Variable**
4. Enter `Key` and `Value`
5. Click **Save**

**Method 2: From Render CLI**
```bash
# Install Render CLI (optional)
npm install -g @render-oss/cli

# Login
render login

# Add variables
render env set OPENAI_API_KEY sk-your-key-here
render env set NEWSAPI_KEY your-newsapi-key
```

### Required Variables

```env
OPENAI_API_KEY=sk-proj-xxxxxx...        # OpenAI API key
NEWSAPI_KEY=0fa5a91c...                 # NewsAPI key
EMAIL_SENDER=your@gmail.com             # Gmail address
EMAIL_PASSWORD=jjku qcob ujnk wabc      # Gmail app password (16 chars)
EMAIL_RECIPIENT=recipient@example.com   # Where to send emails
SMTP_SERVER=smtp.gmail.com              # Gmail SMTP (default)
SMTP_PORT=587                           # SMTP port (default)
SCHEDULE_TIME=22:00                     # 24-hour format
```

---

## Verify Deployment

### Step 1: Check Deployment Status

1. Go to Render dashboard
2. Click your **daily-ai-news** cron job
3. Check status:
   - 🟢 **Running** = Deployed successfully
   - 🔴 **Failed** = Check logs for errors

### Step 2: Run Manual Test

1. Click **Trigger Job** button
2. Wait for execution
3. Check **Event Logs** for output
4. Verify email was received (check inbox and spam folder)

### Step 3: Check Logs

In Render dashboard:
1. Click **daily-ai-news** cron job
2. Click **Logs** tab
3. View real-time logs as job executes

You should see:
```
==================================================
Starting daily news update process...
==================================================
Step 1: Fetching news...
Fetched 5 AI news and 5 world news
Step 2: Summarizing articles...
Articles summarized
Step 3: Sending email...
✓ Daily news email sent successfully
==================================================
Daily news update completed successfully
==================================================
```

---

## Monitoring & Logs

### View Execution History

**In Render Dashboard:**
1. Click your cron job
2. Click **Events** tab
3. See all past job executions
4. Click any event to view logs

### Enable Email Alerts (Optional)

1. Click your cron job
2. Go to **Settings**
3. Enable **Email on failure**
4. You'll receive alerts if the job fails

### Monitoring Checklist

- ✅ Job runs at scheduled time
- ✅ Check logs for errors
- ✅ Verify email received
- ✅ Check spam/promotions folder
- ✅ Monitor API quota usage

---

## Scheduling Times

Render uses **UTC timezone** by default.

**Convert to your timezone:**

| Your Timezone | Render Time | Cron Expression |
|---------------|-------------|-----------------|
| EST (UTC-5) | 3:00 AM | 0 3 * * * |
| CST (UTC-6) | 2:00 AM | 0 2 * * * |
| PST (UTC-8) | 12:00 AM | 0 0 * * * |
| IST (UTC+5:30) | 4:30 PM | 30 16 * * * |
| GMT (UTC+0) | 10:00 PM | 0 22 * * * |

To change schedule:
1. Click your cron job
2. Click **Settings**
3. Modify **Schedule**
4. Click **Save**

---

## Troubleshooting

### Problem: "Build Failed"

**Check Error:**
1. Click **Builds** tab
2. View error message

**Common Issues:**
- Missing dependencies → Check `requirements.txt`
- Python version mismatch → Render uses Python 3.11
- File not found → Check file paths

**Solution:**
```bash
# Locally test build
pip install -r requirements.txt
python app/main.py --run-once
```

### Problem: "Job Failed" or "Job Didn't Run"

**Check:**
1. View **Event Logs**
2. Look for error messages
3. Check environment variables

**Common Issues:**
- Missing API keys → Add to Environment
- Invalid Gmail password → Regenerate app password
- Email config issues → Check SMTP settings

### Problem: "Email Not Received"

**Checklist:**
- [ ] Check spam/promotions folder
- [ ] Verify `EMAIL_RECIPIENT` is correct
- [ ] Check Gmail allows less secure apps (if not using app password)
- [ ] Verify `EMAIL_PASSWORD` is the 16-char app password, not regular password
- [ ] Check `SMTP_SERVER=smtp.gmail.com` and `SMTP_PORT=587`

**Test Locally:**
```bash
python app/main.py --run-once
```

### Problem: "API Rate Limited"

**If OpenAI rate limit:**
- Uses fallback descriptions automatically
- No action needed, job continues

**If NewsAPI quota exceeded:**
- Free tier: 100 requests/day
- Wait until tomorrow (quota resets)
- Upgrade to paid plan for more requests

### Problem: "Build Timeout"

This shouldn't happen, but if it does:
1. Try triggering the job again
2. Check if dependencies are too heavy
3. Contact Render support

---

## Advanced Configuration

### Use Custom Domain Email

If using custom domain:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_SENDER=noreply@yourdomain.com
EMAIL_PASSWORD=your-app-password
```

### Change Execution Schedule

**Every 6 hours:**
```
0 */6 * * *
```

**Every Monday at 9 AM:**
```
0 9 * * 1
```

**Twice daily (10 AM & 10 PM):**
```
0 10,22 * * *
```

### Increase Timeout (if needed)

By default, Render gives 30 minutes. If job takes longer, contact support for custom timeout.

---

## Cost Breakdown

**Render Pricing for This Project:**

| Component | Cost | Notes |
|-----------|------|-------|
| Cron Job | Free | Runs once daily |
| Storage | Free | Minimal logs |
| Bandwidth | Free | Email traffic only |
| **Total** | **$0** | ✅ Free tier |

---

## Deployment Checklist

Before deploying, confirm:

- [ ] GitHub account created
- [ ] Project pushed to GitHub
- [ ] `.env` added to `.gitignore`
- [ ] `.env.example` has all variables
- [ ] OpenAI API key obtained
- [ ] NewsAPI key obtained
- [ ] Gmail app password generated
- [ ] Render account created
- [ ] All environment variables added to Render
- [ ] Cron job created
- [ ] Test job triggered manually
- [ ] Email received successfully
- [ ] Logs show no errors

---

## After Deployment

### Monitor Regularly

1. **Weekly:** Check execution logs
2. **Monthly:** Verify email quality
3. **Quarterly:** Check API quota usage

### Update Code on Render

When you update code in GitHub:
1. Git push to `main` branch
2. Render auto-redeploys (takes 2-3 minutes)
3. No manual action needed

### Update Environment Variables

1. Click your cron job
2. Click **Environment**
3. Edit variable
4. Click **Save**
5. No redeployment needed

---

## Need Help?

### Resources

- [Render Docs](https://render.com/docs)
- [Render Cron Jobs Guide](https://render.com/docs/cronjobs)
- [Render Support](https://render.com/support)

### Common Questions

**Q: Can I change the schedule after deployment?**
A: Yes, go to Settings and edit the cron expression.

**Q: What if the job fails?**
A: Check logs in the Render dashboard. You'll also get email alerts if enabled.

**Q: How do I see if the email was sent?**
A: Check the execution logs and verify email in your inbox.

**Q: Can I run it more frequently than daily?**
A: Yes, modify the cron expression (e.g., `0 */12 * * *` for twice daily).

**Q: Is my API key secure?**
A: Yes, Render encrypts environment variables and doesn't expose them in logs.

---

**🚀 Your Daily AI News automation is now live on Render!**

For any issues, check the [Troubleshooting](#troubleshooting) section or review the logs in your Render dashboard.
