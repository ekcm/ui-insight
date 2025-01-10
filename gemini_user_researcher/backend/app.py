from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import json

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Initialize FastAPI
app = FastAPI(title="UI Insight - WCAG & Usability Analyzer")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebLink(BaseModel):
    url: HttpUrl

class WCAGIssue(BaseModel):
    guideline: str
    issue: str

class AnalysisResponse(BaseModel):
    wcag_analysis: List[WCAGIssue] = []
    usability_insights: List[str] = []
    recommendations: List[str] = []

def fetch_webpage_content(url: str) -> str:
    try:
        response = requests.get(str(url))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.prettify()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching webpage: {str(e)}")

def analyze_with_gemini(content: str) -> Dict:
    prompt = f"""
    Analyze the following HTML content for WCAG compliance and usability. Provide a structured analysis following these exact guidelines:

    HTML Content to Analyze:
    {content[:15000]}

    Rules for Response Format:
    1. Respond ONLY with a JSON object
    2. Do not include any markdown formatting or code blocks
    3. Follow this exact structure:
    {{
        "wcag_analysis": [
            {{
                "guideline": "X.X.X Guideline Name",
                "issue": "Clear description of the issue"
            }}
        ],
        "usability_insights": [
            "Clear, concise usability observation (one sentence per insight)"
        ],
        "recommendations": [
            "Specific, actionable recommendation (one sentence per recommendation)"
        ]
    }}

    Guidelines for Content:
    1. WCAG issues should include the guideline number and a clear description
    2. Usability insights should be single, focused observations
    3. Recommendations should be specific and actionable
    4. All text should be clear and concise
    5. Do not use markdown formatting within the text
    6. Do not use code blocks or backticks in the text
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.candidates[0].content.parts[0].text.strip()
        
        # Clean up any potential markdown formatting
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        response_text = response_text.strip()
        
        try:
            analysis = json.loads(response_text)
            
            # Validate and clean the response
            cleaned_response = {
                "wcag_analysis": [
                    {
                        "guideline": str(item.get("guideline", "")).strip(),
                        "issue": str(item.get("issue", "")).strip().replace("`", "'")
                    }
                    for item in analysis.get("wcag_analysis", [])
                    if item.get("guideline") and item.get("issue")
                ],
                "usability_insights": [
                    str(insight).strip().replace("`", "'")
                    for insight in analysis.get("usability_insights", [])
                    if insight
                ],
                "recommendations": [
                    str(rec).strip().replace("`", "'")
                    for rec in analysis.get("recommendations", [])
                    if rec
                ]
            }
            
            return cleaned_response
            
        except json.JSONDecodeError:
            return {
                "wcag_analysis": [],
                "usability_insights": [],
                "recommendations": ["Error parsing analysis results. Please try again."]
            }
            
    except Exception as e:
        return {
            "wcag_analysis": [],
            "usability_insights": [],
            "recommendations": [f"Error during analysis: {str(e)}"]
        }

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