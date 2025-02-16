# CodeSage 🚀

## Overview
CodeSage is an AI-powered platform designed to enhance code analysis, generate flowcharts, perform static code analysis, and detect AI-generated code. It also features an AI-driven hackathon evaluation system that scores and ranks solutions based on feasibility, creativity, and implementation ease.

## Features
- **Code Analyzer** – AI-powered explanation of Python/JavaScript code.
- **Flowchart Generator** – Convert code into structured flowcharts.
- **Static Code Analysis** – Detect potential issues and enhance code quality.
- **AI Code Detector** – Identify AI-generated code snippets.
- **Hackathon Evaluation** – AI-driven scoring and ranking of hackathon submissions.

## Getting Started

### Use Python 3.9+
Ensure you have Python 3.9 or later installed. You can check your Python version with:
```python
python --version
```

### Create a Virtual Environment (Recommended)
Set up a virtual environment to manage dependencies:
```python
python -m venv venv
```
Activate the virtual environment:
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```powershell
  venv\Scripts\activate
  ```

### Install Dependencies
Install required libraries:
```python
pip install -r requirements.txt
```

### Set Up API Key
You need a **Google Gemini AI API key** to use AI-powered features.
1. Get your API key from **Google Generative AI**.
2. Open `main.py` and replace `Your_api_key` with your actual API key.

### Run the Application
Start CodeSage with Streamlit:
```python
streamlit run main.py
```
Now, open the link displayed in the terminal (usually `http://localhost:8501`) and start using CodeSage.

## Project Structure
```
codesage/
│
├── src/
│   ├── code_analyzer.py        # AI-powered code explanation
│   ├── flowchart_generator.py  # Converts code to flowchart
│   ├── static_analyzer.py      # Performs static code analysis
│   ├── ai_code_detector.py     # Detects AI-generated code
│
├── requirements.txt            # Required Python libraries
├── main.py                     # Streamlit app entry point
├── README.md                   # Project documentation
```

## Requirements
This project requires **Python 3.9+** and the following dependencies:
- `streamlit`
- `transformers`
- `torch`
- `graphviz`
- `pylint`
- `matplotlib`
- `google-generativeai`
- `PyPDF2`
- `python-docx`

Install dependencies:
```python
pip install -r requirements.txt
```

## How to Use?
### Code Analyzer
1. Paste **Python/JavaScript** code.
2. Get **AI-powered explanation**.
3. View a **flowchart representation** of the code.
4. Perform **static analysis**.

### AI Code Detector
1. Paste any code snippet.
2. Check if it is **AI-generated**.

### Hackathon Evaluation
1. **Hosts** upload a problem statement.
2. **Participants** submit solutions (PDF/DOCX).
3. AI **scores and ranks** the submissions.

## Sidebar Content
The sidebar provides quick access to CodeSage functionalities:
- **Code Analyzer** – Understand and improve your code.
- **AI Code Detector** – Identify AI-generated solutions.
- **Hackathon Evaluation** – Rank solutions effectively.

## Screenshots
(Add relevant screenshots here, if available.)

## License
This project is licensed under the **MIT License**.

## Credits
Developed with ❤️ using **Python, Streamlit, and AI models**.

## Contact
For any queries, reach out to **sudharsanmv7@gmail.com**.
