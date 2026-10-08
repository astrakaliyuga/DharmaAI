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
<html>
<head>
    <title>DharmaAI</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; background: #f0f0f0; }
        h1 { color: #333; }
        #chat { border: 1px solid #ccc; padding: 20px; height: 400px; overflow-y: scroll; margin-bottom: 10px; background: white; border-radius: 10px; }
        .user { color: blue; margin: 10px 0; }
        .ai { color: green; margin: 10px 0; }
        input { width: 80%; padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
        button { padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #45a049; }
    </style>
</head>
<body>
    <h1>🧠 DharmaAI</h1>
    <p>Personal AI Assistant with 7 Agents</p>
    <div id="chat"></div>
    <input id="input" placeholder="Type here..." onkeypress="if(event.key==='Enter')send()">
    <button onclick="send()">Send</button>
    <script>
        function send() {
            let msg = document.getElementById('input').value;
            if (!msg) return;
            document.getElementById('chat').innerHTML += '<div class="user"><b>You:</b> ' + msg + '</div>';
            document.getElementById('input').value = '';
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            }).then(r => r.json()).then(d => {
                document.getElementById('chat').innerHTML += '<div class="ai"><b>AI:</b> ' + d.reply + '</div>';
                document.getElementById('chat').scrollTop = 99999;
            });
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
    reply = brain.think(message)
    return jsonify({'reply': reply})

if __name__ == '__main__':
    print("🌐 DharmaAI Web UI: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
