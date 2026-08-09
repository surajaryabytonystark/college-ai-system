import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 🔑 Meta WhatsApp Cloud API (Render Environment Variables से लेगा)
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "YOUR_WHATSAPP_TOKEN_HERE")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "YOUR_PHONE_NUMBER_ID_HERE")

# 📱 6th to 12th & Teachers Database (यहाँ सभी नंबर देश कोड '91' के साथ रहेंगे)
CONTACT_DATABASE = {
    "TEACHERS": ["919876543210"],  # अपने टीचर्स के नंबर यहाँ डालें
    "CLASS 6TH": [],
    "CLASS 7TH": [],
    "CLASS 8TH": [],
    "CLASS 9TH": [],
    "CLASS 10TH": [],
    "CLASS 11TH": [],
    "CLASS 12TH": [],
    "JUNIOR (6-8)": [],
    "HIGH SCHOOL (9-10)": [],
    "INTER (11-12)": [],
    "ALL (6th-12th)": ["919876543210"]  # पूरा स्कूल
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_broadcast', methods=['POST'])
def send_broadcast():
    data = request.json
    target = data.get('target', 'ALL (6th-12th)')
    message_text = data.get('message', '')
    media_link = data.get('link', '')

    if not message_text:
        return jsonify({"status": "error", "message": "संदेश खाली नहीं हो सकता!"}), 400

    # मैसेज फॉर्मेटिंग
    final_text = message_text
    if media_link:
        final_text += f"\n\n🔗 लिंक: {media_link}"

    # टारगेट ग्रुप के नंबर निकालना
    numbers_to_send = CONTACT_DATABASE.get(target, CONTACT_DATABASE["ALL (6th-12th)"])

    if not numbers_to_send:
        # अगर डेटाबेस खाली है, तो टेस्ट मोड में रिस्पॉन्स देगा
        return jsonify({
            "status": "success",
            "message": f"🚀 Broadcast simulated for {target}! (डेटाबेस में नंबर जोड़ें)"
        })

    # WhatsApp API URL
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    success_count = 0
    for phone in numbers_to_send:
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {"body": final_text}
        }
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=5)
            if res.status_code == 200:
                success_count += 1
        except Exception as e:
            print(f"Error sending to {phone}: {e}")

    return jsonify({
        "status": "success",
        "message": f"✅ {target} के {success_count} लोगों को व्हाट्सएप मैसेज भेज दिया गया!"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
  
