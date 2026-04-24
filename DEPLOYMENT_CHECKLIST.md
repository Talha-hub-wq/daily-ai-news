# Complete Render Deployment Checklist

Use this checklist to ensure everything is ready before deploying to Render.

---

## ✅ PRE-DEPLOYMENT CHECKLIST

### API Keys & Credentials Ready
- [ ] **OpenAI API Key** obtained from [platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
  - Format: `sk-proj-xxxxx...`
  - [ ] Test key works locally
- [ ] **NewsAPI Key** obtained from [newsapi.org](https://newsapi.org)
  - [ ] Free tier account created
  - [ ] Quota available (100 requests/day)
- [ ] **Gmail Account** ready for SMTP
  - [ ] 2-Step Verification enabled
  - [ ] App Password generated ([myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords))
  - [ ] App Password format: `xxxx xxxx xxxx xxxx` (16 chars with spaces)
  - [ ] Email recipient confirmed

### Project Files Ready
- [ ] `app/main.py` - Entry point ✓
- [ ] `app/news_fetcher.py` - News fetching ✓
- [ ] `app/summarizer.py` - OpenAI summarization ✓
- [ ] `app/email_sender.py` - Email sending ✓
- [ ] `app/scheduler.py` - Scheduling ✓
- [ ] `config/settings.py` - Configuration ✓
- [ ] `templates/email_template.html` - Email template ✓
- [ ] `requirements.txt` - Dependencies ✓
- [ ] `README.md` - Documentation ✓
- [ ] `.env.example` - Variable template ✓
- [ ] `.gitignore` - Git ignore rules ✓
- [ ] `Procfile` - Process definition ✓
- [ ] `render.yaml` - Render config ✓
- [ ] `runtime.txt` - Python version ✓

### Code Tested Locally
- [ ] Run `python app/main.py --run-once` successfully
- [ ] Check `logs/app.log` for errors
- [ ] Verify email received in inbox
- [ ] No errors in output

### Git & GitHub Ready
- [ ] GitHub account created
- [ ] Repository created on GitHub
- [ ] Project pushed to GitHub
  - [ ] Command: `git push -u origin main`
  - [ ] Files visible on GitHub website
- [ ] `.env` NOT on GitHub (check .gitignore)
- [ ] `.env.example` on GitHub (without real values)
- [ ] All code committed and pushed
  - [ ] Command: `git log --oneline` shows commits
  - [ ] GitHub shows latest commits

### Render Account Ready
- [ ] Render account created at [render.com](https://render.com)
- [ ] Connected GitHub account to Render
  - [ ] Settings → Integrations → GitHub authorized
  - [ ] Render can access your repositories

---

## 🚀 DEPLOYMENT STEPS

### Step 1: Create Cron Job on Render
- [ ] Log in to [Render Dashboard](https://dashboard.render.com)
- [ ] Click **+ New** → **Cron Job**
- [ ] Click **Connect Repository**
- [ ] Select **daily-ai-news** repository
- [ ] Click **Connect**

### Step 2: Configure Basic Settings
| Setting | Value |
|---------|-------|
| Name | `daily-ai-news` |
| Language | `Python 3` |
| Region | Closest to you |
| Plan | `Free` |

- [ ] Name set to `daily-ai-news`
- [ ] Language is `Python 3`
- [ ] Plan is `Free`

### Step 3: Configure Build & Start Commands
- [ ] **Build Command:** `pip install -r requirements.txt`
  - Verify exactly as shown
- [ ] **Start Command:** `python app/main.py --run-once`
  - Verify exactly as shown

### Step 4: Set Schedule
- [ ] **Schedule:** `0 22 * * *` (10 PM UTC)
  - Or adjust to your timezone using the reference below:
  - EST: `0 3 * * *`
  - CST: `0 2 * * *`
  - PST: `0 0 * * *`
  - IST: `30 16 * * *`

### Step 5: Add Environment Variables

**Open Environment Section:**
- [ ] Click **Environment** tab
- [ ] Click **Add Environment Variable**

**Add Each Variable:**

| Variable | Value | Required | Notes |
|----------|-------|----------|-------|
| OPENAI_API_KEY | `sk-proj-...` | ✅ | From OpenAI dashboard |
| NEWSAPI_KEY | `your-key` | ✅ | From NewsAPI |
| EMAIL_SENDER | `your@gmail.com` | ✅ | Gmail address |
| EMAIL_PASSWORD | `xxxx xxxx xxxx xxxx` | ✅ | 16-char app password |
| EMAIL_RECIPIENT | `recipient@example.com` | ✅ | Where to send emails |
| SMTP_SERVER | `smtp.gmail.com` | ✅ | Default for Gmail |
| SMTP_PORT | `587` | ✅ | Default for Gmail |
| SCHEDULE_TIME | `22:00` | ✅ | 24-hour format |

**Checklist for Variables:**
- [ ] OPENAI_API_KEY added
- [ ] NEWSAPI_KEY added
- [ ] EMAIL_SENDER added
- [ ] EMAIL_PASSWORD added (16-char app password)
- [ ] EMAIL_RECIPIENT added
- [ ] SMTP_SERVER added
- [ ] SMTP_PORT added
- [ ] SCHEDULE_TIME added (format: HH:MM)
- [ ] All 8 variables visible in Environment tab
- [ ] Each variable has correct value

### Step 6: Deploy
- [ ] Click **Create Cron Job** button
- [ ] Wait for build to complete (2-3 minutes)
  - Status changes from "Building..." to "Available"
- [ ] Check **Build Status** is green (✓ Deployed)

---

## ✅ POST-DEPLOYMENT VERIFICATION

### Verify Deployment Success
- [ ] Cron job created successfully
- [ ] Status shows "Available" (green)
- [ ] No error messages in Build Logs

### Test Job Manually
1. [ ] Click **Trigger Job** button
2. [ ] Wait for execution (~30 seconds)
3. [ ] Check **Event Logs** tab
   - Should show: "Successfully triggered job"
4. [ ] View logs for output:
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

### Verify Email Received
- [ ] Check inbox for "Daily AI & World News" email
- [ ] Check spam/promotions folder
- [ ] Email contains:
  - [ ] Top 5 AI news
  - [ ] Top 5 world news
  - [ ] Article titles, summaries, sources
  - [ ] Read full article links

### Check Logs for Errors
- [ ] Go to **Logs** tab in Render
- [ ] No error messages
- [ ] No API failures
- [ ] No SMTP errors

---

## 🔧 CONFIGURATION REFERENCE

### Timezone Conversion (UTC)

If you want emails at specific local time:

**Your Local Time → Render UTC Time**

| Your Timezone | Your Time | Render Time | Cron |
|---------------|-----------|-------------|------|
| PST (UTC-8) | 2:00 PM | 10:00 PM | 0 22 * * * |
| MST (UTC-7) | 3:00 PM | 10:00 PM | 0 22 * * * |
| CST (UTC-6) | 4:00 PM | 10:00 PM | 0 22 * * * |
| EST (UTC-5) | 5:00 PM | 10:00 PM | 0 22 * * * |
| GMT (UTC+0) | 10:00 PM | 10:00 PM | 0 22 * * * |
| CET (UTC+1) | 11:00 PM | 10:00 PM | 0 22 * * * |
| IST (UTC+5:30) | 3:30 AM | 10:00 PM | 0 22 * * * |
| SGT (UTC+8) | 6:00 AM | 10:00 PM | 0 22 * * * |
| AEST (UTC+10) | 8:00 AM | 10:00 PM | 0 22 * * * |

**To Change:**
1. Go to your cron job
2. Click **Settings**
3. Change **Schedule** cron expression
4. Click **Save**

### Email Providers (Alternative to Gmail)

**Outlook:**
```
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
```

**Yahoo:**
```
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

**Custom Domain (with Gmail):**
```
EMAIL_SENDER=noreply@yourdomain.com
SMTP_SERVER=smtp.gmail.com
```

---

## 🆘 TROUBLESHOOTING

### Issue: Build Failed
**What to check:**
- [ ] Click **Builds** tab
- [ ] Read error message carefully
- [ ] Common causes:
  - Missing dependency in `requirements.txt`
  - Python syntax error in code
  - File not found (check file paths)

**Solution:**
```bash
# Test locally
python -m pip install --upgrade pip
pip install -r requirements.txt
python app/main.py --run-once
```

### Issue: Job Didn't Run
**What to check:**
- [ ] Check time zone conversion correct
- [ ] View **Events** tab in Render
- [ ] Look for scheduled job entry

**Solution:**
- [ ] Trigger job manually to test
- [ ] Check if API keys are valid

### Issue: Email Not Received

| Check | Solution |
|-------|----------|
| Check spam folder | Sometimes Gmail filters it |
| Wrong EMAIL_RECIPIENT | Edit environment variable in Render |
| Wrong EMAIL_PASSWORD | Use 16-char app password, not regular password |
| Wrong SMTP settings | Should be `smtp.gmail.com:587` |
| Gmail security | May need to enable less secure apps |

**Test Email Sending Locally:**
```bash
python app/main.py --run-once
```

### Issue: API Rate Limited
**If OpenAI rate limited:**
- System automatically uses fallback descriptions
- Job completes successfully
- No action needed

**If NewsAPI quota exceeded:**
- Free tier: 100 requests/day
- Wait until tomorrow (quota resets)
- Or upgrade to paid plan

### Issue: Missing Environment Variables
**Error in logs:**
```
Missing required environment variables: OPENAI_API_KEY, ...
```

**Solution:**
1. Go to your cron job in Render
2. Click **Environment** tab
3. Add missing variables
4. Click Save
5. Trigger job again

---

## 📊 MONITORING & MAINTENANCE

### Daily Check
- [ ] Check inbox for that day's email
- [ ] Verify email content looks correct

### Weekly Check
- [ ] View **Events** in Render dashboard
- [ ] All jobs completed successfully
- [ ] No errors in logs

### Monthly Check
- [ ] Check API usage (NewsAPI quota)
- [ ] Verify OpenAI charges (if applicable)
- [ ] Test manual trigger to ensure still working

### Update Code
When you update code on GitHub:
1. Make changes locally
2. Test with `python app/main.py --run-once`
3. Commit: `git commit -m "Description"`
4. Push: `git push`
5. Render auto-redeploys (2-3 min)
6. No manual action needed in Render

---

## 🎉 SUCCESS!

If all checkboxes above are complete:

- ✅ Project deployed on Render
- ✅ Cron job running automatically
- ✅ Emails received daily at 10 PM
- ✅ System monitoring active
- ✅ Zero manual intervention

**Your Daily AI News automation is live! 🚀**

---

## 📞 GET HELP

If something goes wrong:

1. **Check Logs First**
   - Render Dashboard → Your Cron Job → Logs
   - Detailed error message usually shown

2. **Review This Checklist**
   - Find your issue in Troubleshooting section

3. **Test Locally**
   ```bash
   python app/main.py --run-once
   ```

4. **Render Support**
   - [render.com/support](https://render.com/support)
   - Response usually within hours

5. **GitHub Issues**
   - [Create issue](https://github.com/YOUR_USERNAME/daily-ai-news/issues)
   - Document the problem with logs

---

**Keep this checklist handy for future reference!**
