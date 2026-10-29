import os
import socket
import time
from datetime import datetime, timezone, timedelta

from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = "1"
START_TIME = time.time()
HOSTNAME = socket.gethostname()
IST = timezone(timedelta(hours=5, minutes=30))
request_count = 0

PAGE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Live ECS App</title>
  <style>
    body { font-family: Arial, sans-serif; background: #0f172a; color: #e2e8f0;
           display: flex; justify-content: center; padding: 24px; margin: 0; }
    .card { background: #1e293b; border-radius: 12px; padding: 24px;
            max-width: 420px; width: 100%; }
    h1 { font-size: 22px; margin-top: 0; }
    .clock { font-size: 36px; font-weight: bold; color: #38bdf8; margin: 12px 0; }
    .row { display: flex; justify-content: space-between; padding: 8px 0;
           border-top: 1px solid #334155; font-size: 15px; }
    .label { color: #94a3b8; }
    .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%;
           background: #22c55e; margin-right: 6px; }
  </style>
</head>
<body>
  <div class="card">
    <h1><span class="dot" id="dot"></span>Hello from ECS Fargate! 🐳</h1>
    <div class="clock" id="clock">--:--:--</div>
    <div class="row"><span class="label">Version</span><span id="version">-</span></div>
    <div class="row"><span class="label">Container ID</span><span id="host">-</span></div>
    <div class="row"><span class="label">Server time (IST)</span><span id="ist">-</span></div>
    <div class="row"><span class="label">Uptime</span><span id="uptime">-</span></div>
    <div class="row"><span class="label">Requests served</span><span id="count">-</span></div>
  </div>
  <script>
    function tick() {
      document.getElementById("clock").textContent =
        new Date().toLocaleTimeString();
    }
    async function refresh() {
      try {
        const r = await fetch("/api/status", { cache: "no-store" });
        const d = await r.json();
        document.getElementById("version").textContent = d.version;
        document.getElementById("host").textContent = d.hostname;
        document.getElementById("ist").textContent = d.server_time_ist;
        document.getElementById("uptime").textContent = d.uptime;
        document.getElementById("count").textContent = d.requests;
        document.getElementById("dot").style.background = "#22c55e";
      } catch (e) {
        document.getElementById("dot").style.background = "#ef4444";
      }
    }
    setInterval(tick, 1000);
    setInterval(refresh, 2000);
    tick();
    refresh();
  </script>
</body>
</html>
"""


def format_uptime(seconds):
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}h {m}m {s}s"


@app.route("/")
def home():
    return PAGE


@app.route("/api/status")
def status():
    global request_count
    request_count += 1
    now = datetime.now(IST)
    return jsonify(
        version=APP_VERSION,
        hostname=HOSTNAME,
        server_time_ist=now.strftime("%d %b %Y, %H:%M:%S"),
        uptime=format_uptime(time.time() - START_TIME),
        requests=request_count,
    )


@app.route("/health")
def health():
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 80)))