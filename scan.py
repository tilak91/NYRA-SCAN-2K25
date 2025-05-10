import streamlit as st
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
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
                tmp_file.write(response.read())
                df = pd.read_excel(tmp_file.name)
        return df
    except Exception as e:
        st.error(f"Error loading Excel: {e}")
        return pd.DataFrame()

df = load_excel_data()

# QR scanning section
st.subheader("📸 Scan QR Code using Webcam")
qr_image = st.camera_input("Use your phone camera or webcam")

if qr_image is not None:
    st.image(qr_image, caption="Scanned QR", width=250)

    files = {'file': qr_image.getvalue()}
    api_url = "https://api.qrserver.com/v1/read-qr-code/"
    response = requests.post(api_url, files=files)

    try:
        qr_data = response.json()[0]['symbol'][0]['data']
        if qr_data:
            if qr_data in scanned_qrs:
                st.error("🚫 This QR code has already been scanned! Entry not allowed.")
            else:
                st.success(f"✅ QR Code Data: {qr_data}")
                match = df[df['Virtual Pass ID'] == qr_data]
                if not match.empty:
                    st.success("🎟 Valid Entry Pass!")
                    st.write(f"👤 Name: **{match.iloc[0]['Name']}**")
                    st.write(f"🎓 Roll No: **{match.iloc[0]['Roll No']}**")
                    st.write(f"🏫 Branch: **{match.iloc[0]['Branch']}**")
                    st.write(f"📅 Year: **{match.iloc[0]['Year']}**")

                    # Add to scanned list and save
                    scanned_qrs.append(qr_data)
                    save_scanned_db(scanned_qrs)
                else:
                    st.error("❌ Invalid Pass! Entry Denied.")
        else:
            st.error("⚠️ No data found in QR Code.")
    except Exception as e:
        st.error(f"Error decoding QR: {e}")
