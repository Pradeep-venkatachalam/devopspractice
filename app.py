from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
accounts = {}
history = {}
acc_counter = 1000


# Create Account
@app.route("/create", methods=["POST"])
def create_account():
    global acc_counter

    data = request.json
    user_id = data.get("userId")
    name = data.get("userName")
    phone = data.get("phone")
    aadhar = data.get("aadhar")

    if not str(phone).isdigit() or len(str(phone)) != 10:
        return jsonify({"error": "Invalid phone number"}), 400

    if not str(aadhar).isdigit() or len(str(aadhar)) != 12:
        return jsonify({"error": "Invalid aadhar"}), 400

    acc_no = acc_counter
    acc_counter += 1

    accounts[acc_no] = {
        "userId": user_id,
        "name": name,
        "phone": phone,
        "aadhar": aadhar,
        "balance": 0
    }

    history[acc_no] = []

    return jsonify({"message": "Account created", "accountNumber": acc_no})


# Deposit
@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.json
    acc = data.get("accountNumber")
    amt = data.get("amount")

    if acc not in accounts:
        return jsonify({"error": "Account not found"}), 404

    accounts[acc]["balance"] += amt
    history[acc].append(f"Deposited {amt}")

    return jsonify({"balance": accounts[acc]["balance"]})


# Withdraw
@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.json
    acc = data.get("accountNumber")
    amt = data.get("amount")

    if acc not in accounts:
        return jsonify({"error": "Account not found"}), 404

    if amt <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    if accounts[acc]["balance"] < amt:
        return jsonify({"error": "Insufficient balance"}), 400

    accounts[acc]["balance"] -= amt
    history[acc].append(f"Withdraw {amt}")

    return jsonify({"balance": accounts[acc]["balance"]})


# Transfer
@app.route("/transfer", methods=["POST"])
def transfer():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")
    amt = data.get("amount")

    if sender == receiver:
        return jsonify({"error": "Same account"}), 400

    if sender not in accounts or receiver not in accounts:
        return jsonify({"error": "Account not found"}), 404

    if accounts[sender]["balance"] < amt:
        return jsonify({"error": "Insufficient balance"}), 400

    accounts[sender]["balance"] -= amt
    accounts[receiver]["balance"] += amt

    history[sender].append(f"Sent {amt} to {receiver}")
    history[receiver].append(f"Received {amt} from {sender}")

    return jsonify({"message": "Transaction successful"})


# Show Account
@app.route("/account/<int:acc>")
def show_account(acc):
    if acc not in accounts:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(accounts[acc])


# Show History
@app.route("/history/<int:acc>")
def show_history(acc):
    if acc not in history:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(history[acc])


# Home
@app.route("/")
def home():
    return "DevOps Banking Web App Running 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
