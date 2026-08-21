from fastapi import FastAPI

app = FastAPI(
    title="EasyFleet API",
    description="Fleet telemetry, route optimization, and predictive maintenance",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"status": "online", "message": "EasyFleet backend operational"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}