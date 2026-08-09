import os
import requests
import asyncio
from flask import Flask, render_template, request, jsonify, send_from_directory
import edge_tts

app = Flask(__name__, template_folder="templates", static_folder="static")

# Configuration (Hidden Admin / Env Vars)
AUDIO_DIR = os.path.join(os.getcwd(), "static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Green API Credentials (Replace with actual or manage via /admin)
GREEN_API_INSTANCE_ID = os.environ.get("GREEN_API_INSTANCE_ID", "YOUR_INSTANCE_ID")
GREEN_API_TOKEN = os.environ.get("GREEN_API_TOKEN", "YOUR_API_TOKEN")

# Target WhatsApp Group IDs
TARGET_GROUPS = [
    "1203630XXXXXXX@g.us",  # Class 9th
    "1203630XXXXXXX@g.us",  # Class 10th
    "1203630XXXXXXX@g.us",  # Class 11th
    "1203630XXXXXXX@g.us",  # Class 12th
]

async def generate_ai_voice(text, output_path):
    """Generates natural Hindi/Hinglish AI Voice Note via Edge-TTS (Free & High Quality)"""
    voice = "hi-IN-MadhurNeural"  # Expressive Male Voice (or "hi-IN-SwaraNeural" for female)
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def send_whatsapp_message(chat_id, message):
    """Sends Text Message via Green API"""
    url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE_ID}/sendMessage/{GREEN_API_TOKEN}"
    payload = {"chatId": chat_id, "message": message}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error sending text to {chat_id}: {e}")
        return None

def send_whatsapp_voice(chat_id, audio_file_url):
    """Sends Voice Note (.mp3/.ogg) via Green API as PTT Audio"""
    url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE_ID}/sendFileByUrl/{GREEN_API_TOKEN}"
    payload = {
        "chatId": chat_id,
        "urlFile": audio_file_url,
        "fileName": "notice_voice.mp3"
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        return response.json()
    except Exception as e:
        print(f"Error sending audio to {chat_id}: {e}")
        return None

@app.route("/")
def index():
    """Principal's Ultra-Minimalist UI"""
    return render_template("principal.html")

@app.route("/admin")
def admin():
    """Hidden Owner Control Panel (For Suraj)"""
    return render_template("admin.html")

@app.route("/api/dispatch", methods=["POST"])
def dispatch_notice():
    """1-Click Route: Generates AI Voice & Broadcasts to all target groups instantly"""
    data = request.get_json()
    text_content = data.get("text", "").strip()

    if not text_content:
        return jsonify({"success": False, "error": "मैसेज खाली नहीं हो सकता!"}), 400

    try:
        # 1. Generate AI Audio File
        audio_filename = f"notice_{os.urandom(4).hex()}.mp3"
        audio_file_path = os.path.join(AUDIO_DIR, audio_filename)
        
        asyncio.run(generate_ai_voice(text_content, audio_file_path))

        # Public URL for the generated audio (Replaced dynamically by server host/ngrok)
        host_url = request.host_url.rstrip('/')
        audio_public_url = f"{host_url}/static/audio/{audio_filename}"

        # 2. Parallel Broadcast to All WhatsApp Groups
        dispatch_results = []
        for group_id in TARGET_GROUPS:
            # Send Text Message
            text_res = send_whatsapp_message(group_id, text_content)
            # Send Voice Note
            voice_res = send_whatsapp_voice(group_id, audio_public_url)
            
            dispatch_results.append({
                "group_id": group_id,
                "text_status": text_res,
                "voice_status": voice_res
            })

        return jsonify({
            "success": True,
            "message": "सूचना सफलतापूर्वक सभी ग्रुप्स में भेज दी गई है! 📢",
            "audio_url": audio_public_url,
            "results": dispatch_results
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
