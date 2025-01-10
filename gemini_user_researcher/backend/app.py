from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import google.generativeai as genai
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from typing import List

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Initialize FastAPI
app = FastAPI(title="UI Insight - WCAG & Usability Analyzer")

class WebLink(BaseModel):
    url: HttpUrl

class AnalysisResponse(BaseModel):
    wcag_analysis: List[dict]
    usability_insights: List[str]
    recommendations: List[str]

def fetch_webpage_content(url: str) -> str:
    try:
        response = requests.get(str(url))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.prettify()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching webpage: {str(e)}")

def analyze_with_gemini(content: str) -> dict:
    prompt = f"""
    Analyze the following HTML content for WCAG compliance and usability. Focus on:
    1. WCAG 2.1 compliance issues
    2. User interface usability concerns
    3. Specific recommendations for improvement
    
    HTML Content:
    {content[:15000]}  # Limiting content length for Gemini's context window
    
    Format your response as a JSON object with the following structure:
    {{
        "wcag_analysis": [
            {{"guideline": "WCAG guideline number", "issue": "Description of the issue"}}
        ],
        "usability_insights": ["List of usability observations"],
        "recommendations": ["List of specific recommendations"]
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.candidates[0].content.parts[0].text
        
        # Since we asked Gemini to return JSON, we need to parse it
        import json
        try:
            analysis = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback in case the response isn't proper JSON
            analysis = {
                "wcag_analysis": [],
                "usability_insights": [],
                "recommendations": [response_text]
            }
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing content: {str(e)}")

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_webpage(web_link: WebLink):
    # Fetch webpage content
    content = fetch_webpage_content(web_link.url)
    
    # Analyze with Gemini
    analysis = analyze_with_gemini(content)
    
    return AnalysisResponse(**analysis)

@app.get("/")
async def root():
    response = model.generate_content("How does AI work?")
    return {"response": response.candidates[0].content.parts[0].text}