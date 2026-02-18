from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home route (Login Page)
@app.route("/")
def login():
    return render_template("login.html")

# Handle Login
@app.route("/login", methods=["POST"])
def handle_login():
    email = request.form["email"]
    password = request.form["password"]

    # Temporary login for now
    if email == "admin@gmail.com" and password == "1234":
        return redirect(url_for("dashboard"))
    else:
        return "Invalid Email or Password"

# Dashboard route
@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=True)
