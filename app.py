from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve the OpenAI API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    tone = data.get('tone', 'neutral')
    length = data.get('length', 'medium')

    # Construct the prompt
    final_prompt = f"{prompt}\n\nTone: {tone}\nLength: {length}"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=final_prompt,
            max_tokens=150
        )
        return jsonify({"response": response.choices[0].text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
