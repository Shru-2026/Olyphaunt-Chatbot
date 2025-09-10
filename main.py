# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Import your existing chatbot initializer
from chatbot_backend import initialize_chatbot

# Path to your PDF (adjust if needed)
PDF_PATH = "Olyphaunt FAQs.pdf"

# Initialize chatbot once at startup (may take time depending on your backend)
chatbot = initialize_chatbot(PDF_PATH)

app = FastAPI(title="Olyphaunt Chat API and Frontend")

# Serve static files from ./static (CSS, images, JS if any)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML templates directory
static = Jinja2Templates(directory="static")


class Message(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the chat HTML page."""
    return static.TemplateResponse("chat.html", {"request": request})


@app.post("/chat")
async def chat_endpoint(payload: Message):
    """Receive message JSON { message: "..." } and return { reply: "..." }."""
    try:
        # Call your chatbot's synchronous respond method
        reply = chatbot.respond(payload.message)
    except Exception as e:
        # Return a friendly error message instead of crashing
        reply = f"Error generating reply: {e}"
    return JSONResponse({"reply": reply})
