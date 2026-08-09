import streamlit as st
from gtts import gTTS

st.set_page_config(page_title="College AI Notice System", layout="centered")

st.title("🎙️ मुरारी इंटरमीडिएट कॉलेज - AI नोटिस सिस्टम")
st.write("यहाँ संदेश लिखें और एक क्लिक में AI आवाज़ (MP3) जनरेट करें।")

notice_text = st.text_area("नोटिस का मैसेज लिखें:", height=150)

if st.button("🚀 GENERATE AI VOICE", type="primary"):
    if not notice_text.strip():
        st.error("कृपया पहले कुछ टेक्स्ट लिखें!")
    else:
        with st.spinner("AI आवाज़ बन रही है..."):
            tts = gTTS(text=notice_text, lang='hi', slow=False)
            audio_path = "notice.mp3"
            tts.save(audio_path)
            
            st.success("✅ AI वॉयस नोटिस तैयार है!")
            st.audio(audio_path)
            
            with open(audio_path, "rb") as file:
                st.download_button(
                    label="📥 Download MP3 File",
                    data=file,
                    file_name="Notice.mp3",
                    mime="audio/mp3"
                )
