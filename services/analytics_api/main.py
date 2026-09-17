from pathlib import Path
import json

from fastapi import FastAPI, HTTPException

app = FastAPI(title="PulseStream Analytics API", version="0.1.0")
REPORT_PATH = Path("data/reports/summary.json")


@app.get("/health")
def health():
    return {"status": "ok", "service": "analytics-api"}


@app.get("/analytics/summary")
def summary():
    if not REPORT_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="No analytics report found. Run scripts/run_spark_job.py first.",
        )
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))
