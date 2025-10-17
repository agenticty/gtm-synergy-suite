from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import pandas as pd
import io
from agents.dealsense import DealSenseAgent, DealScore

router = APIRouter(prefix="/dealsense", tags=["DealSense"])

agent = DealSenseAgent()

@router.post("/analyze-csv", response_model=List[DealScore])
async def analyze_deals_csv(file: UploadFile = File(...)):
    """Upload CSV of deals and get AI scoring"""
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV")
    
    try:
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Validate required columns
        required_cols = ['company_name', 'deal_value', 'stage', 'days_in_pipeline']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {missing}"
            )
        
        # Analyze pipeline
        results = agent.analyze_pipeline(df)
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-deal", response_model=DealScore)
async def analyze_single_deal(deal: dict):
    """Analyze a single deal"""
    try:
        result = agent.analyze_deal(deal)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))