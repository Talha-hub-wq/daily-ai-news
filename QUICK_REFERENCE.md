# 🚀 DEPLOYMENT QUICK REFERENCE CARD

Print this page and keep it handy while deploying!

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### ✅ Have These Ready:

```
□ OpenAI API Key         → platform.openai.com/account/api-keys
□ NewsAPI Key            → newsapi.org
□ Gmail App Password     → myaccount.google.com/apppasswords
□ GitHub Account         → github.com
□ Render Account         → render.com
```

---

## 🔑 API KEYS & CREDENTIALS FORMAT

```
OPENAI_API_KEY        = sk-proj-xxxxx...
NEWSAPI_KEY           = 0fa5a91c...
EMAIL_SENDER          = your-email@gmail.com
EMAIL_PASSWORD        = xxxx xxxx xxxx xxxx  (← 16 char app password!)
EMAIL_RECIPIENT       = recipient@example.com
SMTP_SERVER           = smtp.gmail.com
SMTP_PORT             = 587
SCHEDULE_TIME         = 22:00  (24-hour format)
```

---

## 🐙 GITHUB SETUP (10 minutes)

```bash
# Navigate to project
cd "d:\daily AI news"

# Initialize git
git init

# Configure git
git config --global user.name "Your Name"
git config --global user.email "your-email@github.com"

# Stage files
git add .

# Commit
git commit -m "Initial commit: Daily AI news automation"

# Add remote
git remote add origin https://github.com/USERNAME/daily-ai-news.git

# Push
git branch -M main
git push -u origin main
```

---

## 🚀 RENDER DEPLOYMENT (15 minutes)

### Step 1: Login
- Go to https://render.com
- Sign in with GitHub or email

### Step 2: Create Cron Job
- Click **+ New** → **Cron Job**
- Click **Connect Repository**
- Select **daily-ai-news**
- Click **Connect**

### Step 3: Configure

```
Name:              daily-ai-news
Language:          Python 3
Build Command:     pip install -r requirements.txt
Start Command:     python app/main.py --run-once
Schedule:          0 22 * * *  (10 PM UTC)
```

### Step 4: Environment Variables

Add these 8 variables:

| Key | Value |
|-----|-------|
| OPENAI_API_KEY | `sk-proj-...` |
| NEWSAPI_KEY | `0fa5...` |
| EMAIL_SENDER | `your@gmail.com` |
| EMAIL_PASSWORD | `xxxx xxxx xxxx xxxx` |
| EMAIL_RECIPIENT | `recipient@example.com` |
| SMTP_SERVER | `smtp.gmail.com` |
| SMTP_PORT | `587` |
| SCHEDULE_TIME | `22:00` |

### Step 5: Deploy
- Click **Create Cron Job**
- Wait for build (2-3 min)
- Status should show **Deployed** ✅

---

## ✅ VERIFICATION (5 minutes)

```bash
1. Click "Trigger Job" button
2. Wait for execution
3. Check Event Logs - should show success
4. Go to inbox - look for "Daily AI & World News" email
5. If not there, check spam folder
```

---

## ⏰ TIMEZONE CONVERSION

If you want emails at specific local time:

| Your Time | Your Zone | Cron Code |
|-----------|-----------|-----------|
| 2 PM | PST | 0 22 * * * |
| 3 PM | MST | 0 23 * * * |
| 4 PM | CST | 0 0 * * * |
| 5 PM | EST | 0 1 * * * |
| 10 PM | GMT | 0 22 * * * |

---

## 🆘 QUICK TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| **Build Failed** | Check Render logs, verify requirements.txt |
| **Email Not Received** | Check spam, verify EMAIL_RECIPIENT, use 16-char app password |
| **Missing Variables** | Go to Environment tab, add missing ones |
| **Job Didn't Run** | Check timezone, verify time conversion |
| **Authentication Error** | Verify EMAIL_PASSWORD is app password, not regular password |

---

## 📚 DOCUMENTATION GUIDES

```
DEPLOYMENT_START_HERE.md    ← Master guide (start here!)
RENDER_QUICKSTART.md        ← 5-minute version
STEP_BY_STEP_GUIDE.md       ← Visual walkthrough
DEPLOYMENT_CHECKLIST.md     ← Verification checklist
DEPLOYMENT.md               ← Complete reference
GITHUB_SETUP.md             ← GitHub detailed guide
GUIDES_INDEX.md             ← Guide comparison
```

---

## 💾 FILES CREATED FOR DEPLOYMENT

```
render.yaml              ← Render configuration
Procfile               ← Process definition
runtime.txt            ← Python 3.11.8
build.sh               ← Build script
requirements.txt       ← Dependencies (updated)
.env.example          ← Template (without real keys!)
.gitignore            ← Git ignore rules
```

---

## 🔒 SECURITY REMINDERS

```
✓ .env is NOT on GitHub (in .gitignore)
✓ .env.example has NO real API keys
✓ Use Gmail APP PASSWORD (not regular password)
✓ Keep API keys private and secure
✓ Never share .env file
✓ Never commit .env to GitHub
```

---

## 🎯 WHAT HAPPENS AUTOMATICALLY

Once deployed:

```
Every day at 10:00 PM UTC:
  1. Render triggers your cron job
  2. App fetches AI news (5 articles)
  3. App fetches world news (5 articles)
  4. OpenAI summarizes each article
  5. Email sent to your inbox
  6. Logs recorded for monitoring
  7. Process completes (~20 seconds)
  
ZERO manual intervention needed! ✅
```

---

## 📞 HELP RESOURCES

| Problem | Resource |
|---------|----------|
| First time deploying? | DEPLOYMENT_START_HERE.md |
| Want visual guide? | STEP_BY_STEP_GUIDE.md |
| Need verification? | DEPLOYMENT_CHECKLIST.md |
| Have questions? | DEPLOYMENT.md |
| GitHub issues? | GITHUB_SETUP.md |
| Quick reference? | RENDER_QUICKSTART.md |
| All guides | GUIDES_INDEX.md |

---

## ✅ SUCCESS CHECKLIST

- [ ] GitHub repo created
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Cron job created
- [ ] All 8 env variables added
- [ ] Build completed (status = Deployed)
- [ ] Job triggered manually
- [ ] Email received in inbox
- [ ] Email content verified
- [ ] Logs show no errors

**If all checked: YOU'RE DONE!** 🎉

---

## 🚀 NEXT STEPS

1. **Get API Keys** (5 min)
   - https://platform.openai.com/account/api-keys
   - https://newsapi.org
   - https://myaccount.google.com/apppasswords

2. **Push to GitHub** (10 min)
   - Use commands in GITHUB SETUP section above

3. **Deploy on Render** (15 min)
   - Follow RENDER DEPLOYMENT section above

4. **Test & Verify** (5 min)
   - Follow VERIFICATION section above

**Total: ~45 minutes ⏱️**

---

## 📖 WHICH GUIDE SHOULD I READ?

```
FIRST TIME DEPLOYING?
└─ Read: DEPLOYMENT_START_HERE.md

EXPERIENCED WITH CLOUD PLATFORMS?
└─ Read: RENDER_QUICKSTART.md

WANT VISUAL WALKTHROUGH?
└─ Read: STEP_BY_STEP_GUIDE.md

NEED DETAILED REFERENCE?
└─ Read: DEPLOYMENT.md

WANT TO TRACK EVERY STEP?
└─ Read: DEPLOYMENT_CHECKLIST.md

NEED GITHUB HELP?
└─ Read: GITHUB_SETUP.md

WANT GUIDE COMPARISON?
└─ Read: GUIDES_INDEX.md
```

---

## 🎯 REMEMBER

- ✅ All code is ready
- ✅ All configs are ready
- ✅ All documentation is ready
- ✅ You just need to:
  1. Get API keys
  2. Push to GitHub
  3. Deploy on Render
  4. Verify it works

**You've got this!** 🚀

---

**Print this → Keep handy → Refer while deploying**

If stuck on a step, check the relevant guide above.

All guides are in the project root directory.

Good luck! 🎉
