from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

# Assuming chatbot.backend is updated to use the new build_graph
from chatbot.backend import ChatbotManager 

app = Flask(__name__)
# Secret key is REQUIRED to use sessions
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key-123")
manager = None

def get_manager():
    global manager
    if manager is None:
        manager = ChatbotManager()
    return manager

@app.route('/auth/signup', methods=['POST'])
def handle_signup():
    data = request.json
    success, msg = auth.signup(data.get('username'), data.get('password'))
    return jsonify({'success': success, 'message': msg})

@app.route('/auth/login', methods=['POST'])
def handle_login():
    data = request.json
    if auth.login(data.get('username'), data.get('password')):
        session['user'] = data.get('username')
        return jsonify({'success': True, 'message': "Logged in!"})
    return jsonify({'success': False, 'message': "Invalid credentials."}), 401

@app.route('/auth/logout', methods=['POST'])
def handle_logout():
    session.pop('user', None)  # Clears the user from the session
    return jsonify({'success': True})

@app.route('/chat', methods=['POST'])
def chat():
    if 'user' not in session:
        return jsonify({'error': 'Please log in first.'}), 401
    
    try:
        data = request.json
        # Link history to the specific user via thread_id
        config = {"configurable": {"thread_id": session['user']}}
        response = get_manager().get_response(data.get('message', ''), config)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        response = get_manager().get_response(message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gemini Multi-Source RAG</title>
        <style>
            body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
            h1 { color: #1f2937; }
            p { color: #6b7280; }
            #chat-box { height: 400px; border: 1px solid #ccc; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .user { background-color: #e3f2fd; text-align: right; }
            .bot { background-color: #f5f5f5; }
            .error { background-color: #fee; color: #c33; }
            #input-area { display: flex; gap: 10px; }
            input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
            button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <h1>Gemini Multi-Source RAG</h1>
        <p>I am powered by Google Gemini. Ask me about Airline Policies or Stories!</p>
        <div id="chat-box"></div>
        <div id="input-area">
            <input type="text" id="message-input" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
        </div>
        <script>
            function sendMessage() {
                const input = document.getElementById('message-input');
                const message = input.value.trim();
                if (!message) return;
                
                const chatBox = document.getElementById('chat-box');
                chatBox.innerHTML += '<div class="message user">' + escapeHtml(message) + '</div>';
                input.value = '';
                
                fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                })
                .then(r => r.json())
                .then(data => {
                    if (data.error) {
                        chatBox.innerHTML += '<div class="message bot error">Error: ' + escapeHtml(data.error) + '</div>';
                    } else {
                        chatBox.innerHTML += '<div class="message bot">' + escapeHtml(data.response) + '</div>';
                    }
                    chatBox.scrollTop = chatBox.scrollHeight;
                })
                .catch(e => {
                    chatBox.innerHTML += '<div class="message bot error">Network error: ' + e + '</div>';
                    chatBox.scrollTop = chatBox.scrollHeight;
                });
            }
            
            function escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
            
            document.getElementById('message-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv('GOOGLE_API_KEY'):
        print("\n⚠️  WARNING: GOOGLE_API_KEY not found in environment.")
        print("   Please set GOOGLE_API_KEY in your .env file or environment.")
        print("   Get your API key from: https://ai.google.dev/\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)