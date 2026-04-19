from flask import Flask, render_template, request

app = Flask(__name__)

accounts = {}
acc_no = 1000


@app.route("/")
def home():
    return render_template("index.html")


# CREATE ACCOUNT
@app.route("/create", methods=["POST"])
def create():
    global acc_no
    name = request.form["name"]

    accounts[acc_no] = {
        "name": name,
        "balance": 0,
        "transactions": ["Account created"]
    }

    acc_no += 1
    return f"Account created successfully! Account No: {acc_no - 1}"


# DEPOSIT
@app.route("/deposit", methods=["POST"])
def deposit():
    acc = int(request.form["acc"])
    amt = int(request.form["amount"])

    if acc in accounts:
        accounts[acc]["balance"] += amt
        accounts[acc]["transactions"].append(f"Deposited ₹{amt}")
        return f"Balance: ₹{accounts[acc]['balance']}"
    return "Account not found"


# WITHDRAW
@app.route("/withdraw", methods=["POST"])
def withdraw():
    acc = int(request.form["acc"])
    amt = int(request.form["amount"])

    if acc in accounts:
        if accounts[acc]["balance"] >= amt:
            accounts[acc]["balance"] -= amt
            accounts[acc]["transactions"].append(f"Withdrew ₹{amt}")
            return f"Balance: ₹{accounts[acc]['balance']}"
        return "Insufficient balance"
    return "Account not found"


# TRANSFER
@app.route("/transfer", methods=["POST"])
def transfer():
    from_acc = int(request.form["from_acc"])
    to_acc = int(request.form["to_acc"])
    amt = int(request.form["amount"])

    if from_acc not in accounts:
        return "From account not found"
    if to_acc not in accounts:
        return "To account not found"

    if accounts[from_acc]["balance"] < amt:
        return "Insufficient balance"

    accounts[from_acc]["balance"] -= amt
    accounts[to_acc]["balance"] += amt

    accounts[from_acc]["transactions"].append(
        f"Transferred ₹{amt} to {to_acc}"
    )
    accounts[to_acc]["transactions"].append(
        f"Received ₹{amt} from {from_acc}"
    )

    return "Transfer successful"


# HISTORY
@app.route("/history", methods=["POST"])
def history():
    acc = int(request.form["acc"])

    if acc in accounts:
        return "<br>".join(accounts[acc]["transactions"])

    return "Account not found"


# DELETE
@app.route("/delete", methods=["POST"])
def delete():
    acc = int(request.form["acc"])

    if acc in accounts:
        del accounts[acc]
        return "Account deleted successfully"

    return "Account not found"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
