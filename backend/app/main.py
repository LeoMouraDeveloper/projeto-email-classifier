# app/main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from .gemini_classifier import GeminiEmailClassifier
import PyPDF2
import io
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

app = FastAPI(title="Email Classifier API - Gemini Edition", version="3.0")

# Configurar CORS para desenvolvimento e produção
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens temporariamente
    allow_credentials=False,  # Mudado para False quando origins=["*"]
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Inicializar classificador (pode falhar se Gemini não configurado)
try:
    classifier = GeminiEmailClassifier()
except Exception as e:
    print(f"❌ Erro ao inicializar classificador: {e}")
    classifier = None

@app.get("/health")
async def health():
    """Endpoint de saúde com informações do sistema"""
    if not classifier:
        return {
            "status": "error",
            "message": "Classificador não configurado - verifique GEMINI_API_KEY"
        }
    
    status = classifier.get_status()
    return {
        "status": "ok",
        "version": "3.0",
        "classifier": "Gemini-only",
        "gemini": f"✅ {status['status'].title()}",
        "modelo": status['modelo']
    }

@app.get("/system_info")
async def system_info():
    """Informações detalhadas do sistema de classificação"""
    if not classifier:
        return {
            "error": "Classificador não configurado",
            "solution": "Configure GEMINI_API_KEY no arquivo .env"
        }
    
    status = classifier.get_status()
    return {
        "version": "3.0-gemini-only",
        "components": {
            "gemini": "✅ Ativo" if status['status'] == 'ativo' else "❌ Inativo",
            "sklearn": "🗑️ Removido (não necessário)",
            "nltk": "🗑️ Removido (não necessário)"
        },
        "features": status['recursos'],
        "accuracy_expected": "90-95%",
        "performance": "Ultra-rápido",
        "modelo": status['modelo']
    }

@app.post("/process_email")
async def process_email(text: Optional[str] = Form(default=None), file: Optional[UploadFile] = File(default=None)):
    """
    Recebe:
      - campo form 'text' (texto do email) OR
      - upload de arquivo .txt ou .pdf (campo 'file')
    Retorna JSON com categoria, confiança e resposta sugerida.
    
    Versão 3.0: Usa apenas Google Gemini para máxima precisão e simplicidade
    """
    if not classifier:
        raise HTTPException(
            status_code=500, 
            detail="Classificador não configurado. Verifique GEMINI_API_KEY no arquivo .env"
        )
    
    print(f"DEBUG: text recebido: {repr(text)}")
    print(f"DEBUG: file recebido: {file}")
    
    # Verificar se text está vazio ou None
    if text is not None and text.strip() == "":
        text = None
    
    if not text and not file:
        print("DEBUG: Nenhum texto ou arquivo fornecido")
        raise HTTPException(status_code=400, detail="Envie 'text' (form field) ou um arquivo 'file' (.txt ou .pdf).")

    if file:
        filename = file.filename.lower()
        content = await file.read()
        if filename.endswith(".pdf"):
            try:
                reader = PyPDF2.PdfReader(io.BytesIO(content))
                pages = []
                for page in reader.pages:
                    txt = page.extract_text()
                    if txt:
                        pages.append(txt)
                text = "\n".join(pages)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Erro ao ler PDF: {e}")
        elif filename.endswith(".txt"):
            text = content.decode("utf-8", errors="ignore")
        else:
            raise HTTPException(status_code=400, detail="Formato não suportado. Use .txt ou .pdf.")

    result = classifier.classify_and_respond(text)
    return result
