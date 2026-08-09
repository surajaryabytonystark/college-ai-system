import streamlit as st
from gtts import gTTS
import os

st.set_page_config(
    page_title="STARK AI | Master Control Hub",
    page_icon="⚡",
    layout="centered"
)

# Custom Stark Styling
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .stark-header { background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; text-align: center; font-size: 2.2rem; }
    .stark-sub { text-align: center; color: #94a3b8; font-size: 0.95rem; margin-bottom: 20px; }
    .stButton > button { width: 100%; background: linear-gradient(90deg, #ff0844 0%, #ffb199 100%) !important; color: white !important; border: none !important; padding: 12px !important; font-weight: bold !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="stark-header">⚡ STARK MASTER CONTROL</div>', unsafe_allow_html=True)
st.markdown('<div class="stark-sub">Main Owner Control Panel</div>', unsafe_allow_html=True)

st.divider()

# Session state to manage dynamic admins in memory
if "admins" not in st.session_state:
    # 👑 DEFAULT MASTER OWNER (केवल Suraj)
    st.session_state.admins = {
        "7860": {"name": "Suraj (Master Owner 👑)", "role": "Master"}
    }

# Sidebar Authentication
st.sidebar.title("🔐 Passcode Verification")
input_pin = st.sidebar.text_input("अपना Passcode दर्ज करें:", type="password")

if input_pin in st.session_state.admins:
    user_info = st.session_state.admins[input_pin]
    user_name = user_info["name"]
    user_role = user_info["role"]
    
    st.sidebar.success(f"👤 Logged in: **{user_name}**")
    
    # MASTER OWNER SPECIAL CONTROLS (नए एडमिन जोड़ने/हटाने का पैनल)
    if user_role == "Master":
        st.subheader("👑 Master Control: नए Admins मैनेज करें")
        with st.expander("➕ नए Admin को Add करें (प्रिंसिपल सर / टीचर्स)"):
            new_name = st.text_input("Admin का नाम लिखें (उदा: Principal Sir):")
            new_pin = st.text_input("उनके लिए नया PIN बनाएँ (उदा: 2222):", type="password")
            
            if st.button("➕ Add New Admin Access"):
                if new_name and new_pin:
                    st.session_state.admins[new_pin] = {"name": new_name, "role": "Admin"}
                    st.success(f"✅ **{new_name}** को नया Admin बना दिया गया है! उनका PIN है: `{new_pin}`")
                else:
                    st.warning("कृपया नाम और PIN दोनों दर्ज करें!")

        st.markdown("---")

    # BROADCAST INTERFACE (यह सब Admins के लिए काम करेगा)
    st.subheader("📢 Broadcast Notice Center")
    raw_notice = st.text_area("📝 नोटिस या मैसेज टाइप करें:", placeholder="उदा: कल कॉलेज बंद रहेगा...", height=120)
    target_group = st.selectbox("🎯 टारगेट ग्रुप चुनें:", ["📢 All Students", "👨‍🏫 Staff Group", "🎓 Class 10th", "🔥 Class 12th"])
    
    if st.button("🚀 EXECUTE & BROADCAST"):
        if raw_notice.strip():
            with st.spinner("AI Processing Audio Broadcast..."):
                tts = gTTS(text=raw_notice, lang='hi')
                tts.save("notice.mp3")
                
                st.audio("notice.mp3", format="audio/mp3")
                st.code(f"📢 OFFICIAL NOTICE\n-------------------\n{raw_notice}\n-------------------\nIssued By: {user_name}\n_Powered by Stark AI System_", language="markdown")
                st.balloons()
        else:
            st.error("कृपया कोई मैसेज टाइप करें!")

else:
    if input_pin:
        st.error("❌ अमान्य (Invalid) PIN! केवल अधिकृत मेंबर्स ही लॉग इन कर सकते हैं।")
    else:
        st.warning("🔒 सिस्टम लॉक है! बाएँ (Sidebar) में Master Owner PIN डालकर अनलॉक करें।")
