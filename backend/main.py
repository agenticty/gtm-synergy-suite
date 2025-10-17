from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import dealsense
from routers import askgtm
from routers import outreachai
import uvicorn
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="GTM Synergy Suite API",
    description="AI-powered tools for GTM teams",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://gtm-synergy-suite.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dealsense.router)
app.include_router(askgtm.router)
app.include_router(outreachai.router)

@app.get("/")
def root():
    return {
        "message": "GTM Synergy Suite API",
        "status": "operational",
        "tools": ["DealSense AI", "AskGTM AI", "OutreachAI"]
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)