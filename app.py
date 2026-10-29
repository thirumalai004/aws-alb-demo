from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from my custom domain! 🌐</h1><p>Version: 2</p>"

@app.route("/health")
def health():
    return "ok", 200