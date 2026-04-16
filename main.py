# SPDX-License-Identifier: AGPL-3.0-only
import os
from fastapi import FastAPI

app = FastAPI(title="ploydok fixture-fastapi")

BUILD_ID = os.environ.get("PLOYDOK_BUILD_ID", "unknown")

@app.get("/")
def root():
    return {"message": "hello from ploydok (fastapi)", "build": BUILD_ID}

@app.get("/health")
def health():
    return {"status": "ok"}
