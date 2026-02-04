import streamlit as st
import json
import os
import time
from pydantic import BaseModel, ValidationError
from typing import List, Literal
from dotenv import load_dotenv


try:
    import google.generativeai as genai
except ImportError:
    genai = None


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY and genai:
    genai.configure(api_key=API_KEY)


class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str

class GeneratorResponse(BaseModel):
    explanation: str
    mcqs: List[MCQ]

class ReviewerResponse(BaseModel):
    status: Literal["pass", "fail"]
    feedback: List[str]


def call_gemini(role: str, prompt: str, response_model: type) -> str:
    """
    Calls Gemini 1.5 Flash with native JSON schema enforcement.
    """
    if API_KEY and genai:
        try:
            model = genai.GenerativeModel(
                'gemini-flash-latest',
                generation_config={
                    "response_mime_type": "application/json",
                    "response_schema": response_model
                }
            )
            
            chat = model.start_chat(history=[])
            response = chat.send_message(
                f"You are a {role} agent for an educational system. {prompt}"
            )
            return response.text
        except Exception as e:
            st.error(f"Gemini API Error: {e}")
            return "{}"
    else:
        time.sleep(1)
        if role == "generator":
            return json.dumps({
                "explanation": "MOCK: Gemini Key missing. Angles are formed by two rays.",
                "mcqs": [{"question": "Angle < 90?", "options": ["Acute", "Obtuse"], "answer": "Acute"}]
            })
        elif role == "reviewer":
            if "CRITICAL FEEDBACK" in prompt:
                return json.dumps({"status": "pass", "feedback": ["Looks good now."]})
            return json.dumps({"status": "fail", "feedback": ["(Mock) Too complex.", "(Mock) Add example."]})
        
def generator_agent(grade: int, topic: str, feedback: List[str] = None) -> GeneratorResponse:
    prompt = f"Generate content for Grade {grade} on topic '{topic}'."
    if feedback:
        prompt += f"\n\nCRITICAL FEEDBACK TO ADDRESS: {feedback}"
    
    response_text = call_gemini("generator", prompt, GeneratorResponse)
    
    try:
        return GeneratorResponse.model_validate_json(response_text)
    except ValidationError:
        return GeneratorResponse(explanation="Error parsing JSON", mcqs=[])

def reviewer_agent(content: GeneratorResponse, grade: int) -> ReviewerResponse:
    prompt = f"""
    Review this content for Grade {grade}:
    {content.model_dump_json()}
    
    Check for: 1. Age appropriateness 2. Clarity 3. Correctness.
    """
    response_text = call_gemini("reviewer", prompt, ReviewerResponse)
    
    try:
        return ReviewerResponse.model_validate_json(response_text)
    except ValidationError:
        return ReviewerResponse(status="fail", feedback=["Error parsing Reviewer JSON"])

st.set_page_config(page_title="Gemini Agent Pipeline", page_icon="✨")

st.title("✨ AI Agent Pipeline (Gemini)")
st.caption("Using: " + ("Gemini 1.5 Flash ⚡" if API_KEY else "Mock Mode (Add GEMINI_API_KEY to .env)"))

with st.sidebar:
    st.header("Config")
    grade = st.slider("Grade Level", 1, 12, 4)
    topic = st.text_input("Topic", "Solar System")
    btn = st.button("Start Pipeline", type="primary")

if btn:
    with st.status("Running Agents...", expanded=True) as status:
        
        st.write(" **Generator:** Drafting content...")
        content = generator_agent(grade, topic)
        st.json(content.model_dump())
        
        st.write(" **Reviewer:** Validating...")
        review = reviewer_agent(content, grade)
        
        if review.status == "pass":
            st.success("Content Passed!")
            final_content = content
        else:
            st.warning(f" Review Failed: {review.feedback}")
            st.write("🔧 **Refining:** Sending back to Generator...")
            
            final_content = generator_agent(grade, topic, review.feedback)
            st.success("Refined Content Generated")
            
        status.update(label="Workflow Complete", state="complete")

    st.divider()
    st.subheader("Final Output")
    st.write(final_content.explanation)
    for q in final_content.mcqs:
        st.info(f"**Q:** {q.question}\n\nAnswer: {q.answer}")