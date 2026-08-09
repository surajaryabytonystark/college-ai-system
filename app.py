import streamlit as st
from gtts import gTTS
import os

st.set_page_config(
    page_title="STARK AI | Multi-Admin Dispatcher",
    page_icon="⚡",
    layout="centered"
)

# Custom Styling
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .stark-header { background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; text-align: center; font-size: 2.2rem; }
    .stark-sub { text-align: center; color: #94a3b8; font-size: 0.95rem; margin-bottom: 20px; }
    .stButton > button { width: 100%; background: linear-gradient(90deg, #ff0844 0%, #ffb199 100%) !important; color: white !important; border: none !important; padding: 12px !important; font-weight: bold !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="stark-header">⚡ STARK MULTI-ADMIN SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="stark-sub">Role-Based Automated Access Portal</div>', unsafe_allow_html=True)

st.divider()

# Pre-defined Authorized Admins (In real app, you can add dynamically)
ADMIN_PASSCODES = {
    "1111": "Suraj (Master Owner)",
    "2222": "Principal Sir (Main Admin)",
    "3332": "Vice Principal / HOD"
}

# Sidebar Master Access
st.sidebar.title("🔐 Access Management")
user_passcode = st.sidebar.text_input("अपना Admin Passcode दर्ज करें:", type="password")

if user_passcode in ADMIN_PASSCODES:
    role = ADMIN_PASSCODES[user_passcode]
    st.sidebar.success(f"✅ Logged in as: **{role}**")
    
    st.success(f"WELCOME, **{role}**! आप ब्रॉडकास्ट भेजने के लिए अधिकृत (Authorized) हैं।")
    
    # Broadcast Interface
    raw_notice = st.text_area("📝 मैसेज या नोटिस टाइप करें:", placeholder="उदा: कल कॉलेज 10 बजे बंद रहेगा...", height=120)
    target_group = st.selectbox("🎯 किस ग्रुप में भेजना है?", ["📢 All Students (General)", "👨‍🏫 Staff Official Group", "🎓 Class 10th", "🔥 Class 12th"])
    
    if st.button("🚀 GENERATE & BROADCAST"):
        if raw_notice.strip():
            with st.spinner("AI Processing Voice & Formatting..."):
                tts = gTTS(text=raw_notice, lang='hi')
                tts.save("notice.mp3")
                
                st.audio("notice.mp3", format="audio/mp3")
                st.code(f"📢 OFFICIAL NOTICE\n-------------------\n{raw_notice}\n-------------------\nIssued by: {role}\n_Powered by Stark AI System_", language="markdown")
                st.balloons()
        else:
            st.error("कृपया कोई मैसेज टाइप करें!")

else:
    if user_passcode:
        st.error("❌ अमान्य (Invalid) Passcode! आप मैसेज नहीं भेज सकते।")
    else:
        st.warning("🔒 मैसेज भेजने के लिए कृपया बाएँ (Sidebar) में अपना Admin Passcode डालें।")
