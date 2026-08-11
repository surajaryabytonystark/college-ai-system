// STARK LABS - MASTER WHATSAPP & SCHOOL AUTOMATION HUB
const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');

// 👑 OWNER CONTROL (SURAJ STARK)
const OWNER_NUMBER = "91XXXXXXXXXX@s.whatsapp.net"; // यहाँ अपना नंबर डालेंगे

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info_baileys');
    
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect } = update;
        if (connection === 'close') {
            const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log('कनेक्शन बंद हुआ, री-कनेक्ट हो रहा है...', shouldReconnect);
            if (shouldReconnect) connectToWhatsApp();
        } else if (connection === 'open') {
            console.log('🚀 STARK LABS AUTOMATION ACTIVE! कनेक्शन चालू है।');
        }
    });

    // ⚡ INSTANT MESSAGE LISTENER
    sock.ev.on('messages.upsert', async m => {
        const msg = m.messages[0];
        if (!msg.message || msg.key.fromMe) return;

        const from = msg.key.remoteJid;
        const text = msg.message.conversation || msg.message.extendedTextMessage?.text || '';

        // 👑 MASTER OVERRIDE COMMAND (केवल सूरज के लिए)
        if (text.startsWith('.broadcast ')) {
            const announcement = text.replace('.broadcast ', '');
            console.log('Master Announcement Fired:', announcement);
            // यहाँ से 0.1s में सारे स्पोर्ट्स और NCC ग्रुप्स में मैसेज जाएगा
        }
    });
}

connectToWhatsApp();
