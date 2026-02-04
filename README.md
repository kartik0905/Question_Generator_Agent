# AI Educational Content Pipeline
### Generator–Reviewer Architecture

![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Gemini](https://img.shields.io/badge/Google-Gemini%20API-orange)
![Gradio](https://img.shields.io/badge/UI-Gradio%20Compatible-brightgreen)

---

## 📘 Overview

**AI Educational Content Pipeline** is a Python-based application that generates **high-quality educational explanations and quizzes** using a **multi-agent AI architecture**.

The system follows a **Generator–Reviewer pattern**, where:
- A **Generator Agent** creates educational content.
- A **Reviewer Agent** evaluates the content for **accuracy, clarity, and age-appropriateness**.
- If the content fails review, an **automatic refinement loop** is triggered until the output meets quality standards.

This architecture ensures **reliable, structured, and production-ready educational content**, making the project suitable for real-world AI applications.

---

## ✨ Key Features

- **Dual-Agent System**  
  Implements a Generator–Reviewer architecture to ensure content quality.

- **Self-Correcting Feedback Loop**  
  Automatically refines content based on reviewer feedback.

- **Structured Output with Pydantic**  
  Enforces strict JSON schemas and reliable LLM responses.

- **Cost-Effective Design**  
  Optimized to work within the **Google Gemini Free Tier**.

- **Interactive UI**  
  Built with Streamlit for fast iteration and usability.

---

## 🛠 Tech Stack

- **Python** – Core backend logic  
- **Streamlit** – Interactive frontend  
- **Google Gemini API** (`gemini-flash-latest`) – LLM provider  
- **Pydantic** – Data validation and schema enforcement  
- **uv** – Fast dependency and environment management  

---

## ⚙️ How It Works

1. **User Input**  
   The user provides a topic and target age group via the Streamlit UI.

2. **Generator Agent**  
   Produces structured educational explanations and quiz questions.

3. **Reviewer Agent**  
   Critiques the generated content for correctness and suitability.

4. **Refinement Loop**  
   If issues are found, feedback is sent back to the Generator for correction.

5. **Final Output**  
   Only approved, high-quality content is displayed to the user.

---

## 📂 Project Structure

```bash
.
├── app.py              # Streamlit application entry point
├── agents/             # Generator and Reviewer agent logic
│   ├── generator.py
│   └── reviewer.py
├── models/             # Pydantic schemas
│   └── schemas.py
├── utils/              # Helper functions
├── .env.example        # Environment variable template
├── pyproject.toml      # uv configuration
└── README.md
```

---

## 🚀 Installation

> This project uses **uv** for dependency management.

```bash
# Clone the repository
git clone https://github.com/kartik0905/Question_Generator_Agent.git
cd Question_Generator_Agent
```

```bash
# Initialize uv (if needed)
uv init
```

```bash
# Install dependencies
uv add streamlit pydantic google-generativeai python-dotenv
```

```bash
# Create environment file
touch .env
```

Add the following to your `.env` file:

```env
GEMINI_API_KEY=your_key_here
```

---

## ▶️ Usage

Run the Streamlit application:

```bash
uv run streamlit run app.py
```

Open your browser and start generating AI-reviewed educational content.

---

## 🎯 Use Case & Motivation

This project demonstrates:
- Practical **multi-agent AI workflows**
- Safe and reliable **LLM-driven content generation**
- Strong **software engineering practices** using validation and feedback loops

It is designed to showcase **production-oriented AI system design**, making it suitable for **developer internship or research submissions**.

---

## 📜 License

This project is licensed under the MIT License.

---

**Built with ❤️ using Python, Streamlit, and Google Gemini**
