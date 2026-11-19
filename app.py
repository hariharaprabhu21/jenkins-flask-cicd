from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Hari Hara Prabhu's CI/CD"

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)