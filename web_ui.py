from flask import Flask, render_template_string, request, jsonify
from brain.llm import LLMBrain
from brain.rag import RAGBrain
from agents.manager import AgentManager

app = Flask(__name__)
brain = LLMBrain()
rag = RAGBrain()
manager = AgentManager()

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DharmaAI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 900px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 90vh;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 30px;
            text-align: center;
        }
        .header h1 { font-size: 28px; margin-bottom: 5px; }
        .header p { font-size: 14px; opacity: 0.9; }
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px 30px;
            background: #f8f9fa;
        }
        .message {
            margin-bottom: 20px;
            display: flex;
            animation: fadeIn 0.3s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .message.user { justify-content: flex-end; }
        .message.ai { justify-content: flex-start; }
        .bubble {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            font-size: 15px;
            line-height: 1.5;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        .user .bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        .ai .bubble {
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
            border-bottom-left-radius: 4px;
        }
        .input-container {
            padding: 20px 30px;
            background: white;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 10px;
        }
        .input-container input {
            flex: 1;
            padding: 14px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 15px;
            outline: none;
            transition: border-color 0.3s;
        }
        .input-container input:focus { border-color: #667eea; }
        .input-container button {
            padding: 14px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .input-container button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .typing {
            display: none;
            padding: 12px 18px;
            background: white;
            border-radius: 18px;
            border-bottom-left-radius: 4px;
            border: 1px solid #e0e0e0;
            width: fit-content;
        }
        .typing span {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #667eea;
            border-radius: 50%;
            margin: 0 2px;
            animation: typing 1.4s infinite;
        }
        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        .quick-commands {
            padding: 10px 30px;
            background: #f8f9fa;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .quick-commands button {
            padding: 6px 14px;
            background: white;
            border: 1px solid #667eea;
            color: #667eea;
            border-radius: 15px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .quick-commands button:hover {
            background: #667eea;
            color: white;
        }
        @media (max-width: 600px) {
            .container { height: 100vh; border-radius: 0; }
            .bubble { max-width: 85%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 DharmaAI</h1>
            <p>Personal AI Assistant with 17 Agents</p>
        </div>
        <div class="chat-container" id="chat">
            <div class="message ai">
                <div class="bubble">Hello! I am DharmaAI. How can I help you today?</div>
            </div>
        </div>
        <div class="quick-commands">
            <button onclick="quick('/system')">System</button>
            <button onclick="quick('/cpu')">CPU</button>
            <button onclick="quick('/ram')">RAM</button>
            <button onclick="quick('/disk')">Disk</button>
            <button onclick="quick('/agents')">Agents</button>
            <button onclick="quick('/backup list')">Backups</button>
            <button onclick="quick('/ping google.com')">Ping</button>
        </div>
        <div class="input-container">
            <input id="input" placeholder="Type a message..." onkeypress="if(event.key==='Enter')send()">
            <button onclick="send()">Send</button>
        </div>
    </div>
    <script>
        function quick(cmd) {
            document.getElementById('input').value = cmd;
            send();
        }
        function send() {
            let msg = document.getElementById('input').value.trim();
            if (!msg) return;
            
            let chat = document.getElementById('chat');
            chat.innerHTML += '<div class="message user"><div class="bubble">' + escapeHtml(msg) + '</div></div>';
            document.getElementById('input').value = '';
            chat.scrollTop = chat.scrollHeight;
            
            chat.innerHTML += '<div class="typing" id="typing"><span></span><span></span><span></span></div>';
            chat.scrollTop = chat.scrollHeight;
            
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            }).then(r => r.json()).then(d => {
                let typing = document.getElementById('typing');
                if (typing) typing.remove();
                chat.innerHTML += '<div class="message ai"><div class="bubble">' + escapeHtml(d.reply) + '</div></div>';
                chat.scrollTop = chat.scrollHeight;
            }).catch(err => {
                let typing = document.getElementById('typing');
                if (typing) typing.remove();
                chat.innerHTML += '<div class="message ai"><div class="bubble">Error: ' + err + '</div></div>';
            });
        }
        function escapeHtml(text) {
            let div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    cmd = message.lower()
    
    if cmd == '/agents':
        agents = manager.list_agents()
        reply = "Available Agents:\n" + "\n".join([f"  {n}: {d}" for n, d in agents])
    elif cmd == '/system':
        reply = manager.run("system info")
    elif cmd == '/cpu':
        reply = manager.run("cpu")
    elif cmd == '/ram':
        reply = manager.run("ram")
    elif cmd == '/disk':
        reply = manager.run("disk")
    elif cmd == '/process':
        reply = manager.run("process")
    elif cmd == '/backup list':
        reply = manager.run("backup list")
    elif cmd.startswith('/agent '):
        reply = manager.run(message[7:].strip())
    elif cmd.startswith('/web '):
        reply = manager.run(message[5:].strip())
    elif cmd.startswith('/ping '):
        reply = manager.run(f"ping -c 3 {message[6:].strip()}")
    elif cmd.startswith('/db '):
        reply = manager.run(f"database {message[4:].strip()}")
    elif cmd.startswith('/rag '):
        reply = rag.query(message[5:].strip())
    else:
        reply = brain.think(message)
    
    return jsonify({'reply': reply})

if __name__ == '__main__':
    print("🌐 DharmaAI Web UI: http://localhost:5000")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=5000, debug=False)
