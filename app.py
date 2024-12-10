from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    tone = data.get('tone', 'neutral')
    length = data.get('length', 'medium')

    # Construct the prompt
    final_prompt = f"{prompt}\n\nTone: {tone}\nLength: {length}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace with the appropriate model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": final_prompt}
            ],
            max_tokens=150
        )
        return jsonify({"response": response['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
