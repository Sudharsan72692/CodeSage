import streamlit as st
import os
import google.generativeai as genai
import PyPDF2
import docx
import pandas as pd
import json
from src.code_analyzer import CodeAnalyzer
from src.flowchart_generator import FlowchartGenerator
from src.static_analyzer import StaticAnalyzer
from src.ai_code_detector import AICodeDetector  # AI Code Detector Import

API_KEY = "Your_api_key_here" 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.0-pro-exp-02-05")

# Function to extract text from PDF or DOCX files
def extract_text_from_file(uploaded_file):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension == "pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            return text
        elif file_extension == "docx":
            doc = docx.Document(uploaded_file)
            text = " ".join([para.text for para in doc.paragraphs])
            return text
    return ""

# Function to analyze multiple solutions
def analyze_solutions(problem_statement, solutions):
    results = []
    for uploaded_file in solutions:
        solution_text = extract_text_from_file(uploaded_file)
        team_name = uploaded_file.name.split(".")[0]  # Use filename as team name
        if solution_text:
            prompt = (
                f"Given the problem statement:\n{problem_statement}\n\n"
                f"Evaluate the following solution based on feasibility, creativity, and implementation ease. "
                f"Provide a score (0-100), a summary (50 words max), and list positives, negatives, feasibility, and implementation ease ratings (out of 10):\n\n"
                f"{solution_text}\n\n"
                "Respond strictly in JSON format:\n"
                "{'score': <integer>, 'summary': '<50-word summary>', "
                "'positives': '<positive aspects>', 'negatives': '<negative aspects>', "
                "'feasibility': <rating out of 10>, 'implementation_ease': <rating out of 10>}\n"
            )
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(prompt)
            if response and response.text:
                try:
                    response_json = json.loads(response.text.strip("```json\n").strip("```"))  # Ensure valid JSON
                    results.append({
                        "team": team_name,
                        "score": response_json.get("score", 0),
                        "summary": response_json.get("summary", "No summary available."),
                        "positives": response_json.get("positives", "N/A"),
                        "negatives": response_json.get("negatives", "N/A"),
                        "feasibility": response_json.get("feasibility", "N/A"),
                        "implementation_ease": response_json.get("implementation_ease", "N/A"),
                    })
                except json.JSONDecodeError:
                    results.append({
                        "team": team_name,
                        "score": -1,
                        "summary": "⚠️ AI response not in valid JSON format.",
                        "positives": "N/A",
                        "negatives": "N/A",
                        "feasibility": "N/A",
                        "implementation_ease": "N/A",
                    })

    results = [r for r in results if r["score"] >= 0]
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

# Function to handle code analysis
def analyze_code():
    st.header("🔹 Code Analyzer")
    code_input = st.text_area("Paste your Python/JavaScript code here:", height=200)
    if st.button("Analyze Code"):
        if code_input.strip():
            try:
                code_analyzer = CodeAnalyzer(API_KEY)
                flowchart_gen = FlowchartGenerator()
                static_analyzer = StaticAnalyzer()
                
                # Code Explanation
                explanation = code_analyzer.explain_code(code_input)
                st.subheader("📜 Code Explanation")
                st.write(explanation)
                
                # Flowchart Generation
                flowchart = flowchart_gen.generate_flowchart(code_input)
                st.subheader("📊 Code Flowchart")
                if flowchart:
                    st.graphviz_chart(flowchart)
                else:
                    st.warning("⚠️ Flowchart generation failed.")
                
                # Static Code Analysis
                issues = static_analyzer.analyze(code_input)
                st.subheader("🔍 Static Analysis Results")
                if issues:
                    for issue in issues:
                        st.warning(issue)
                else:
                    st.success("✅ No issues found in the code!")

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

# Function to check AI-generated code
def detect_ai_code():
    st.header("🤖 AI Code Detector")
    code_input = st.text_area("Paste the code to check if AI-generated:", height=200)
    if st.button("Check if AI-Generated"):
        if code_input.strip():
            try:
                ai_detector = AICodeDetector(API_KEY)
                result = ai_detector.is_ai_generated(code_input)
                st.subheader("🚀 AI-Generated Code Detection")
                st.write(result)
            except Exception as e:
                st.error(f"❌ Error detecting AI-generated code: {e}")

# Function to handle Hackathon evaluation
def hackathon_submission():
    st.header("🏆 Hackathon Submission & Evaluation")

    # Host uploads problem statement
    st.subheader("📜 Host: Upload Problem Statement")
    problem_file = st.file_uploader("Upload Problem Statement (PDF/DOCX)", type=["pdf", "docx"])
    problem_text = extract_text_from_file(problem_file) if problem_file else ""

    # Team Selection Options
    st.subheader("🎯 Team Selection Criteria")
    num_teams = st.number_input("Number of teams to be selected:", min_value=1, step=1)
    selection_type = st.radio("Selection type:", ["Per Theme", "Total Members"])

    # Participants Upload Solutions
    st.subheader("📂 Participants: Upload Solutions")
    solution_files = st.file_uploader("Upload Solution Files (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

    if st.button("📊 Analyze & Shortlist"):
        if problem_text and solution_files:
            results = analyze_solutions(problem_text, solution_files)

            if results:
                st.success("🏆 All Submitted Solutions & Scores")

                # 1️⃣ **Displaying Score for Each Solution**
                st.markdown("### 📊 Solution Scores")
                df_scores = pd.DataFrame(results, columns=["team", "score"])
                st.dataframe(df_scores)

                # 2️⃣ **Summarization for the Best Solution**
                best_solution = results[0]
                st.markdown("### 🏅 Best Solution Summary")
                st.subheader(f"🥇 {best_solution['team']} (Score: {best_solution['score']})")
                st.write(best_solution["summary"])

                # 3️⃣ **Comparison Table**
                st.markdown("### 📊 Solution Comparison Table")
                df_comparison = pd.DataFrame(results)
                st.dataframe(df_comparison)

                # 4️⃣ **Justification Statement for Best Solution (Updated Section)**
                st.markdown("### 🎯 Justification for Best Solution")

                # **Generating a justification using the best solution summary**
                best_summary = best_solution["summary"]
                justification_prompt = (
                    f"Analyze the following solution summary:\n{best_summary}\n\n"
                    f"Explain its necessity, how helpful it is, its impact, and its causes. "
                    "Break it down into the following:\n"
                    "- **Necessity:** Why is this solution needed?\n"
                    "- **Helpfulness:** How does it benefit people or solve a problem?\n"
                    "- **Impact:** What larger effects or improvements does it create?\n"
                    "- **Causes:** What factors or problems led to the creation of this solution?\n\n"
                    "Respond strictly in JSON format:\n"
                    "{'necessity': '<explanation>', 'helpfulness': '<explanation>', 'impact': '<explanation>', 'causes': '<explanation>'}"
                )

                chat_session = model.start_chat(history=[])
                justification_response = chat_session.send_message(justification_prompt)

                if justification_response and justification_response.text:
                    try:
                        justification_json = json.loads(justification_response.text.strip("```json\n").strip("```"))
                        necessity = justification_json.get("necessity", "N/A")
                        helpfulness = justification_json.get("helpfulness", "N/A")
                        impact = justification_json.get("impact", "N/A")
                        causes = justification_json.get("causes", "N/A")

                        st.write(f"**🔹 Necessity:** {necessity}")
                        st.write(f"**✅ Helpfulness:** {helpfulness}")
                        st.write(f"**📊 Impact:** {impact}")
                        st.write(f"**🛠 Causes:** {causes}")
                    except json.JSONDecodeError:
                        st.warning("⚠️ AI response was not in valid JSON format.")
                else:
                    st.warning("⚠️ AI couldn't generate a justification.")

            else:
                st.warning("⚠️ No valid solutions were analyzed.")
        else:
            st.warning("⚠️ Please upload both the problem statement and at least one solution.")

# Main function with sidebar navigation and project description
def main():
    st.sidebar.title("🔹 Select Feature")
    option = st.sidebar.radio("Choose an option:", ["Hackathon Evaluation", "Code Analyzer", "AI Code Detector"])

    # Adding About CodeSage section in the sidebar
    st.sidebar.markdown("---")
    st.sidebar.title("🧠 About CodeSage")
    st.sidebar.write(
        "CodeSage is an AI-powered platform designed to assist developers and hackathon participants with code analysis, "
        "flowchart generation, static code analysis, and AI-generated code detection. It also provides an intelligent system "
        "for evaluating hackathon solutions based on feasibility, creativity, and implementation ease."
    )
    st.sidebar.write(
        "With CodeSage, you can:\n"
        "- 🔍 Analyze your Python and JavaScript code\n"
        "- 📝 Generate visual flowcharts\n"
        "- 🚀 Detect AI-generated code\n"
        "- 🏆 Evaluate hackathon solutions\n"
    )
    st.sidebar.markdown("### 🚀 Enhance your coding experience with CodeSage!")

    if option == "Hackathon Evaluation":
        hackathon_submission()
    elif option == "Code Analyzer":
        analyze_code()
    elif option == "AI Code Detector":
        detect_ai_code()

if __name__ == "__main__":
    main()
