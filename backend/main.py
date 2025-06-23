import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "3978"))

if __name__ == "__main__":
    uvicorn.run("app:app", host=HOST, port=PORT)
