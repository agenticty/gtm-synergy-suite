from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from agents.askgtm import AskGTMAgent
import json

router = APIRouter(prefix="/askgtm", tags=["AskGTM"])

# Initialize agent (singleton)
agent = AskGTMAgent()

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: List[dict]

class DocumentUpload(BaseModel):
    text: str
    metadata: Optional[dict] = None

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question to the GTM knowledge base"""
    try:
        result = agent.ask(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_conversation():
    """Reset conversation history"""
    try:
        agent.reset_conversation()
        return {"message": "Conversation reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-document")
async def add_document(doc: DocumentUpload):
    """Add a new document to knowledge base"""
    try:
        agent.add_documents([doc.text], [doc.metadata] if doc.metadata else None)
        return {"message": "Document added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-docs")
async def upload_documents(file: UploadFile = File(...)):
    """Upload multiple documents (JSON format)"""
    try:
        contents = await file.read()
        docs = json.loads(contents.decode('utf-8'))
        
        texts = [doc["content"] for doc in docs]
        metadatas = [doc.get("metadata", {}) for doc in docs]
        
        agent.add_documents(texts, metadatas)
        
        return {"message": f"Added {len(docs)} documents successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_stats():
    """Get knowledge base statistics"""
    try:
        stats = agent.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))