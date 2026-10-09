from flask import Flask, render_template_string, request, jsonify
from brain.llm import LLMBrain
from brain.rag import RAGBrain
from agents.manager import AgentManager
import psutil

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
    <title>DharmaAI - Personal AI Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            background: #0a0a1a;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            overflow: hidden;
            position: relative;
        }
        
        /* Particle Canvas */
        #particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }
        
        /* 3D Animated Background */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            overflow: hidden;
        }
        
        .bg-animation .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.6;
            animation: float 20s infinite ease-in-out;
        }
        
        .bg-animation .orb:nth-child(1) {
            width: 500px;
            height: 500px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            top: -200px;
            left: -200px;
            animation-delay: 0s;
        }
        
        .bg-animation .orb:nth-child(2) {
            width: 400px;
            height: 400px;
            background: linear-gradient(135deg, #f093fb, #f5576c);
            bottom: -150px;
            right: -150px;
            animation-delay: -5s;
        }
        
        .bg-animation .orb:nth-child(3) {
            width: 300px;
            height: 300px;
            background: linear-gradient(135deg, #4facfe, #00f2fe);
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation-delay: -10s;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) scale(1); }
            25% { transform: translate(50px, -50px) scale(1.1); }
            50% { transform: translate(-30px, 30px) scale(0.9); }
            75% { transform: translate(30px, 50px) scale(1.05); }
        }
        
        /* Main Container */
        .container {
            position: relative;
            z-index: 1;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            box-shadow: 
                0 30px 80px rgba(0, 0, 0, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.1) inset,
                0 0 60px rgba(102, 126, 234, 0.3);
            width: 100%;
            max-width: 1000px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 90vh;
            transform-style: preserve-3d;
            transition: transform 0.3s ease;
        }
        
        /* Header */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            color: white;
            padding: 25px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: shine 3s infinite;
        }
        
        @keyframes shine {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .header h1 {
            font-size: 32px;
            margin-bottom: 8px;
            font-weight: 800;
            letter-spacing: 2px;
            text-shadow: 0 4px 15px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
        }
        
        .header p {
            font-size: 14px;
            opacity: 0.95;
            letter-spacing: 1px;
            position: relative;
            z-index: 1;
        }
        
        /* Live Stats Bar */
        .stats-bar {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 12px;
            position: relative;
            z-index: 1;
        }
        
        .stat-item {
            background: rgba(255,255,255,0.15);
            padding: 6px 14px;
            border-radius: 15px;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .stat-value {
            font-weight: 700;
            color: #fff;
        }
        
        /* Chat Container */
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 25px 30px;
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
            scroll-behavior: smooth;
        }
        
        .chat-container::-webkit-scrollbar { width: 8px; }
        .chat-container::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
        .chat-container::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 10px;
        }
        
        /* Messages */
        .message {
            margin-bottom: 20px;
            display: flex;
            animation: messageIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }
        
        @keyframes messageIn {
            from { opacity: 0; transform: translateY(30px) scale(0.9); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        
        .message.user { justify-content: flex-end; }
        .message.ai { justify-content: flex-start; }
        
        .bubble {
            max-width: 70%;
            padding: 15px 20px;
            border-radius: 20px;
            font-size: 15px;
            line-height: 1.6;
            word-wrap: break-word;
            white-space: pre-wrap;
            position: relative;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .bubble:hover { transform: translateY(-2px); }
        
        .user .bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 5px;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .ai .bubble {
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
            border-bottom-left-radius: 5px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }
        
        .ai .bubble .avatar {
            display: inline-block;
            width: 28px;
            height: 28px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            text-align: center;
            line-height: 28px;
            font-size: 14px;
            margin-right: 10px;
            vertical-align: middle;
        }
        
        /* Typing Indicator */
        .typing {
            display: none;
            padding: 15px 20px;
            background: white;
            border-radius: 20px;
            border-bottom-left-radius: 5px;
            border: 1px solid #e0e0e0;
            width: fit-content;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }
        
        .typing span {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            margin: 0 3px;
            animation: typing 1.4s infinite;
        }
        
        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0) scale(1); opacity: 0.6; }
            30% { transform: translateY(-12px) scale(1.2); opacity: 1; }
        }
        
        /* Quick Commands */
        .quick-commands {
            padding: 12px 30px;
            background: rgba(248, 249, 250, 0.9);
            backdrop-filter: blur(10px);
            border-top: 1px solid rgba(0,0,0,0.05);
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            overflow-x: auto;
        }
        
        .quick-commands button {
            padding: 8px 16px;
            background: white;
            border: 2px solid transparent;
            color: #667eea;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            white-space: nowrap;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
        }
        
        .quick-commands button:hover {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        /* Input Container */
        .input-container {
            padding: 20px 30px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-top: 1px solid rgba(0,0,0,0.05);
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .input-container input {
            flex: 1;
            padding: 16px 24px;
            border: 2px solid #e0e0e0;
            border-radius: 30px;
            font-size: 15px;
            outline: none;
            transition: all 0.3s ease;
            background: rgba(248, 249, 250, 0.8);
        }
        
        .input-container input:focus {
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1), 0 8px 25px rgba(102, 126, 234, 0.2);
            transform: translateY(-2px);
        }
        
        .voice-btn {
            padding: 16px 20px;
            background: linear-gradient(135deg, #f093fb, #f5576c);
            color: white;
            border: none;
            border-radius: 30px;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 8px 25px rgba(245, 87, 108, 0.4);
        }
        
        .voice-btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 12px 35px rgba(245, 87, 108, 0.5);
        }
        
        .voice-btn.listening {
            animation: pulse 1s infinite;
            background: linear-gradient(135deg, #f5576c, #f093fb);
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .input-container .send-btn {
            padding: 16px 32px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 30px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            letter-spacing: 0.5px;
        }
        
        .input-container .send-btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5);
        }
        
        /* Spinner */
        .spinner {
            display: none;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(102, 126, 234, 0.2);
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            body { padding: 0; }
            .container { height: 100vh; border-radius: 0; max-width: 100%; }
            .header h1 { font-size: 24px; }
            .stats-bar { gap: 10px; }
            .stat-item { padding: 4px 10px; font-size: 10px; }
            .bubble { max-width: 85%; font-size: 14px; }
            .quick-commands { padding: 10px 15px; }
            .input-container { padding: 15px; }
            .input-container input { padding: 14px 20px; }
            .input-container .send-btn { padding: 14px 24px; }
            .voice-btn { padding: 14px 16px; font-size: 16px; }
        }
    </style>
</head>
<body>
    <!-- Particle Canvas -->
    <canvas id="particles"></canvas>
    
    <!-- 3D Animated Background -->
    <div class="bg-animation">
        <div class="orb"></div>
        <div class="orb"></div>
        <div class="orb"></div>
    </div>
    
    <div class="container">
        <div class="header">
            <h1>🧠 DharmaAI</h1>
            <p>Personal AI Assistant with 20 Agents</p>
            <div class="stats-bar">
                <div class="stat-item">⚡ CPU: <span class="stat-value" id="cpu-stat">0%</span></div>
                <div class="stat-item">💾 RAM: <span class="stat-value" id="ram-stat">0%</span></div>
                <div class="stat-item">💿 Disk: <span class="stat-value" id="disk-stat">0%</span></div>
            </div>
        </div>
        
        <div class="chat-container" id="chat">
            <div class="message ai">
                <div class="bubble">
                    <span class="avatar">🧠</span>
                    Hello! I am DharmaAI. How can I help you today?
                </div>
            </div>
        </div>
        
        <div class="quick-commands">
            <button onclick="quick('/system')">🖥️ System</button>
            <button onclick="quick('/cpu')">⚡ CPU</button>
            <button onclick="quick('/ram')">💾 RAM</button>
            <button onclick="quick('/disk')">💿 Disk</button>
            <button onclick="quick('/agents')">🤖 Agents</button>
            <button onclick="quick('/backup list')">💾 Backups</button>
            <button onclick="quick('/ping google.com')">🌐 Ping</button>
            <button onclick="quick('/morning')">🌅 Morning</button>
            <button onclick="quick('/me')">👤 About Me</button>
        </div>
        
        <div class="input-container">
            <input id="input" placeholder="Type a message..." onkeypress="if(event.key==='Enter')send()">
            <button class="voice-btn" id="voiceBtn" onclick="startVoice()" title="Voice input">🎤</button>
            <div class="spinner" id="spinner"></div>
            <button class="send-btn" onclick="send()">Send ➤</button>
        </div>
    </div>
    
    <script>
        // ==================== PARTICLE EFFECTS ====================
        const canvas = document.getElementById('particles');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const particles = [];
        for (let i = 0; i < 60; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 1,
                color: ['#667eea', '#764ba2', '#f093fb', '#4facfe'][Math.floor(Math.random() * 4)]
            });
        }
        
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => {
                p.x += p.vx;
                p.y += p.vy;
                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
                
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fillStyle = p.color + '99';
                ctx.fill();
            });
            requestAnimationFrame(animate);
        }
        animate();
        
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
        
        // ==================== VOICE INPUT ====================
        function startVoice() {
            if (!('webkitSpeechRecognition' in window)) {
                alert('Voice not supported in this browser');
                return;
            }
            const recognition = new webkitSpeechRecognition();
            recognition.lang = 'en-US';
            recognition.continuous = false;
            recognition.interimResults = false;
            
            const voiceBtn = document.getElementById('voiceBtn');
            voiceBtn.classList.add('listening');
            
            recognition.onresult = (e) => {
                document.getElementById('input').value = e.results[0][0].transcript;
                voiceBtn.classList.remove('listening');
                send();
            };
            
            recognition.onerror = (e) => {
                voiceBtn.classList.remove('listening');
                alert('Voice error: ' + e.error);
            };
            
            recognition.onend = () => {
                voiceBtn.classList.remove('listening');
            };
            
            recognition.start();
        }
        
        // ==================== LIVE STATS ====================
        function updateStats() {
            fetch('/stats')
                .then(r => r.json())
                .then(d => {
                    document.getElementById('cpu-stat').textContent = d.cpu + '%';
                    document.getElementById('ram-stat').textContent = d.ram + '%';
                    document.getElementById('disk-stat').textContent = d.disk + '%';
                })
                .catch(() => {});
        }
        updateStats();
        setInterval(updateStats, 3000);
        
        // ==================== CHAT ====================
        function quick(cmd) {
            document.getElementById('input').value = cmd;
            send();
        }
        
        function send() {
            let msg = document.getElementById('input').value.trim();
            if (!msg) return;
            
            let chat = document.getElementById('chat');
            let spinner = document.getElementById('spinner');
            let sendBtn = document.querySelector('.send-btn');
            
            chat.innerHTML += '<div class="message user"><div class="bubble">' + escapeHtml(msg) + '</div></div>';
            document.getElementById('input').value = '';
            chat.scrollTop = chat.scrollHeight;
            
            spinner.style.display = 'block';
            sendBtn.disabled = true;
            sendBtn.style.opacity = '0.6';
            
            chat.innerHTML += '<div class="typing" id="typing"><span></span><span></span><span></span></div>';
            chat.scrollTop = chat.scrollHeight;
            
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            })
            .then(r => r.json())
            .then(d => {
                let typing = document.getElementById('typing');
                if (typing) typing.remove();
                chat.innerHTML += '<div class="message ai"><div class="bubble"><span class="avatar">🧠</span>' + escapeHtml(d.reply) + '</div></div>';
                chat.scrollTop = chat.scrollHeight;
            })
            .catch(err => {
                let typing = document.getElementById('typing');
                if (typing) typing.remove();
                chat.innerHTML += '<div class="message ai"><div class="bubble"><span class="avatar">⚠️</span>Error: ' + escapeHtml(err.toString()) + '</div></div>';
            })
            .finally(() => {
                spinner.style.display = 'none';
                sendBtn.disabled = false;
                sendBtn.style.opacity = '1';
            });
        }
        
        function escapeHtml(text) {
            let div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        document.getElementById('input').focus();
        
        // 3D parallax effect
        document.addEventListener('mousemove', (e) => {
            let container = document.querySelector('.container');
            let x = (e.clientX / window.innerWidth - 0.5) * 8;
            let y = (e.clientY / window.innerHeight - 0.5) * 8;
            container.style.transform = `perspective(1000px) rotateY(${x}deg) rotateX(${-y}deg)`;
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/stats')
def stats():
    return jsonify({
        'cpu': psutil.cpu_percent(),
        'ram': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent
    })

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
    elif cmd == '/morning':
        reply = "Morning Briefing:\n"
        reply += f"System: {manager.run('system info')}\n"
        reply += f"CPU: {manager.run('cpu')}\n"
        reply += f"RAM: {manager.run('ram')}\n"
        reply += f"Disk: {manager.run('disk')}\n"
        reply += f"Backup: {manager.run('backup list')}"
    elif cmd == '/me':
        reply = rag.query("Who is Kaliyuga? What are his goals and skills?")
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
