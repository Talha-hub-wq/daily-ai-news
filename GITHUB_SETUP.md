# GitHub Setup Guide

Complete guide to push your Daily AI News project to GitHub and connect it with Render.

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface (Recommended)

1. Go to [github.com](https://github.com) and log in
2. Click **+** icon (top right) → **New repository**
3. Enter:
   - **Repository name:** `daily-ai-news`
   - **Description:** "Automated daily AI & world news email updates"
   - **Visibility:** Public (recommended for Render)
   - Leave other options default
4. Click **Create repository**
5. Copy the repository URL (e.g., `https://github.com/YOUR_USERNAME/daily-ai-news.git`)

### Option B: Using GitHub CLI

```bash
# Install GitHub CLI from https://cli.github.com
gh auth login
gh repo create daily-ai-news --public --source=. --remote=origin --push
```

---

## Step 2: Initialize Git in Your Project

### Windows (PowerShell)

```bash
# Navigate to project directory
cd D:\daily AI news

# Initialize git repository
git init

# Verify git is initialized
git status
```

### Mac/Linux

```bash
cd ~/daily-ai-news
git init
```

---

## Step 3: Configure Git User

**First time only:**

```bash
# Set your name (used in commits)
git config --global user.name "Your Name"

# Set your email (use your GitHub email)
git config --global user.email "your-email@github.com"

# Verify
git config --global user.name
git config --global user.email
```

---

## Step 4: Add Files to Git

```bash
# Add all files
git add .

# View what will be added
git status

# Expected output:
# - app/ (folder with Python files)
# - config/ (folder with settings)
# - templates/ (folder with HTML)
# - requirements.txt
# - README.md
# - .gitignore
# - Procfile
# - render.yaml
# - etc.
```

---

## Step 5: Create First Commit

```bash
# Commit with message
git commit -m "Initial commit: Daily AI news automation agent for Render"

# View commit
git log --oneline
```

---

## Step 6: Connect to GitHub

```bash
# Add remote repository (replace URL with yours)
git remote add origin https://github.com/YOUR_USERNAME/daily-ai-news.git

# Verify remote
git remote -v

# Expected output:
# origin  https://github.com/YOUR_USERNAME/daily-ai-news.git (fetch)
# origin  https://github.com/YOUR_USERNAME/daily-ai-news.git (push)
```

---

## Step 7: Push to GitHub

### First Push (requires authentication)

```bash
# Rename branch to main (GitHub default)
git branch -M main

# Push to GitHub
git push -u origin main
```

**On Windows, you may get prompted:**
- If asked for credentials, enter your GitHub username and password
- Or use a Personal Access Token:
  1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
  2. Click **Generate new token (classic)**
  3. Select `repo` scope
  4. Copy token
  5. Use as password when prompted

### Subsequent Pushes

After the first push, just use:

```bash
git push
```

---

## Verify on GitHub

1. Go to [github.com/YOUR_USERNAME/daily-ai-news](https://github.com/YOUR_USERNAME/daily-ai-news)
2. You should see your files listed
3. Check README.md displays correctly
4. Click **commits** to see your history

---

## Step 8: Connect Render to GitHub

### Method 1: During Cron Job Creation (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **+ New** → **Cron Job**
3. Click **Connect Repository**
4. Authorize Render to access GitHub
5. Select your **daily-ai-news** repository
6. Click **Connect**

### Method 2: Manual Connection

1. Go to Render dashboard
2. Click your account → **Connected Services**
3. Click **Connect GitHub**
4. Authorize Render

---

## Updating Code on GitHub

After initial push, to make changes:

### Local Changes

```bash
# Make changes to files in your editor

# View changes
git status

# Stage changes
git add .

# Or stage specific files
git add app/main.py config/settings.py

# Commit
git commit -m "Description of changes"

# Push to GitHub
git push
```

### Render Auto-Deployment

When you `git push`:
1. Code automatically updates in GitHub
2. Render detects the change (takes 1-2 seconds)
3. Render rebuilds automatically (takes 2-3 minutes)
4. Updated code runs on next scheduled time

---

## Ignore Sensitive Files

Your `.gitignore` already includes:

```
.env           # Never commit API keys!
logs/          # Log files
__pycache__/   # Python cache
.vscode/       # IDE settings
```

**Verify before pushing:**

```bash
# Check what will be committed
git status

# Should NOT show:
# .env
# logs/
# __pycache__/
```

---

## Create .env Template for Others (Optional)

Since `.env` is ignored, create `.env.example`:

```
# Already created for you!
cat .env.example

# Should include all variable names (no actual values)
```

---

## Common Git Commands

```bash
# View commit history
git log

# View changes before committing
git diff

# Undo uncommitted changes
git restore <filename>

# View what's staged
git status

# Remove file from tracking (keep locally)
git rm --cached <filename>

# View remote
git remote -v

# Change remote URL
git remote set-url origin https://new-url-here
```

---

## Troubleshooting

### "Permission denied (publickey)"

**Solution:** Set up SSH keys instead of HTTPS:

```bash
# Generate SSH key (follow prompts)
ssh-keygen -t ed25519 -C "your-email@github.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub
# Paste at https://github.com/settings/ssh/new

# Update remote to use SSH
git remote set-url origin git@github.com:YOUR_USERNAME/daily-ai-news.git
```

### "fatal: not a git repository"

**Solution:**
```bash
# Make sure you're in the project directory
cd D:\daily AI news

# Reinitialize if needed
git init
```

### ".env accidentally committed"

**Solution:**
```bash
# Remove from git (keeps file locally)
git rm --cached .env

# Add pattern to .gitignore
echo ".env" >> .gitignore

# Commit change
git add .gitignore
git commit -m "Remove .env from tracking"
git push
```

### "Can't authenticate with username/password"

**Solution:** GitHub deprecated password auth. Use:
1. Personal Access Token (recommended)
2. SSH Key
3. GitHub CLI

See GitHub docs: [https://docs.github.com/en/authentication](https://docs.github.com/en/authentication)

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Connect Render to GitHub
3. ✅ Deploy on Render
4. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Render setup

---

## Double-Check Checklist

- [ ] Repository created on GitHub
- [ ] `.git` folder exists in your project
- [ ] `git remote -v` shows your GitHub URL
- [ ] Files visible on GitHub website
- [ ] `.env` is in `.gitignore` and NOT on GitHub
- [ ] All requirements.txt dependencies listed
- [ ] All source files visible on GitHub

---

**You're ready to deploy on Render! 🚀**

See [RENDER_QUICKSTART.md](RENDER_QUICKSTART.md) for the 5-minute Render setup.
