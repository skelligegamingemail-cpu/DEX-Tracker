import streamlit as st
import pandas as pd
import re
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# --- KONFIGURACJA STREAMLIT ---
st.set_page_config(page_title="DEX Tracker DPD", page_icon="📦")

st.title("📦 DEX Tracker - DPD Online")
st.markdown("Wklej numery paczek poniżej, aby wygenerować raport Excel.")

# --- LOGIKA SELENIUM (Wersja Serwerowa) ---
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # Ważne dla serwerów:
    options.add_argument("--blink-settings=imagesEnabled=false")
    
    # Automatyczna instalacja drivera na serwerze
    return webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=options
    )

def get_raw_events(number, driver):
    url = f"https://tracktrace.dpd.com.pl/parcelDetails?typ=1&p1={number}"
    try:
        driver.get(url)
        time.sleep(2) # Czekamy na JS
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", class_="table-track")
        
        events = []
        if table:
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                texts = [c.get_text(separator=" ", strip=True) for c in cols]
                if len(texts) >= 3:
                    events.append({
                        "data": f"{texts[0]} {texts[1]}",
                        "status": texts[2],
                        "lokalizacja": texts[3] if len(texts) > 3 else ""
                    })
        return events
    except:
        return []

# --- INTERFEJS UŻYTKOWNIKA ---
input_numbers = st.text_area("Numery paczek (jeden pod drugim):", height=200)
process_btn = st.button("GENERUJ RAPORT")

if process_btn and input_numbers:
    numbers = [n.strip() for n in input_numbers.splitlines() if n.strip()]
    
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    driver = get_driver()
    
    try:
        for idx, num in enumerate(numbers, start=1):
            status_text.text(f"Sprawdzam paczkę {idx}/{len(numbers)}: {num}")
            
            # Pobieranie danych (uproszczone dla Streamlit bez rekurencji w tym przykładzie)
            events = get_raw_events(num, driver)
            
            if events:
                newest = events[0]
                results.append({
                    "ID Grupy": idx,
                    "Numer paczki": num,
                    "Ostatni Status": newest['status'],
                    "Data": newest['data'],
                    "Lokalizacja": newest['lokalizacja']
                })
            else:
                results.append({
                    "ID Grupy": idx, "Numer paczki": num, "Ostatni Status": "Brak danych/Błąd", "Data": "", "Lokalizacja": ""
                })
            
            progress_bar.progress(idx / len(numbers))
            
        driver.quit()
        
        # Wyświetlanie wyników
        df = pd.DataFrame(results)
        st.dataframe(df)
        
        # Przygotowanie do pobrania
        excel_data = df.to_excel("raport.xlsx", index=False) # Wymaga openpyxl
        with open("raport.xlsx", "rb") as f:
            st.download_button(
                label="📥 Pobierz raport Excel",
                data=f,
                file_name="raport_dpd.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
    except Exception as e:
        st.error(f"Wystąpił błąd: {e}")
        if 'driver' in locals(): driver.quit()
