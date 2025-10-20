from fastapi      import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from urllib.parse import urlparse, ParseResult
from pydantic     import BaseModel
from core         import Grok
from wrapper      import ChatGPT
from uvicorn      import run
import json


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def read_root():
    return FileResponse("index.html")

class ConversationRequest(BaseModel):
    proxy: str = None
    message: str
    model: str = "grok-3-auto"
    extra_data: dict = None
    ai_type: str = "grok"  # Can be "grok" or "chatgpt"
    image: str = None  # Base64 encoded image for ChatGPT
    stream: bool = False  # Enable streaming response

def format_proxy(proxy: str) -> str:
    
    if not proxy.startswith(("http://", "https://")):
        proxy: str = "http://" + proxy
    
    try:
        parsed: ParseResult = urlparse(proxy)

        if parsed.scheme not in ("http", ""):
            raise ValueError("Not http scheme")

        if not parsed.hostname or not parsed.port:
            raise ValueError("No url and port")

        if parsed.username and parsed.password:
            return f"http://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port}"
        
        else:
            return f"http://{parsed.hostname}:{parsed.port}"
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid proxy format: {str(e)}")

@app.post("/ask")
async def create_conversation(request: ConversationRequest):
    if not request.proxy or not request.message:
        raise HTTPException(status_code=400, detail="Proxy and message are required")

    proxy = format_proxy(request.proxy)

    try:
        if request.stream:
            # Streaming response
            async def generate():
                if request.ai_type.lower() == "chatgpt":
                    # For ChatGPT, streaming not yet implemented in wrapper, so simulate with full response split into tokens
                    # TODO: Modify ChatGPT wrapper to support streaming
                    if request.image:
                        full_response: str = ChatGPT(proxy).ask_question(request.message, image=request.image)
                    elif request.extra_data:
                        full_response: str = ChatGPT(proxy).ask_question(request.message, extra_data=request.extra_data)
                    else:
                        full_response: str = ChatGPT(proxy).ask_question(request.message)
                    # Split into tokens (simple word-based for now)
                    tokens = full_response.split()
                    for token in tokens:
                        yield f"data: {json.dumps({'token': token + ' '})}\n\n"
                    # Send final metadata
                    yield f"data: {json.dumps({'done': True, 'extra_data': None})}\n\n"
                else:
                    # For Grok, use the stream_response from start_convo
                    answer: dict = Grok(request.model, proxy).start_convo(request.message, request.extra_data)
                    for token in answer.get("stream_response", []):
                        yield f"data: {json.dumps({'token': token})}\n\n"
                    # Send final metadata
                    yield f"data: {json.dumps({'done': True, 'extra_data': answer.get('extra_data')})}\n\n"
            return StreamingResponse(generate(), media_type="text/event-stream")
        else:
            # Non-streaming response (existing logic)
            if request.ai_type.lower() == "chatgpt":
                # Use ChatGPT wrapper
                if request.image:
                    answer: str = ChatGPT(proxy).ask_question(request.message, image=request.image)
                elif request.extra_data:
                    answer: str = ChatGPT(proxy).ask_question(request.message, extra_data=request.extra_data)
                else:
                    answer: str = ChatGPT(proxy).ask_question(request.message)

                return {
                    "status": "success",
                    "stream_response": [answer],
                    "extra_data": None  # ChatGPT doesn't use extra_data for continuation
                }
            else:
                # Default to Grok
                answer: dict = Grok(request.model, proxy).start_convo(request.message, request.extra_data)

                return {
                    "status": "success",
                    **answer
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    run("api_server:app", host="0.0.0.0", port=6969)
