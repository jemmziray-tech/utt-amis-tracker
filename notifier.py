import pandas as pd
import requests
import os


def send_telegram_alert():
    # Grab the secure secrets from GitHub's vault
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Missing Telegram credentials. Exiting.")
        return

    # Read the data we just scraped
    try:
        df = pd.read_csv("data/utt_amis_history.csv")
        # Get the very last row (today's data)
        latest_data = df.iloc[-1]

        date = latest_data["Date"]
        liquid_nav = latest_data["Liquid_Fund_NAV"]
        wekeza_nav = latest_data["Wekeza_Maisha_NAV"]

        # Format the message
        message = (
            f"📈 *UTT AMIS Daily Update* ({date})\n\n"
            f"🔹 *Liquid Fund:* {liquid_nav} TZS\n"
            f"🔹 *Wekeza Maisha:* {wekeza_nav} TZS"
        )

        # Send the message via Telegram's API
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram alert sent successfully!")
        else:
            print(f"Failed to send alert: {response.text}")

    except Exception as e:
        print(f"Error reading data or sending alert: {e}")


if __name__ == "__main__":
    send_telegram_alert()
