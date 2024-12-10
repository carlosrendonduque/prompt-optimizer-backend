from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai
from flask_cors import CORS
import anthropic

# Load environment variables
load_dotenv()
#anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
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


@app.route('/api/computer_use', methods=['POST'])
def computer_use():
    try:
        # Parse user input
        data = request.json
        user_prompt = data.get("prompt", "")
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        # Send request to Anthropic API
        response = client.beta.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=[
                {
                    "type": "computer_20241022",
                    "name": "computer",
                    "display_width_px": 1024,
                    "display_height_px": 768,
                    "display_number": 1,
                },
                {
                    "type": "text_editor_20241022",
                    "name": "str_replace_editor",
                },
                {
                    "type": "bash_20241022",
                    "name": "bash",
                },
            ],
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            betas=["computer-use-2024-10-22"],
        )

        # Extract the relevant tool input from the response content
        tool_input = None
        for block in response.content:
            # Check if the block is a BetaToolUseBlock
            if hasattr(block, "type") and block.type == "tool_use":
                tool_input = block.input
                break

        # If no tool input is found, return an appropriate error
        if not tool_input:
            return jsonify({"error": "No tool input found in the response"}), 400

        # Simulate using the tool (e.g., create a file or execute a command)
        result = execute_tool(tool_input)

        return jsonify({"tool_input": tool_input, "tool_result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


import os

def execute_tool(tool_input):
    """
    Executes the tool command based on the provided input.
    """
    try:
        command = tool_input.get("command")
        path = tool_input.get("path")
        file_text = tool_input.get("file_text")

        # Simulate file creation as an example
        if command == "create" and path and file_text:
            # Ensure the directory exists
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Create the file
            with open(path, "w") as f:
                f.write(file_text)
            return f"File '{path}' created successfully with content: {file_text}"

        return "Tool command not recognized or incomplete"
    except Exception as e:
        return f"Error executing tool: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
