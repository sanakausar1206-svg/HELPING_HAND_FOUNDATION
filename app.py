from flask import Flask, request, send_from_directory, render_template_string
import sqlite3
import os

app = Flask(__name__, static_folder="public")
app.secret_key = "helping-hands-student-project"
DATABASE = os.path.join(os.path.dirname(__file__), "helping_hands.db")


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_db()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            interest TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()


@app.route("/")
def home():
    return send_from_directory("public", "index.html")


@app.route("/<path:page>")
def pages(page):
    # Serve only files inside the public folder.
    return send_from_directory("public", page)


@app.route("/volunteer", methods=["POST"])
def volunteer():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    interest = request.form.get("interest", "").strip()

    if not name or not email or not interest:
        return "Please complete all volunteer fields.", 400

    connection = get_db()
    connection.execute(
        "INSERT INTO volunteers (name, email, interest) VALUES (?, ?, ?)",
        (name, email, interest)
    )
    connection.commit()
    connection.close()
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Volunteer Registration Successful</title>
        <style>
            * { box-sizing: border-box; }
            body {
                margin: 0; min-height: 100vh; display: flex;
                justify-content: center; align-items: center; padding: 20px;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #e8f7f0, #f4f7fb, #fff3e8);
                color: #183b32;
            }
            .success-card {
                width: 100%; max-width: 550px; padding: 40px 25px;
                text-align: center; background: white; border-radius: 22px;
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.10);
            }
            .check {
                width: 75px; height: 75px; margin: 0 auto 20px;
                display: flex; justify-content: center; align-items: center;
                background: #dff7e9; color: #16845e; border-radius: 50%;
                font-size: 40px; font-weight: bold;
            }
            .brand {
                color: #16845e; font-size: 13px; font-weight: bold;
                letter-spacing: 2px; text-transform: uppercase;
            }
            h1 { margin: 18px 0; font-size: 30px; }
            p { color: #64756f; line-height: 1.7; margin-bottom: 28px; }
            .buttons {
                display: flex; justify-content: center;
                flex-wrap: wrap; gap: 12px;
            }
            a {
                padding: 13px 18px; border-radius: 10px;
                text-decoration: none; font-weight: bold;
            }
            .primary { background: #176b57; color: white; }
            .secondary { background: #eaf6f1; color: #176b57; }
            a:hover { opacity: 0.85; }
            .footer { margin-top: 28px; font-size: 12px; color: #91a19b; }
            @media (max-width: 450px) {
                .success-card { padding: 30px 18px; }
                .buttons a { width: 100%; }
            }
        </style>
    </head>
    <body>
        <div class="success-card">
            <div class="check">&#10003;</div>
            <div class="brand">Helping Hands Foundation</div>
            <h1>You're on the team!</h1>
            <p>
                Your volunteer registration has been saved successfully.
                Thank you for giving your time to make a difference.
            </p>
            <div class="buttons">
                <a class="primary" href="/volunteer.html">Back to Volunteer Page</a>
                <a class="secondary" href="/">Back to Home</a>
            </div>
            <div class="footer">Together, small acts make a big difference.</div>
        </div>
    </body>
    </html>
    """

@app.route("/donate", methods=["POST"])
def donate():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    amount = request.form.get("amount", "").strip()

    if not name or not email or not amount:
        return "Please complete all donation fields.", 400

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        return "Please enter a valid donation amount.", 400

    connection = get_db()
    connection.execute(
        "INSERT INTO donations (name, email, amount) VALUES (?, ?, ?)",
        (name, email, amount)
    )
    connection.commit()
    connection.close()
    return """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Donation pledge saved! | Helping Hands Foundation</title>
      <style>
        * { box-sizing: border-box; }
        body {
          margin: 0; min-height: 100vh; display: grid; place-items: center;
          padding: 24px; font-family: Arial, Helvetica, sans-serif;
          background: linear-gradient(135deg, #e8f7f0 0%, #f4f7fb 55%, #fff3e8 100%);
          color: #183b32;
        }
        .success-card {
          width: 100%; max-width: 560px; text-align: center; background: #fff;
          padding: 42px 32px; border-radius: 24px;
          box-shadow: 0 18px 55px rgba(20, 83, 65, .13);
          border: 1px solid rgba(23, 107, 87, .10);
        }
        .check {
          width: 76px; height: 76px; margin: 0 auto 20px; display: grid;
          place-items: center; border-radius: 50%; background: #dff7e9;
          color: #16845e; font-size: 38px; font-weight: 700;
        }
        .eyebrow { color: #16845e; text-transform: uppercase; letter-spacing: 2px;
          font-size: 12px; font-weight: 700; margin-bottom: 10px; }
        h1 { font-size: clamp(26px, 5vw, 34px); line-height: 1.2; margin: 0 0 14px; }
        p { color: #64756f; font-size: 16px; line-height: 1.7; margin: 0 0 26px; }
        .actions { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }
        a { display: inline-block; text-decoration: none; font-weight: 700; padding: 13px 19px;
          border-radius: 12px; transition: transform .15s ease, background .15s ease; }
        a:hover { transform: translateY(-2px); }
        .primary { background: #176b57; color: #fff; }
        .primary:hover { background: #105744; }
        .secondary { color: #176b57; background: #eaf6f1; }
        .footer { margin-top: 28px; font-size: 12px; color: #91a19b; }
        @media (max-width: 420px) {
          .success-card { padding: 32px 20px; }
          .actions a { width: 100%; }
        }
      </style>
    </head>
    <body>
      <main class="success-card">
        <div class="check">&#10003;</div>
        <div class="eyebrow">Helping Hands Foundation</div>
        <h1>Donation pledge saved!</h1>
        <p>Thank you for supporting our cause. Your pledge has been recorded. This is a student project, so no real payment was collected.</p>
        <div class="actions">
          <a class="primary" href="/donation.html">Back to Donation Page</a>
          <a class="secondary" href="/">Back to Home</a>
        </div>
        <div class="footer">Together, small acts make a big difference.</div>
      </main>
    </body>
    </html>
    """


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        return "Please complete all contact fields.", 400

    connection = get_db()
    connection.execute(
        "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )
    connection.commit()
    connection.close()
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Message Sent Successfully</title>
        <style>
            * { box-sizing: border-box; }
            body {
                margin: 0; min-height: 100vh; display: flex;
                justify-content: center; align-items: center; padding: 20px;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #e8f7f0, #f4f7fb, #fff3e8);
                color: #183b32;
            }
            .success-card {
                width: 100%; max-width: 550px; padding: 40px 25px;
                text-align: center; background: #fff; border-radius: 22px;
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.10);
            }
            .check {
                width: 75px; height: 75px; margin: 0 auto 20px;
                display: flex; justify-content: center; align-items: center;
                background: #dff7e9; color: #16845e; border-radius: 50%;
                font-size: 40px; font-weight: bold;
            }
            .brand {
                color: #16845e; font-size: 13px; font-weight: bold;
                letter-spacing: 2px; text-transform: uppercase;
            }
            h1 { margin: 18px 0; font-size: 30px; }
            p { color: #64756f; line-height: 1.7; margin-bottom: 28px; }
            .buttons {
                display: flex; justify-content: center;
                flex-wrap: wrap; gap: 12px;
            }
            a {
                padding: 13px 18px; border-radius: 10px;
                text-decoration: none; font-weight: bold;
            }
            .primary { background: #176b57; color: white; }
            .secondary { background: #eaf6f1; color: #176b57; }
            a:hover { opacity: 0.85; }
            .footer { margin-top: 28px; font-size: 12px; color: #91a19b; }
            @media (max-width: 450px) {
                .success-card { padding: 30px 18px; }
                .buttons a { width: 100%; }
            }
        </style>
    </head>
    <body>
        <main class="success-card">
            <div class="check">&#10003;</div>
            <div class="brand">Helping Hands Foundation</div>
            <h1>Message sent successfully!</h1>
            <p>
                Thank you for reaching out. Your message has been saved.
                We appreciate you getting in touch with Helping Hands.
            </p>
            <div class="buttons">
                <a class="primary" href="/contact.html">Back to Contact Page</a>
                <a class="secondary" href="/">Back to Home</a>
            </div>
            <div class="footer">Together, small acts make a big difference.</div>
        </main>
    </body>
    </html>
    """

@app.route("/records")
def records():
    """Simple read-only page to view form submissions for the student project."""
    connection = get_db()
    volunteers = connection.execute(
        "SELECT * FROM volunteers ORDER BY id DESC"
    ).fetchall()
    donations = connection.execute(
        "SELECT * FROM donations ORDER BY id DESC"
    ).fetchall()
    messages = connection.execute(
        "SELECT * FROM messages ORDER BY id DESC"
    ).fetchall()
    connection.close()

    page = """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Saved Form Records | Helping Hands</title>
      <style>
        body { margin:0; padding:24px; font-family:Arial,sans-serif; background:#f4f7fb; color:#1e293b; }
        .wrap { max-width:1100px; margin:auto; }
        h1 { color:#176b57; margin-bottom:6px; }
        .note { color:#64748b; margin-top:0; }
        .section { background:white; padding:18px; margin:22px 0; border-radius:14px; box-shadow:0 4px 18px #0f172a0d; overflow-x:auto; }
        h2 { margin-top:0; color:#176b57; }
        table { width:100%; border-collapse:collapse; min-width:560px; }
        th, td { padding:11px 12px; border-bottom:1px solid #e2e8f0; text-align:left; vertical-align:top; }
        th { background:#e8f5f0; }
        .empty { color:#64748b; padding:10px 0; }
        a { color:#176b57; font-weight:bold; }
        .top { display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px; }
        .count { display:inline-block; background:#e8f5f0; color:#176b57; padding:5px 10px; border-radius:20px; font-size:14px; }
      </style>
    </head>
    <body>
      <main class="wrap">
        <div class="top">
          <div><h1>Saved Form Records</h1>
          <p class="note">Read-only view of information submitted through the website forms.</p></div>
          <a href="/">← Back to website</a>
        </div>

        <section class="section">
          <h2>Volunteer Registrations <span class="count">{{ volunteers|length }} records</span></h2>
          {% if volunteers %}
          <table><thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Interest</th><th>Date</th></tr></thead><tbody>
          {% for item in volunteers %}
          <tr><td>{{ item.id }}</td><td>{{ item.name }}</td><td>{{ item.email }}</td><td>{{ item.interest }}</td><td>{{ item.created_at }}</td></tr>
          {% endfor %}
          </tbody></table>
          {% else %}<p class="empty">No volunteer registrations saved yet.</p>{% endif %}
        </section>

        <section class="section">
          <h2>Donation Pledges <span class="count">{{ donations|length }} records</span></h2>
          {% if donations %}
          <table><thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Amount</th><th>Date</th></tr></thead><tbody>
          {% for item in donations %}
          <tr><td>{{ item.id }}</td><td>{{ item.name }}</td><td>{{ item.email }}</td><td>₹{{ "%.2f"|format(item.amount) }}</td><td>{{ item.created_at }}</td></tr>
          {% endfor %}
          </tbody></table>
          {% else %}<p class="empty">No donation pledges saved yet.</p>{% endif %}
        </section>

        <section class="section">
          <h2>Contact Messages <span class="count">{{ messages|length }} records</span></h2>
          {% if messages %}
          <table><thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Message</th><th>Date</th></tr></thead><tbody>
          {% for item in messages %}
          <tr><td>{{ item.id }}</td><td>{{ item.name }}</td><td>{{ item.email }}</td><td>{{ item.message }}</td><td>{{ item.created_at }}</td></tr>
          {% endfor %}
          </tbody></table>
          {% else %}<p class="empty">No contact messages saved yet.</p>{% endif %}
        </section>
        <p class="note">Student-project note: this page has no login. Use it only on your own computer for demonstration.</p>
      </main>
    </body>
    </html>
    """
    return render_template_string(
        page, volunteers=volunteers, donations=donations, messages=messages
    )


create_tables()

if __name__ == "__main__":
    print("Helping Hands Foundation is starting...")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(debug=True)