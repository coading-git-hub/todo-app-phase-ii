import uvicorn
import os

if __name__ == "__main__":
    # Set the port to 8000
    os.environ.setdefault("PORT", "8000")
    print("Starting server on port 8000...")
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=False)