import pandas as pd
import requests
import os
import plotly.express as px


def create_chart_image(df):
    """Generates a sleek, dark-themed image of the last 30 days of growth."""
    # Grab the last 30 days so the mobile chart isn't overly cramped
    df_recent = df.tail(30).copy()

    df_long = df_recent.reset_index().melt(
        id_vars="Date",
        value_vars=["Liquid_Fund_NAV", "Wekeza_Maisha_NAV"],
        var_name="Fund",
        value_name="NAV (TZS)",
    )
    df_long["Fund"] = df_long["Fund"].str.replace("_", " ")

    fig = px.line(
        df_long,
        x="Date",
        y="NAV (TZS)",
        color="Fund",
        facet_row="Fund",
        template="plotly_dark",
        markers=True,
        color_discrete_map={
            "Liquid Fund NAV": "#00E396",
            "Wekeza Maisha NAV": "#008FFB",
        },
    )

    fig.update_traces(line=dict(width=3), marker=dict(size=6))
    fig.update_yaxes(matches=None, showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    fig.update_xaxes(showgrid=False)

    fig.update_layout(
        showlegend=False,
        height=600,
        width=800,  # Fixed width ensures a high-quality rendering
        margin=dict(t=40, b=20, l=10, r=10),
        paper_bgcolor="#0E1117",  # Matches Streamlit's dark mode
        plot_bgcolor="#0E1117",
    )

    fig.for_each_annotation(lambda a: a.update(text=f"<b>{a.text.split('=')[-1]}</b>"))

    # Save the figure as a temporary image file
    image_path = "daily_trend.png"
    fig.write_image(image_path)
    return image_path


def send_telegram_alert():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Missing Telegram credentials. Exiting.")
        return

    try:
        df = pd.read_csv("data/utt_amis_history.csv")

        if df.empty:
            print("Data is empty. Nothing to report.")
            return

        latest_data = df.iloc[-1]
        date = latest_data["Date"]

        liquid_nav = latest_data["Liquid_Fund_NAV"]
        wekeza_nav = latest_data["Wekeza_Maisha_NAV"]

        liquid_delta_str = ""
        wekeza_delta_str = ""

        if len(df) > 1:
            prev_data = df.iloc[-2]

            l_diff = liquid_nav - prev_data["Liquid_Fund_NAV"]
            l_pct = (l_diff / prev_data["Liquid_Fund_NAV"]) * 100
            l_icon = "🟢 +" if l_diff >= 0 else "🔴 "
            liquid_delta_str = f"\n   └ {l_icon}{l_diff:.2f} TZS ({l_pct:.3f}%)"

            w_diff = wekeza_nav - prev_data["Wekeza_Maisha_NAV"]
            w_pct = (w_diff / prev_data["Wekeza_Maisha_NAV"]) * 100
            w_icon = "🟢 +" if w_diff >= 0 else "🔴 "
            wekeza_delta_str = f"\n   └ {w_icon}{w_diff:.2f} TZS ({w_pct:.3f}%)"

        message = (
            f"📊 <b>UTT AMIS Daily Report</b>\n"
            f"📅 {date}\n\n"
            f"💧 <b>Liquid Fund:</b> {liquid_nav:,.2f} TZS"
            f"{liquid_delta_str}\n\n"
            f"📈 <b>Wekeza Maisha:</b> {wekeza_nav:,.2f} TZS"
            f"{wekeza_delta_str}\n\n"
            f"🔗 <a href='https://utt-amis-tracker-johnmziray.streamlit.app/'>Open Executive Dashboard</a>"
        )

        # 1. Create the chart image
        image_path = create_chart_image(df)

        # 2. Change the Telegram API endpoint to sendPhoto
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto "

        # 3. Send the image with the text acting as the caption
        with open(image_path, "rb") as photo:
            payload = {"chat_id": chat_id, "caption": message, "parse_mode": "HTML"}
            files = {"photo": photo}

            response = requests.post(url, data=payload, files=files)

        if response.status_code == 200:
            print("Telegram alert with image sent successfully!")
        else:
            print(f"Failed to send alert: {response.text}")

        # 4. Clean up the temporary image file
        if os.path.exists(image_path):
            os.remove(image_path)

    except Exception as e:
        print(f"Error reading data or sending alert: {e}")


if __name__ == "__main__":
    send_telegram_alert()
