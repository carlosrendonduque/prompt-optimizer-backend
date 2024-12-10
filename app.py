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

        # Construct the system message based on tone
        system_message = f"You are a helpful assistant with a {tone} tone."

        # Use OpenAI's latest API for chat completions
        completion = openai.chat.completions.create(
            model="gpt-4o",  # Replace with the correct model name (e.g., "gpt-4o-mini")
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )

        # Return the generated content as the response
        return jsonify({"response": completion["choices"][0]["message"]["content"]})

    except Exception as e:
        # Handle errors gracefully
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
