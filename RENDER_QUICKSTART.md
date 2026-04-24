# Render Deployment Quick Start

This is a quick reference for deploying to Render. For detailed instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 5-Minute Setup

### 1. Prepare GitHub Repository
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/daily-ai-news.git
git push -u origin main
```

### 2. Create Render Cron Job
1. go to [render.com](https://render.com) → Sign up with GitHub
2. Click **+ New** → **Cron Job**
3. Connect your **daily-ai-news** repository
4. Set:
   - **Name:** daily-ai-news
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app/main.py --run-once`
   - **Schedule:** `0 22 * * *` (10 PM UTC daily)

### 3. Add Environment Variables

Add these in the **Environment** section:

```
OPENAI_API_KEY=sk-your-key-here
NEWSAPI_KEY=your-newsapi-key
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=16-char-app-password
EMAIL_RECIPIENT=recipient@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SCHEDULE_TIME=22:00
```

### 4. Deploy & Test

1. Click **Create Cron Job**
2. Wait for build (2-3 min)
3. Click **Trigger Job** to test
4. Check your inbox for test email

## That's it! 🎉

Your daily AI news emails will now be sent automatically at 10:00 PM UTC every day.

---

## Getting API Keys

### OpenAI Key
- Go to [platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
- Click **Create new secret key**
- Copy the key

### NewsAPI Key
- Go to [newsapi.org](https://newsapi.org)
- Sign up → Click **Get API Key**
- Copy your key

### Gmail App Password
- Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
- Select "Mail" and "Windows Computer"
- Copy the 16-character password

---

## Troubleshooting

**Build failed?**
- Check logs in Render dashboard
- Verify requirements.txt has all dependencies
- Test locally: `python app/main.py --run-once`

**Email not received?**
- Check spam folder
- Verify EMAIL_RECIPIENT is correct
- Ensure EMAIL_PASSWORD is the 16-char app password
- Check logs for SMTP errors

**Job didn't run?**
- Verify schedule time (Render uses UTC)
- Check if API keys are valid
- View logs in Render dashboard

## Change Schedule

Go to your cron job → **Settings** → **Schedule**

Common times (UTC):
- 10 PM: `0 22 * * *`
- 3 AM: `0 3 * * *`
- Twice daily: `0 10,22 * * *`

---

For complete guide, see [DEPLOYMENT.md](DEPLOYMENT.md)
