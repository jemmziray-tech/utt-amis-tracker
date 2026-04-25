<div align="center">

<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=28&pause=1000&color=27AE60&center=true&vCenter=true&width=600&lines=UTT+AMIS+Daily+Tracker;Automating+Wealth+Tracking...;Because+Manual+Checking+is+Boring...;Serverless+Data+Pipeline+Active+%E2%9C%85" alt="Typing SVG" /></a>

**The serverless financial butler that watches your mutual funds so you don't have to.**

[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://utt-amis-tracker-johnmziray.streamlit.app/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3.10-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](#)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Engineering-150458?style=for-the-badge&logo=pandas&logoColor=white)](#)
[![Telegram](https://img.shields.io/badge/Telegram-Live%20Alerts-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](#)

<br>

### 🌐 **[View the Live Interactive Dashboard Here](https://utt-amis-tracker-johnmziray.streamlit.app/)**

</div>

---

## 🚀 The Mission
Let’s be honest: logging into financial portals every single day just to check if your Net Asset Value (NAV) moved by 0.02% is exhausting. 

I built this repository to completely automate the tracking of **Tanzania's UTT AMIS** mutual funds (specifically the *Liquid Fund* and *Wekeza Maisha*). It acts as a lightweight, fully automated data engineering pipeline that scrapes, cleans, stores, and alerts—all while I'm busy doing literally anything else.

## ✨ Features (What the Robot Does)
- 📊 **Interactive Web Dashboard:** Hosts a live, auto-updating Streamlit application with interactive Plotly charts and a wealth forecasting time-machine.
- 🕵️‍♂️ **Automated Web Scraping:** Uses `pandas` to silently extract live financial tables from the UTT AMIS website.
- 🗄️ **Living Database:** Appends the cleaned data to a historical `.csv` file directly inside this repository.
- ⏰ **Cron-Triggered:** Runs flawlessly at 17:00 EAT every weekday via GitHub Actions. Zero servers to maintain.
- 📱 **Telegram Integration:** Pings my phone with a formatted market summary right as the work day ends.

<br>

<div align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2FqZ2QyaWpxMmF3YTF1bDF4aHZxZ2x1MDFkbnVzaDZqbjF6YWlpeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/L1R1tvI9svkIWwpVYr/giphy.gif" width="300" alt="Robot processing data animation">
  <br>
  <i>Live footage of GitHub Actions handling my investments.</i>
</div>

<br>

## ⚙️ How It Works (The Magic)
1. **`scraper.py`**: The brains. It tricks the website into thinking it's a real browser, hunts down the exact HTML table containing the NAVs, sanitizes the giant numbers, and saves them.
2. **`notifier.py`**: The mouthpiece. It reads the latest row from the CSV, securely grabs my hidden API tokens, and fires off a message to the Telegram bot.
3. **`app.py`**: The face. It connects to Streamlit Community Cloud to instantly render the CSV data into an interactive, public-facing web UI.
4. **`tracker.yml`**: The boss. It wakes up Ubuntu in the cloud, installs the dependencies, runs the scripts, commits the new data back to the repo, and goes back to sleep.

---

## 🛠️ Want Your Own Butler? (Setup Guide)
Feel free to fork this repository and set up your own tracker! 

1. **Fork** this repository.
2. Create a Telegram Bot via `BotFather` and get your Chat ID via `IDBot`.
3. Go to your repository **Settings > Secrets and variables > Actions**.
4. Add two Repository Secrets:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
5. Go to the **Actions** tab, enable workflows, and run it manually to test!

---
<div align="center">
  <b>Built with 💻 and ☕ by <a href="https://github.com/jemmziray-tech">John Mziray</a></b>
  <br>
  <i>Because data pipelines equal peace of mind.</i>
</div>
