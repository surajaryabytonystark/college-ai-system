import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 🔑 Meta WhatsApp Cloud API Credentials
# (इनकी जगह अपनी Meta Developer Dashboard की कीज़ डालें)
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "YOUR_WHATSAPP_TOKEN_HERE")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "YOUR_PHONE_NUMBER_ID_HERE")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_broadcast', methods=['POST'])
def send_broadcast():
    data = request.json
    target = data.get('target', 'ALL')
    message_text = data.get('message', '')
    media_link = data.get('link', '')

    if not message_text:
        return jsonify({"status": "error", "message": "मैसेज खाली नहीं हो सकता!"}), 400

    # अगर लिंक मौजूद है तो मैसेज में नीचे जोड़ें
    final_text = message_text
    if media_link:
        final_text += f"\n\n🔗 लिंक: {media_link}"

    # WhatsApp API URL
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    # उदाहरण: टेस्ट नंबर (यहाँ बाद में डेटाबेस से 6th-12th के नंबर लूप में चलेंगे)
    # टेस्ट के लिए अपना व्हाट्सएप नंबर देश कोड के साथ डालें (जैसे: "919876543210")
    recipient_phone = "919876543210"

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_phone,
        "type": "text",
        "text": {
            "body": final_text
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        res_data = response.json()

        if response.status_code == 200:
            return jsonify({
                "status": "success",
                "message": f"✅ WhatsApp पर {target} को मैसेज सफलतापूर्वक भेज दिया गया!"
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"WhatsApp API एरर: {res_data.get('error', {}).get('message', 'Unknown Error')}"
            }), 400

    except Exception as e:
        return jsonify({"status": "error", "message": f"सर्वर एरर: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
