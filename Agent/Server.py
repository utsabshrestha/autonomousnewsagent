from re import match
from unittest import case, result
from pkg_resources import yield_lines
import uvicorn
import json
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from Agent.GeminiApi import GeminiApi
from Graph import graph as agent_app
from AgentEvents import news_event_stream_generator as agent

app = FastAPI()
gemini = GeminiApi().GetInstance()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/stream")
async def run_agent(topic: str):
    print(f"Received request for topic : {topic}")
    return StreamingResponse(agent(topic), media_type="text/event-stream")


@app.get("/health")
async def health_check():
    health_status = {
        "Agentstatus": "healthy",
        "service": "autonomous-news-agent",
        "gemini_api": "unknown"
    }
    
    try:
        # Simple test call to verify Gemini is responsive
        response = gemini.invoke("Hello")
        if response and response.content:
            health_status["gemini_api"] = "healthy"
        else:
            health_status["gemini_api"] = "unhealthy"
            health_status["Agentstatus"] = "degraded"
    except Exception as e:
        health_status["gemini_api"] = f"error: {str(e)}"
        health_status["Agentstatus"] = "degraded"
    
    return health_status

if __name__ == "__main__":
    #run on localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)

