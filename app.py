from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask App is Running!"

@app.route('/api')
def api():
    return jsonify({
        "message": "Welcome to Flask API"
    })

if __name__ == '__main__':
    app.run(debug=True)
