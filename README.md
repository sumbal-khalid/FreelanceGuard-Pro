# 🛡️ FreelanceGuard Pro — AI Safety Copilot for Freelancers

> AI-assisted risk assessment for freelance job posts, screenshots, and client reputation.

FreelanceGuard Pro helps freelancers identify potential warning signs in job posts and client messages before they commit. It accepts text, screenshots, and client information, then produces a structured risk report with evidence quotes, recommended actions, and a generated safe response.

Built for the **PakAngels GenAI & Agentic AI Final Hackathon — Cohort 11**.

---

## 🎯 Problem Statement

Freelancers on platforms like Upwork, Fiverr, and LinkedIn lose time and money to suspicious job posts. Common warning signs include unpaid test work, off-platform payment demands, upfront fees, sensitive information requests, unrealistic promises, urgency pressure, and vague requirements. Existing safety measures are fragmented and slow. FreelanceGuard Pro provides a unified, multi-modal workflow for risk assessment.

---

## ✨ Features

- 🔍 **Job Risk Analysis** — Classifies job posts as LOW / MEDIUM / HIGH
- 📸 **Multi-Modal Input** — Upload screenshots; text is auto-extracted via vision OCR
- 🚩 **Red Flag Detection** — 13 risk categories grounded in Upwork and FTC guidance
- 📌 **Evidence Extraction** — Quotes the exact text that triggered each flag
- 📖 **Plain-English Explanation** — Context-aware interpretation
- ✅ **Recommended Action** — Practical next steps
- ✉️ **Safe Response Generator** — Drafts professional replies
- 🕵️ **Client Reputation Analyzer** — Assesses client risk from provided information
- 📄 **PDF Report Export** — Full analysis exportable

---

## ⚙️ How It Works

Three-layer architecture: **Knowledge → Reasoning → Action**

1. **Knowledge Layer** — 13-category safety knowledge base in JSON, grounded in Upwork and FTC guidance.
2. **Reasoning Layer** — Groq LLaMA analyzes input (text or image), matches signals, and quotes evidence.
3. **Action Layer** — Produces a risk report, recommends next steps, generates a safe response.

---

## 🛠️ Tech Stack

- **UI:** Streamlit
- **LLM (Text):** Groq — `openai/gpt-oss-120b`
- **LLM (Vision/OCR):** Groq — `qwen/qwen3.8-27b`
- **Structured Output:** JSON mode
- **Determinism:** `temperature=0.0`, `seed=42`
- **Image Processing:** Pillow
- **PDF Export:** fpdf
- **Deployment:** Streamlit Community Cloud

---

## 💻 Local Setup

Prerequisites: Python 3.10+ and a free Groq API key from https://console.groq.com/keys

```bash
git clone https://github.com/sumbal-khalid/FreelanceGuard-Pro.git
cd FreelanceGuard
py -m pip install -r requirements.txt
echo GROQ_API_KEY=gsk_your_real_key_here > .env
py -m streamlit run App.py