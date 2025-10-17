from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from agents.outreachai import OutreachAIAgent, OutreachRequest, OutreachResult

router = APIRouter(prefix="/outreachai", tags=["OutreachAI"])

agent = OutreachAIAgent()

class GenerateOutreachRequest(BaseModel):
    company_name: str
    industry: str
    company_size: str
    pain_points: List[str]
    decision_maker_name: Optional[str] = None
    decision_maker_title: Optional[str] = None
    recent_activity: Optional[str] = None
    channel: str = "email"

class MultiVersionRequest(GenerateOutreachRequest):
    versions_count: int = 3

@router.post("/generate", response_model=OutreachResult)
async def generate_outreach(request: GenerateOutreachRequest):
    """Generate personalized outreach message"""
    try:
        outreach_request = OutreachRequest(**request.dict())
        result = agent.generate_outreach(outreach_request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-multiple", response_model=List[OutreachResult])
async def generate_multiple_versions(request: MultiVersionRequest):
    """Generate multiple versions for A/B testing"""
    try:
        outreach_request = OutreachRequest(**request.dict(exclude={'versions_count'}))
        results = agent.generate_multiple_versions(outreach_request, request.versions_count)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/generate-debug")
async def generate_outreach_debug(request: GenerateOutreachRequest):
    """Debug version that shows raw output"""
    try:
        outreach_request = OutreachRequest(**request.dict())
        result = agent.generate_outreach(outreach_request)
        
        # Return both raw result and parsed result
        return {
            "parsed": result.dict(),
            "raw_type": str(type(result))
        }
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@router.get("/channels")
async def get_supported_channels():
    """Get list of supported outreach channels"""
    return {
        "channels": [
            {"id": "email", "name": "Email", "description": "Traditional email outreach"},
            {"id": "linkedin", "name": "LinkedIn", "description": "LinkedIn connection message"},
            {"id": "slack", "name": "Slack", "description": "Slack direct message"}
        ]
    }