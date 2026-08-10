from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Murari Dispatcher Server is Live!"

# Webhook Verification Endpoint for Meta
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == 'suraj_dispatcher_secret':
        return challenge, 200
    return 'Forbidden', 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
  
