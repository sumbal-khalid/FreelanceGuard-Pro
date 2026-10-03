import os
import json
import base64
from groq import Groq
from dotenv import load_dotenv
from prompts import ANALYSIS_PROMPT, RESPONSE_PROMPT, OCR_PROMPT, REPUTATION_PROMPT

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TEXT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "qwen/qwen3.8-27b"


def load_knowledge_base():
    with open("knowledge_base.json", "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_job(user_input: str) -> dict:
    """Analyze a job post or client message for risk signals."""
    kb = load_knowledge_base()
    prompt = ANALYSIS_PROMPT.format(
        knowledge_base=json.dumps(kb),
        user_input=user_input
    )
    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.0,
        top_p=1.0,
        seed=42
    )
    return json.loads(response.choices[0].message.content)


def generate_response(user_input: str, analysis: dict, action: str) -> str:
    """Generate a professional response message based on the risk analysis."""
    prompt = RESPONSE_PROMPT.format(
        action=action,
        analysis=json.dumps(analysis),
        user_input=user_input
    )
    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        top_p=1.0,
        seed=42
    )
    return response.choices[0].message.content


def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract text from an uploaded image using Groq's vision model."""
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": OCR_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.0,
        max_tokens=2000
    )

    extracted = response.choices[0].message.content.strip()

    if extracted == "NO_TEXT_FOUND" or len(extracted) < 5:
        return ""
    return extracted


def analyze_reputation(client_info: str) -> dict:
    """Analyze client reputation based on provided information."""
    prompt = REPUTATION_PROMPT.format(client_info=client_info)
    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.0,
        top_p=1.0,
        seed=42
    )
    return json.loads(response.choices[0].message.content)