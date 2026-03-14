import uvicorn
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from main import app

if __name__ == "__main__":
    print("Starting uvicorn server on port 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
