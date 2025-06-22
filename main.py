from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import requests, os, io
from dotenv import load_dotenv
from PIL import Image
import pytesseract
import pymupdf  # PyMuPDF
import docx

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_file(file: UploadFile):
    filename = file.filename.lower()
    content = ""

    if filename.endswith(".pdf"):
        pdf = pymupdf.open(stream=file.file.read(), filetype="pdf")
        content = "\n".join(page.get_text() for page in pdf)
    elif filename.endswith(".docx"):
        doc = docx.Document(file.file)
        content = "\n".join(p.text for p in doc.paragraphs)
    elif filename.endswith(".txt"):
        content = file.file.read().decode("utf-8")
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(io.BytesIO(file.file.read()))
        content = pytesseract.image_to_string(image)
    else:
        content = "Unsupported file type."

    return content

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body["message"]


    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )

    reply = response.json()["choices"][0]["message"]["content"]
    return {"response": reply}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    extracted = extract_text_from_file(file)
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Tell me about the document."},
            {"role": "user", "content": extracted}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )

    reply = response.json()["choices"][0]["message"]["content"]
    return {"response": reply}
