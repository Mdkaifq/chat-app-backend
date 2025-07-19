import uvicorn
import os

port = int(os.getenv("port", 33254))
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True, server_header=False)
