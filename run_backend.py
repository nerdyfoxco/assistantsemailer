import uvicorn
import sys
import os

# Add current dir to path explicitly to ensure spine package is found
sys.path.append(os.getcwd())

if __name__ == "__main__":
    print(f"Starting backend with sys.path: {sys.path}")
    uvicorn.run("spine.main:app", host="0.0.0.0", port=8000, reload=False)
