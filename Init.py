import os
from flask import Flask, render_template, request, Response
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    def generate():
        stream = anthropic.messages.create(
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_message}
            ],
            model="claude-3-opus-20240229",
            stream=True
        )
        for event in stream:
            if event.type == "content_block_delta":
                yield f"data: {event.delta.text}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
