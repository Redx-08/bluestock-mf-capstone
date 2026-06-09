import requests
import pandas as pd
from pathlib import Path
import time

RAW_PATH = Path("data/raw")
RAW_PATH.mkdir(parents=True, exist_ok=True)

funds = {
    "125497": "HDFC_Top_100",
    "119551": "SBI_Bluechip",
    "120503": "ICICI_Bluechip",
    "118632": "Nippon_Large_Cap",
    "119092": "Axis_Bluechip",
    "120841": "Kotak_Bluechip"
}

print("Fetching live NAV data from mfapi.in...")

for code, name in funds.items():
    url = f"https://api.mfapi.in/mf/{code}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            nav_data = data.get("data", [])
            
            if nav_data:
                df = pd.DataFrame(nav_data)
                df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
                df = df.sort_values('date')
                
                file_path = RAW_PATH / f"live_{name}_{code}.csv"
                df.to_csv(file_path, index=False)
                print(f"Saved {name} ({code}) -> {len(df)} records")
            else:
                print(f"No data for {name} ({code})")
        else:
            print(f"Failed {name} ({code}): HTTP {response.status_code}")
            
    except Exception as e:
        print(f"Error fetching {name} ({code}): {e}")
    
    time.sleep(0.5)

print(f"Files saved to: {RAW_PATH}/")