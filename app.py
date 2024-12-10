from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)

# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        # Parse input from the POST request
        data = request.json
        prompt = data.get("prompt", "")
        tone = data.get("tone", "neutral")
        length = data.get("length", "medium")

        # Create a structured message prompt for chat completion
        messages = [
            {"role": "system", "content": f"You are a helpful assistant with a {tone} tone."},
            {"role": "user", "content": prompt}
        ]

        # Use the OpenAI Chat API to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Replace with the model you want to use, e.g., "gpt-4o" or "gpt-3.5-turbo"
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )

        # Return the generated content to the client
        return jsonify({"response": response["choices"][0]["message"]["content"]})

    except Exception as e:
        # Handle errors gracefully
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
