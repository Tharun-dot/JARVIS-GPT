from flask import Flask, request, render_template, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Ensure the API key is set
api_key = os.getenv("GROQ_API_KEY")
if api_key is None:
    raise ValueError("API key is not set in environment variables")

client = Groq(api_key=api_key)

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
