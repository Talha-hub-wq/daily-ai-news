# Daily AI & World News Automation Agent

An automated system that fetches the latest AI and world news daily, summarizes them using OpenAI, and sends a beautifully formatted email at 10:00 PM every day.

> 🚀 **Ready to deploy?** See [DEPLOYMENT GUIDES](#-deployment-guides) below for Render, GitHub, and complete setup instructions.

## Features

✅ **Automated Daily News Delivery** - Sends curated news every day at 10:00 PM  
✅ **AI News Focus** - Top 5 latest AI tools, products, and advancements  
✅ **World News** - Top 5 global news updates  
✅ **Smart Summarization** - Uses OpenAI GPT to create 2-3 sentence summaries  
✅ **Duplicate Prevention** - Removes duplicate articles  
✅ **HTML Email** - Professional, responsive email design  
✅ **Error Handling** - Graceful fallbacks and retry logic  
✅ **Logging** - Detailed logs for debugging  

## Project Structure

```
daily AI news/
├── app/
│   ├── main.py              # Entry point and scheduler setup
│   ├── news_fetcher.py      # Fetches news from APIs
│   ├── summarizer.py        # Summarizes with OpenAI
│   ├── email_sender.py      # Sends HTML emails
│   └── scheduler.py         # Handles daily scheduling
├── config/
│   └── settings.py          # Configuration and environment variables
├── templates/
│   └── email_template.html  # HTML email template
├── logs/                    # Auto-created, stores app.log
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
└── README.md               # This file
```

## 🚀 Deployment Guides

### Quick Start (Choose One)

| Guide | Time | Best For |
|-------|------|----------|
| [**RENDER_QUICKSTART.md**](RENDER_QUICKSTART.md) | 5 min | Deploy immediately |
| [**STEP_BY_STEP_GUIDE.md**](STEP_BY_STEP_GUIDE.md) | 30 min | Visual walkthrough |
| [**DEPLOYMENT.md**](DEPLOYMENT.md) | Detailed | Complete reference |
| [**DEPLOYMENT_CHECKLIST.md**](DEPLOYMENT_CHECKLIST.md) | Reference | Verification checklist |
| [**GITHUB_SETUP.md**](GITHUB_SETUP.md) | 10 min | GitHub push guide |

### Deployment Path

1. **GitHub Setup** (10 min) → [GITHUB_SETUP.md](GITHUB_SETUP.md)
   - Create GitHub repo
   - Push project code
   
2. **Prepare Credentials** (10 min) → See below
   - Get API keys
   - Generate Gmail app password
   
3. **Deploy on Render** (15 min) → [RENDER_QUICKSTART.md](RENDER_QUICKSTART.md)
   - Create cron job
   - Add environment variables
   - Deploy!
   
4. **Test & Verify** (5 min) → [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
   - Trigger job manually
   - Verify email received
   - Check logs

**Total Time: 40 minutes to fully deployed!** ⏱️

---

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- Gmail account (for SMTP) or another email service
- OpenAI API key
- NewsAPI key (free tier available)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get API Keys

#### NewsAPI Key (Free)
1. Visit [https://newsapi.org](https://newsapi.org)
2. Click "Get API Key"
3. Sign up with email
4. Copy your API key

#### OpenAI API Key
1. Visit [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Click "Create new secret key"
3. Copy the key (you won't see it again)

#### Gmail Setup (SMTP)
1. Enable 2-Step Verification in your Google Account
2. Generate an App Password:
   - Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character password

### 4. Create .env File

Create a `.env` file in the project root directory with your credentials:

```env
# API Keys
OPENAI_API_KEY=sk-your-openai-key-here
NEWSAPI_KEY=your-newsapi-key-here

# Email Configuration (Gmail)
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-16-char-app-password
EMAIL_RECIPIENT=recipient@example.com

# SMTP Settings (Gmail defaults)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Scheduling (24-hour format)
SCHEDULE_TIME=22:00
```

⚠️ **Important**: Never commit `.env` to version control!

### 5. Verify Setup

Run the app once to test:

```bash
python app/main.py --run-once
```

You should see:
- Configuration validation ✓
- News fetching
- Article summarization
- Email sending

Check your inbox for the news email!

## How to Run

### Option 1: Run Scheduler (Recommended)

Start the automatic scheduler (runs at 10:00 PM daily):

```bash
python app/main.py
```

The scheduler will:
- Run continuously
- Check for scheduled tasks every minute
- Send email at 10:00 PM (22:00)
- Log all activity to `logs/app.log`

### Option 2: Run Once (Testing)

Test the system without starting the scheduler:

```bash
python app/main.py --run-once
```

### Option 3: Schedule with System Cron/Task Scheduler

**Windows (Task Scheduler):**

1. Open Task Scheduler
2. Create Basic Task → "Daily News Update"
3. Trigger: Daily at 10:00 PM
4. Action: Start program
   - Program: `python.exe`
   - Arguments: `app/main.py --run-once`
   - Start in: `path\to\daily AI news`
5. Click OK

**Linux/Mac (Cron):**

```bash
# Open crontab
crontab -e

# Add this line (sends email at 10 PM daily)
0 22 * * * cd /path/to/daily\ AI\ news && python app/main.py --run-once
```

## How the System Works

### 1. News Fetching (`news_fetcher.py`)
- Queries NewsAPI for AI news and world news
- Uses multiple search queries for better coverage
- Returns top 5 unique articles per category
- Handles API errors gracefully

### 2. Summarization (`summarizer.py`)
- Uses OpenAI GPT-3.5-turbo
- Creates 2-3 line summaries for each article
- Falls back to original description if API fails
- Handles rate limiting gracefully

### 3. Email Sending (`email_sender.py`)
- Constructs professional HTML email
- Uses SMTP to send via Gmail
- Includes article titles, summaries, sources, and links
- Responsive design works on mobile and desktop

### 4. Scheduling (`scheduler.py`)
- Uses `schedule` library (simple and reliable)
- Runs job at specified time daily
- Logs all activity

## Example Email Output

**Subject:** Daily AI & World News

**Content:**
```
📰 Daily AI & World News
Your daily digest of the latest AI innovations and global updates

🤖 Top AI News
1. OpenAI Releases GPT-5
   OpenAI announced the release of GPT-5, featuring improved reasoning...
   Source: TechCrunch
   Read full article →

2. New AI Chip Breakthrough
   ...

🌍 Top World News
1. Global Markets React to Economic News
   ...
```

## Configuration Guide

### Change Scheduling Time

Edit `.env`:
```env
SCHEDULE_TIME=14:30  # 2:30 PM
```

### Change Email Recipient

Edit `.env`:
```env
EMAIL_RECIPIENT=newrecipient@example.com
```

### Use Different Email Provider

For Outlook:
```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
```

For Yahoo:
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

## Error Handling

The system includes robust error handling:

- **API Failures**: Uses fallback descriptions if OpenAI API fails
- **Rate Limiting**: Catches and logs rate limit errors
- **Empty Results**: Logs warning if no news found
- **Email Errors**: Logs SMTP errors and continues
- **Missing Config**: Validates all required variables before starting

All errors are logged to `logs/app.log`.

## Troubleshooting

### "Missing required environment variables"
**Solution:** Check `.env` file has all required keys. Run `python app/main.py` to see which ones are missing.

### "SMTP authentication failed"
**Solution:** Verify Email, Password, and SMTP settings in `.env`. For Gmail, make sure you're using the 16-character app password, not your regular password.

### "NewsAPI quota exceeded"
**Solution:** Wait until tomorrow (quota resets daily). Free tier gives 100 requests/day.

### "OpenAI API rate limit"
**Solution:** Default is 3 requests/minute. The system falls back to original descriptions if rate limited.

### No email received
**Solution:** 
1. Check `logs/app.log` for errors
2. Check spam folder
3. Verify recipient email in `.env`
4. Test with `python app/main.py --run-once`

### Scheduler not sending at 10 PM
**Solution:** 
1. Keep terminal/command window open
2. Check system time is correct
3. Verify `SCHEDULE_TIME=22:00` in `.env`
4. Check `logs/app.log` for scheduled job confirmation

## Advanced Usage

### Customize News Queries

Edit `app/news_fetcher.py`, modify the `queries` list in `fetch_ai_news()`:

```python
queries = [
    "latest AI news 2026",
    "machine learning breakthroughs",
    "AI startup funding"
]
```

### Modify Email Template

Edit `templates/email_template.html`. The placeholders are:
- `{{ AI_NEWS }}` - AI news section (auto-populated)
- `{{ WORLD_NEWS }}` - World news section (auto-populated)

### Use Different News Source

Replace NewsAPI with other sources:
- `newsdata.io` - Free tier
- `currentsapi.services` - Free tier
- Custom web scraping with BeautifulSoup

## Performance

- **Startup**: < 2 seconds
- **News Fetch**: 2-3 seconds
- **Summarization**: 5-10 seconds (depends on OpenAI API)
- **Email Send**: 1-2 seconds
- **Total Time**: ~10-15 seconds

## Security Note

- `.env` file contains sensitive credentials
- Add `.env` to `.gitignore` if using git
- Never share your API keys or app passwords
- Regenerate API keys if accidentally exposed

## Dependencies

- `requests` - HTTP requests for API calls
- `openai` - OpenAI API client
- `schedule` - Job scheduling library
- `python-dotenv` - Load environment variables

## License

MIT License - Feel free to use and modify

## Support

For issues:
1. Check `logs/app.log` for detailed error messages
2. Verify all API keys are valid
3. Test with `python app/main.py --run-once`
4. Check internet connection

## Future Enhancements

- Database for storing sent news (prevent duplicates across days)
- User preferences for news categories
- Multiple recipient support
- Web dashboard to view scheduled emails
- Push notifications alternative to email
- Support for more news sources

---

**Enjoy your daily AI & World News! 🚀**
