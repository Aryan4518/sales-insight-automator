from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import google.generativeai as genai
import os
import smtplib
from email.mime.text import MIMEText

app = FastAPI(title="Sales Insight Automator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("AIzaSyA8pjH_7tQ4-8Bqt1-0izuRJG-dR71Webk"))

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), email: str = Form(...)):

    if not file.filename.endswith(".csv"):
        return {"error": "Only CSV allowed"}

    df = pd.read_csv(file.file)

    summary_data = df.describe().to_string()

    prompt = f"""
    Analyze this sales dataset and create an executive summary.

    {summary_data}

    Mention:
    - Top performing region
    - Highest revenue product
    - Any anomalies
    """

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt)

    summary = response.text

    send_email(email, summary)

    return {"summary": summary}


def send_email(receiver, message):

    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(message)

    msg["Subject"] = "Sales AI Summary"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())