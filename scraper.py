import pandas as pd
import requests
from datetime import datetime
import os
from io import StringIO


def fetch_utt_nav():
    url = "https://uttamis.co.tz/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching data from UTT AMIS..."
        )
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        tables = pd.read_html(StringIO(response.text))
        print(f"Found {len(tables)} tables on the page. Searching for NAV data...")

        nav_df = None

        for i, table in enumerate(tables):
            if (
                "liquid fund" in table.to_string().lower()
                and "wekeza maisha" in table.to_string().lower()
            ):
                print(f"Target data found in table index {i}")
                nav_df = table
                break

        if nav_df is None:
            raise ValueError(
                "Could not find a table containing 'Liquid Fund' and 'Wekeza Maisha'."
            )

        # Standardize column names
        nav_df.columns = nav_df.columns.str.strip().str.lower()

        # Dynamically find the right columns
        scheme_cols = [
            col
            for col in nav_df.columns
            if "scheme" in col or "fund" in col or "name" in col
        ]

        # THE FIX: Force the script to specifically look for the "NAV Per Unit" column
        nav_cols = [
            col
            for col in nav_df.columns
            if "nav per unit" in col or ("nav" in col and "unit" in col)
        ]

        if not scheme_cols or not nav_cols:
            raise ValueError(
                f"Could not identify columns. Found: {nav_df.columns.tolist()}"
            )

        scheme_col = scheme_cols[0]
        nav_col = nav_cols[0]

        # Filter the DataFrame
        liquid_data = nav_df[
            nav_df[scheme_col].str.contains("Liquid Fund", case=False, na=False)
        ]
        wekeza_data = nav_df[
            nav_df[scheme_col].str.contains("Wekeza Maisha", case=False, na=False)
        ]

        if liquid_data.empty or wekeza_data.empty:
            raise ValueError(
                "Found the table, but couldn't isolate the specific funds."
            )

        # Extract values, remove commas, and convert to float
        liquid_nav = float(str(liquid_data[nav_col].values[0]).replace(",", "").strip())
        wekeza_nav = float(str(wekeza_data[nav_col].values[0]).replace(",", "").strip())

        print(f"Liquid Fund NAV Per Unit: {liquid_nav}")
        print(f"Wekeza Maisha NAV Per Unit: {wekeza_nav}")

        # Format the final data
        date_today = datetime.now().strftime("%Y-%m-%d")
        final_df = pd.DataFrame(
            {
                "Date": [date_today],
                "Liquid_Fund_NAV": [liquid_nav],
                "Wekeza_Maisha_NAV": [wekeza_nav],
            }
        )

        # Save to CSV
        os.makedirs("data", exist_ok=True)
        file_path = "data/utt_amis_history.csv"

        write_header = not os.path.exists(file_path)
        final_df.to_csv(file_path, mode="a", header=write_header, index=False)

        print(f"Successfully saved to {file_path}")

    except Exception as e:
        print(f"Error fetching NAV data: {e}")


if __name__ == "__main__":
    fetch_utt_nav()
