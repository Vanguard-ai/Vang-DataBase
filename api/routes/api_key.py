from fastapi import HTTPException, Header

API_KEY = "Vanguard2024"

def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")