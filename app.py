from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai
from flask_cors import CORS
# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)
CORS(app)
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
        system_message = f"You are a helpful assistant with a {tone} tone. Please generate a response that is {length} in length."

        # Use OpenAI's latest API for chat completions
        completion = openai.chat.completions.create(
            model="gpt-4o",  # Replace with the correct model name
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )

        # Correctly access the response content
        response_content = completion.choices[0].message.content

        # Return the generated content as the response
        return jsonify({"response": response_content})

    except Exception as e:
        # Handle errors gracefully
        return jsonify({"error": str(e)}), 500

@app.route('/api/evaluate', methods=['POST'])
def evaluate_prompt():
    try:
        data = request.json
        prompt = data.get("prompt", "")

        # Evaluation criteria
        # Clarity: Checks if the prompt includes task-defining keywords or sufficient length.
        clarity_keywords = ["explain", "summarize", "describe", "list", "analyze", "write"]
        clarity = (
            "Clarity"
            if any(keyword in prompt.lower() for keyword in clarity_keywords) and len(prompt.split()) > 3
            else "Unclear"
        )

        # Specificity: Checks if the prompt provides sufficient context or detail.
        specificity = (
            "Specific"
            if len(prompt.split()) > 8 and any(char in prompt for char in ["?", ".", ":"])
            else "Vague"
        )

        # Structure: Checks if the prompt includes formatting cues or structural indicators.
        structure_keywords = ["bullet points", "steps", "format", "outline", ":"]
        structure = (
            "Well-structured"
            if any(keyword in prompt.lower() for keyword in structure_keywords)
            else "Needs Structure"
        )

        # Combine evaluation results
        feedback = [
            {"criterion": "Clarity", "score": clarity},
            {"criterion": "Specificity", "score": specificity},
            {"criterion": "Structure", "score": structure}
        ]

        return jsonify({"evaluation": feedback})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
