import os
import google.generativeai as genai

class AICodeDetector:
    def __init__(self, api_key):
        os.environ["GEMINI_API_KEY"] = api_key
        genai.configure(api_key=api_key)

        self.generation_config = {
            "temperature": 0.5,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 100,
            "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-pro-exp-02-05",
            generation_config=self.generation_config,
        )

    def is_ai_generated(self, code_snippet):
        prompt = (
    "Analyze the following code and determine whether it was generated by an AI, "
    "such as ChatGPT, Gemini, or Copilot, based on structure, comments, and style. "
    "Provide a one-word answer (Yes/No) followed by a confidence score (0-100). "
    "Explain briefly if possible.\n\n"
    f"{code_snippet}"
)
        
        chat_session = self.model.start_chat(history=[])
        response = chat_session.send_message(prompt)

        return response.text.strip() if response else "Error: No response generated."
