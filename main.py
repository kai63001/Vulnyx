from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path
from numba import jit

app = FastAPI()
templates = Jinja2Templates(directory="templates")

RESULT_PATH = Path("results/results.json")
RESULT_PATH.parent.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory="public"), name="static")


@jit(nopython=True)
def calculate_score(x):
    # ตัวอย่าง JIT function ที่คำนวณหนัก ๆ
    result = 0
    for i in range(x):
        result += i * i
    return result

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    if RESULT_PATH.exists():
        data = json.loads(RESULT_PATH.read_text())
    else:
        data = []
    return templates.TemplateResponse("dashboard.html", {"request": request, "results": data})

@app.post("/scan")
async def scan(request: Request, domain: str = Form(...)):
    # ตัวอย่าง fake scan
    score = calculate_score(1000)
    result = {"domain": domain, "status": "done", "score": score}
    
    # บันทึกลง JSON
    results = []
    if RESULT_PATH.exists():
        results = json.loads(RESULT_PATH.read_text())
    print(results)
    results.append(result)
    RESULT_PATH.write_text(json.dumps(results, indent=2))

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "results": results,
        "message": f"Scan complete for {domain}"
    })


if __name__ == "__main__":
    import uvicorn
    print("🚀 Vulnyx Server starting at http://localhost:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000)