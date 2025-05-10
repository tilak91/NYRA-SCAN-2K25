import streamlit as st
import pandas as pd
import requests
import tempfile
import urllib.request
import json
import os

# CONFIG
st.set_page_config(page_title="🎉 QR Verifier", page_icon="🔍")
st.title("🎉 Freshers Fest QR Verifier")

# Constants
EXCEL_URL = "https://raw.githubusercontent.com/tilak91/NYRA-ONE/main/freshers_data.xlsx"
SCANNED_DB = "scanned_qr.json"  # local file to track scanned QR codes

# Load scanned QR codes from file
def load_scanned_db():
    if os.path.exists(SCANNED_DB):
        with open(SCANNED_DB, "r") as f:
            return json.load(f)
    else:
        return []

# Save scanned QR codes
def save_scanned_db(scanned_qrs):
    with open(SCANNED_DB, "w") as f:
        json.dump(scanned_qrs, f)

scanned_qrs = load_scanned_db()

# Load Excel data
@st.cache_data
def load_excel_data():
    try:
        with urllib.request.urlopen(EXCEL_URL) as response:
