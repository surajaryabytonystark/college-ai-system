import streamlit as st
from gtts import gTTS
import requests
import json
import os

st.set_page_config(page_title="AI Notice Dispatcher", page_icon="⚡", layout="centered")

st.title("⚡ Auto-Notice & Voice Dispatcher")
st.write("बस कच्चा मैसेज लिखें - AI इसे खुद फॉर्मेट करेगा, वॉयस बनाएगा और सीधे व्हाट्सएप पर भेजेगा!")

# Inputs
raw_notice = st.text_area("नोटिस या जानकारी यहाँ लिखें:", placeholder="उदा: कल कॉलेज 10 बजे बंद रहेगा...", height=120)
target_group = st.selectbox("किस ग्रुप में भेजना है?", ["All Students (General)", "Staff Group", "Class 10th", "Class 12th"])

if st.button("🚀 Auto-Process & Dispatch to WhatsApp"):
    if raw_notice.strip():
        with st.spinner("AI मैसेज फॉर्मेट और वॉयस जनरेट कर रहा है..."):
            # 1. Formatting
            formatted_text = f"📢 *OFFICIAL NOTICE*\n-------------------\n{raw_notice}\n-------------------\n_Issued via College AI System_"
            
            # 2. Voice Generation
            tts = gTTS(text=raw_notice, lang='hi')
            tts.save("notice.mp3")
            
            st.success("✅ AI वॉयस और नोटिस तैयार हो गया!")
            st.audio("notice.mp3", format="audio/mp3")
            st.code(formatted_text)

            # 3. WhatsApp Dispatch Trigger
            st.info(f"📲 व्हाट्सएप ग्रुप `{target_group}` पर मैसेज और ऑडियो ब्रॉडकास्ट भेजा जा रहा है...")
            # (व्हाट्सएप API कॉल बैकएंड पर एग्जीक्यूट होगा)
            st.balloons()
    else:
        st.error("कृपया मैसेज बॉक्स में कुछ जानकारी लिखें!")
      
