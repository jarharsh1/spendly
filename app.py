import os
import re
from datetime import datetime

from flask import Flask, redirect, render_template, request, session, url_for

from database.db import (
    create_user,
    get_db,
    get_user_by_email,
    get_user_by_id,
    init_db,
    seed_db,
    verify_user,
)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-secret-key-do-not-use-in-production")

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    error = None
    if not name or not email or not password:
        error = "All fields are required."
    elif not EMAIL_RE.match(email):
        error = "Enter a valid email address."
    elif len(password) < 8:
        error = "Password must be at least 8 characters."
    elif get_user_by_email(email):
        error = "An account with this email already exists."

    if error:
        return render_template("register.html", error=error, name=name, email=email), 400

    create_user(name, email, password)
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    user = verify_user(email, password) if email and password else None

    if user is None:
        error = "Invalid email or password."
        return render_template("login.html", error=error, email=email), 400

    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    db_user = get_user_by_id(session["user_id"])
    if db_user is None:
        session.pop("user_id", None)
        return redirect(url_for("login"))

    member_since = datetime.strptime(db_user["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %Y")
    user = {
        "name": db_user["name"],
        "email": db_user["email"],
        "member_since": member_since,
    }
    stats = {
        "total_spent": "₹6,220",
        "transaction_count": 8,
        "top_category": "Shopping",
    }
    transactions = [
        {"date": "2026-01-18", "description": "Miscellaneous", "category": "Other", "amount": "₹300"},
        {"date": "2026-01-15", "description": "Dinner with friends", "category": "Food", "amount": "₹450"},
        {"date": "2026-01-12", "description": "Movie tickets", "category": "Entertainment", "amount": "₹600"},
        {"date": "2026-01-10", "description": "Pharmacy", "category": "Health", "amount": "₹800"},
        {"date": "2026-01-08", "description": "New shoes", "category": "Shopping", "amount": "₹2,200"},
    ]
    categories = [
        {"name": "Shopping", "amount": "₹2,200", "percent": 78},
        {"name": "Bills", "amount": "₹1,500", "percent": 58},
        {"name": "Health", "amount": "₹800", "percent": 42},
        {"name": "Entertainment", "amount": "₹600", "percent": 32},
    ]

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
