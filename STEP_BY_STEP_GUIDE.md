# Step-by-Step Render Deployment Visual Guide

Complete visual walkthrough with detailed instructions for each step.

---

## 📋 Overview

This guide shows exactly what you'll see and click at each stage of deploying to Render.

---

## PART 1: GitHub Setup (5 minutes)

### Step 1.1: Create GitHub Repository

**1. Go to GitHub:**
- URL: https://github.com
- Click **Sign in** (or Sign up if new user)

**2. Create New Repository:**
- Click **+** icon (top right)
- Select **New repository**

**3. Fill Repository Form:**
```
Repository name:        daily-ai-news
Description:           Automated daily AI & world news email updates
Visibility:            ⚪ Public
Initialize:            ☐ Add .gitignore
                       ☐ Add license
```

- Click **Create repository**

**4. Copy Repository URL:**
- You'll see a button that says "Code" (green button)
- Copy the HTTPS URL: `https://github.com/YOUR_USERNAME/daily-ai-news.git`
- Save this for later

---

### Step 1.2: Push Project to GitHub

**1. Open Terminal/PowerShell:**
- Windows: Press `Win + R`, type `powershell`, press Enter
- Mac: Press `Cmd + Space`, type `terminal`, press Enter

**2. Navigate to Project:**
```bash
cd "D:\daily AI news"
```

**3. Initialize Git (one time only):**
```bash
git init
git config --global user.name "Your Name"
git config --global user.email "your-github-email@example.com"
```

**4. Stage All Files:**
```bash
git add .
```

**5. Create First Commit:**
```bash
git commit -m "Initial commit: Daily AI news automation agent"
```

**6. Add Remote & Push:**
```bash
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/daily-ai-news.git
git branch -M main
git push -u origin main
```

**7. Authenticate:**
- If prompted for password, use GitHub Personal Access Token:
  - Go to: https://github.com/settings/tokens
  - Click **Generate new token (classic)**
  - Check `repo` scope
  - Copy token
  - Paste as password in terminal

**8. Verify on GitHub:**
- Go to your GitHub repository
- Should see all files displayed

---

## PART 2: Prepare API Keys & Credentials (10 minutes)

### Step 2.1: Get OpenAI API Key

**1. Go to OpenAI:**
- URL: https://platform.openai.com/account/api-keys
- Sign in (or create account)

**2. Create API Key:**
- Click **Create new secret key**
- Name: `Render Deployment`
- Copy the key (shows only once!)
- Format looks like: `sk-proj-xxxxx...`
- **Save this safely** (you'll need it in 10 minutes)

---

### Step 2.2: Get NewsAPI Key

**1. Go to NewsAPI:**
- URL: https://newsapi.org
- Click **Get API Key**

**2. Create Account:**
- Enter email
- Create password
- Choose "Free" plan
- Copy your API key
- **Save this safely**

---

### Step 2.3: Get Gmail App Password

**1. Go to Gmail Account:**
- URL: https://myaccount.google.com/apppasswords
- Sign in with your Gmail

**2. Select App & Device:**
- App: **Mail**
- Device: **Windows Computer** (or your OS)

**3. Get App Password:**
- Click **Generate**
- Gmail shows 16-character password with spaces
- Format: `xxxx xxxx xxxx xxxx`
- **Copy this password**
- Save it safely

**Important:** This is NOT your regular Gmail password!

---

## PART 3: Render Deployment (15 minutes)

### Step 3.1: Render Account Setup

**1. Sign Up for Render:**
- URL: https://render.com
- Click **Sign Up**
- Option A: **Sign up with GitHub** (easiest!)
  - Click button
  - Authorize Render to access GitHub
- Option B: Email signup
  - Enter email and password

**2. Create Account:**
- Complete any profile prompts
- Confirm email if needed

**3. Go to Render Dashboard:**
- URL: https://dashboard.render.com
- You should see empty dashboard with **+ New** button

---

### Step 3.2: Connect GitHub (If You Haven't)

**1. In Render Dashboard:**
- Click your name (top right) → **Account**
- Go to **Integrations** tab
- Find **GitHub**
- Click **Connect** (if not already connected)

**2. Authorize:**
- GitHub page opens
- Click **Authorize render**
- You're done!

---

### Step 3.3: Create Cron Job

**1. In Render Dashboard:**
- Click **+ New** button (top right)
- Select **Cron Job**

**2. Connect Repository:**
- Click **Connect Repository**
- Find and click **daily-ai-news** repository
- Click **Connect**

---

### Step 3.4: Configure Basic Settings

**You're now in the cron job configuration page:**

Fill in these fields:

| Field | Value |
|-------|-------|
| Name | `daily-ai-news` |
| Language | `Python 3` |
| Region | Closest to you (e.g., us-east-1) |
| Plan | `Free` |

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
python app/main.py --run-once
```

---

### Step 3.5: Set Schedule

**Schedule (Cron Expression):**

Choose based on your timezone:

| Your Timezone | Time | Cron Expression |
|---------------|------|-----------------|
| PST (UTC-8) | 2:00 PM | `0 14 * * *` |
| MST (UTC-7) | 3:00 PM | `0 15 * * *` |
| CST (UTC-6) | 4:00 PM | `0 16 * * *` |
| EST (UTC-5) | 5:00 PM | `0 17 * * *` |
| GMT (UTC+0) | 10:00 PM | `0 22 * * *` |
| CET (UTC+1) | 11:00 PM | `0 23 * * *` |
| IST (UTC+5:30) | 3:30 AM | `30 3 * * *` |

Default is 10 PM UTC: `0 22 * * *`

---

### Step 3.6: Add Environment Variables

**1. Click Environment Section:**
- Scroll down or find "Environment" tab
- Click **Add Environment Variable**

**2. Add Each Variable (8 total):**

Click **Add Environment Variable** and fill in:

**Variable 1:**
```
Key:    OPENAI_API_KEY
Value:  sk-proj-xxxxx...  (your OpenAI key)
```
Click ✓

**Variable 2:**
```
Key:    NEWSAPI_KEY
Value:  0fa5a91c... (your NewsAPI key)
```
Click ✓

**Variable 3:**
```
Key:    EMAIL_SENDER
Value:  your-email@gmail.com
```
Click ✓

**Variable 4:**
```
Key:    EMAIL_PASSWORD
Value:  xxxx xxxx xxxx xxxx  (16-char app password)
```
Click ✓

**Variable 5:**
```
Key:    EMAIL_RECIPIENT
Value:  recipient@example.com  (where you want emails sent)
```
Click ✓

**Variable 6:**
```
Key:    SMTP_SERVER
Value:  smtp.gmail.com
```
Click ✓

**Variable 7:**
```
Key:    SMTP_PORT
Value:  587
```
Click ✓

**Variable 8:**
```
Key:    SCHEDULE_TIME
Value:  22:00
```
Click ✓

**Verify:** All 8 variables should be listed in the Environment section.

---

### Step 3.7: Deploy!

**1. Click Create Cron Job:**
- Scroll down
- Click blue **Create Cron Job** button
- You'll see "Building..." message

**2. Wait for Build:**
- Takes 2-3 minutes
- You'll see progress in the Build Logs
- Wait until status says **"Deployed"**

**3. View Build Logs:**
- Click **Builds** tab
- Should see green checkmark (✓)
- No error messages

---

## PART 4: Test & Verify (5 minutes)

### Step 4.1: Test Job Manually

**1. In Your Cron Job Page:**
- Look for **Trigger Job** button (or **Manual Trigger**)
- Click it

**2. Watch Execution:**
- Click **Events** or **Logs** tab
- Wait ~30 seconds for execution
- Should see success message

**3. Check Logs Output:**
- Should see lines like:
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
```

---

### Step 4.2: Verify Email Received

**1. Check Your Inbox:**
- Email subject: "Daily AI & World News"
- From: your-email@gmail.com
- Should contain:
  - Top 5 AI news articles
  - Top 5 world news articles
  - Each with title, summary, source, link

**2. Check Spam Folder:**
- Sometimes first email goes to spam
- Mark as "Not spam" so future emails go to inbox

**3. Verify Content:**
- [ ] Email has nice formatting
- [ ] Articles are readable
- [ ] Links work
- [ ] Summary text makes sense

---

## PART 5: Ongoing Management

### Daily (Automatic)

- Email is sent automatically at your scheduled time
- No manual action needed!

### Weekly Check

**1. Go to Render Dashboard:**
- Click your cron job
- Click **Events** tab

**2. Verify Jobs Ran:**
- Should see running job entries every day
- Click one to see logs
- Verify no error messages

### When You Update Code

**1. Make Changes Locally:**
- Edit files in your editor
- Test: `python app/main.py --run-once`

**2. Push to GitHub:**
```bash
git add .
git commit -m "Description of changes"
git push
```

**3. Render Auto-Updates:**
- Detects code change automatically (1-2 seconds)
- Redeploys (2-3 minutes)
- Updated code runs next scheduled time
- No manual Render action needed!

---

## 🎉 You're Done!

If you completed all sections:

✅ Project on GitHub  
✅ Deployed on Render  
✅ Email received successfully  
✅ Scheduled to run daily automatically  

**Your Daily AI News automation is LIVE! 🚀**

---

## Quick Reference

| Need | Action |
|------|--------|
| Change schedule | Cron Job Settings → Schedule |
| Update API keys | Cron Job → Environment → Edit |
| View logs | Cron Job → Logs |
| Manual trigger | Cron Job → Trigger Job button |
| Update code | `git push` (auto-deploys) |
| Check history | Cron Job → Events tab |

---

## Troubleshooting Quick Links

- Build failed? → Check `DEPLOYMENT_CHECKLIST.md` → Troubleshooting section
- Email not received? → Same file, "Email Not Received" section
- GitHub issues? → `GITHUB_SETUP.md`
- Render issues? → `DEPLOYMENT.md`

---

**Questions? Check the detailed guides or Render support at render.com/support**
