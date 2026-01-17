



from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "ashishghosalkar"

# ---------------- LOGIN MANAGER ----------------
login_manager = LoginManager(app)
login_manager.login_view = "login"

# ---------------- IN-MEMORY USERS ----------------
users = {}  # store users like: users["email"] = "password"

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        
@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None

# ---------------- ROUTES ---------------s
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            flash("Password do not match")
            return redirect(url_for("signup"))

        if email in users:
            flash("Email already exists")
            return redirect(url_for("signup"))

        users[email] = password
        flash("Signup successful!")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in users and users[email] == password:
            login_user(User(email))
            return redirect(url_for("account"))
        flash("Invalid email or password")

    return render_template("login.html")

@app.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user.id)

@app.route("/cart")
@login_required
def cart():
    return "<h1>Your Cart (Protected)</h1><a href='/account'>Back to Account</a>"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)
