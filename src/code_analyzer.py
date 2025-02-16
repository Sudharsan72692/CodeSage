import os
import ast
import google.generativeai as genai

class CodeAnalyzer:
    def __init__(self, api_key):
        os.environ["GEMINI_API_KEY"] = api_key
        genai.configure(api_key=api_key)

        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-pro-exp-02-05",
            generation_config=self.generation_config,
        )

    def explain_code(self, code_snippet):
        try:
            ast.parse(code_snippet)  # Validate syntax before processing

            prompt = f"Explain the following  code in simple terms and also provide the flowchart for the code:\n\n{code_snippet}"
            chat_session = self.model.start_chat(history=[])
            response = chat_session.send_message(prompt)

            return response.text if response else "Error: No explanation generated."
        except Exception as e:
            return f"Error analyzing code: {str(e)}"
