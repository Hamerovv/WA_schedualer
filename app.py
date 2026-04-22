from flask import Flask, jsonify, request
from scheduler import run_scheduler, load_jobs
import threading

app = Flask(__name__)

ENGINE_STATE = {"running": False}


# ===================== START ENGINE =====================
def start_engine():
    if not ENGINE_STATE["running"]:
        ENGINE_STATE["running"] = True
        threading.Thread(target=run_scheduler, daemon=True).start()


# ===================== API =====================

@app.route("/start")
def start():
    start_engine()
    return jsonify({"status": "started"})


@app.route("/status")
def status():
    jobs, _ = load_jobs()
    return jsonify({
        "running": ENGINE_STATE["running"],
        "jobs_pending": len(jobs)
    })


@app.route("/run-now", methods=["POST"])
def run_now():
    start_engine()
    return jsonify({"status": "triggered"})


# ===================== DASHBOARD =====================

@app.route("/")
def home():
    return """
    <h2>📬 WhatsApp Scheduler Dashboard</h2>
    <button onclick="fetch('/start')">Start Engine</button>
    <button onclick="fetch('/run-now', {method:'POST'})">Run Now</button>
    <p>Check /status for live state</p>
    """


if __name__ == "__main__":
    app.run(port=5055)