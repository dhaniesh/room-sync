from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/health")
def health() -> dict:
    return JSONResponse({"status": "Healthy", "statusCode": "200"}, status.HTTP_200_OK)

