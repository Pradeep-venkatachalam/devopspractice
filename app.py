from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from DevOps Banking Project "

@app.route("/health")
def health():
    return "OK - Service is Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
