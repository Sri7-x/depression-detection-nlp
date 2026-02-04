from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model import analyze_text

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputText(BaseModel):
    description: str

@app.post("/predict")
async def predict_depression(input: InputText):
    if not input.description.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        result = analyze_text(input.description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "Depression Detection API is running"}
