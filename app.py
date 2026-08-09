import streamlit as st
from gtts import gTTS
import os

# Page Config with Dark Theme
st.set_page_config(
    page_title="STARK AI | College Dispatcher",
    page_icon="⚡",
    layout="centered"
)

# Tony Stark Futuristic CSS Styling
st.markdown("""
    <style>
    /* Background & Main Container */
    .stApp {
        background: radial-gradient(circle, #0f172a 0%, #020617 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Neon Glow Header */
    .stark-header {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
        font-size: 2.2rem;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
    }
    
    /* Subtitle */
    .stark-sub {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 25px;
    }
    
    /* Custom Input Card */
    div[data-baseweb="textarea"] {
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
        background-color: #0f172a !important;
        box-shadow: 0 4px 20px rgba(0, 242, 254, 0.05);
    }
    
    /* Futuristic Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #ff0844 0%, #ffb199 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 28px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        box-shadow: 0 0 15px rgba(255, 8, 68, 0.4) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(255, 8, 68, 0.7) !important;
    }
    
    /* Status Badge */
    .status-box {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid #00f2fe;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="stark-header">⚡ STARK AI DISPATCHER</div>', unsafe_allow_html=True)
st.markdown('<div class="stark-sub">JARVIS-Powered Automated College Broadcast System</div>', unsafe_allow_html=True)

st.divider()

# Input Section
raw_notice = st.text_area("📝 कमांड / नोटिस टाइप करें:", placeholder="उदा: कल कॉलेज 10 बजे बंद रहेगा...", height=120)

target_group = st.selectbox(
    "🎯 टारगेट ऑडियो ब्रॉडकास्ट चैनल:",
    ["📢 All Students (General)", "👨‍🏫 Staff Official Group", "🎓 Class 10th Hub", "🔥 Class 12th Hub"]
)

st.write("")

# Process Button
if st.button("🚀 EXECUTE & BROADCAST"):
    if raw_notice.strip():
        with st.spinner("🤖 JARVIS Processing... Generating High-Quality Voice & Formatting..."):
            # 1. Voice Output
            tts = gTTS(text=raw_notice, lang='hi')
            tts.save("notice.mp3")
            
            # Display Success UI
            st.markdown(f"""
            <div class="status-box">
                <h4 style="color:#00f2fe; margin:0;">✅ AUDIO BROADCAST GENERATED</h4>
                <p style="color:#cbd5e1; margin-top:5px; font-size:0.85rem;">Target: {target_group}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.audio("notice.mp3", format="audio/mp3")
            
            st.markdown("### 📄 Auto-Formatted Output")
            st.code(f"📢 OFFICIAL NOTICE\n-------------------\n{raw_notice}\n-------------------\n_Issued via STARK AI System_", language="markdown")
            st.balloons()
    else:
        st.error("⚠️ एरर: कृपया पहले कोई नोटिस या कमांड टाइप करें!")
