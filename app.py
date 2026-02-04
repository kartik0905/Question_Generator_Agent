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

