from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_cors import CORS
import os
from dotenv import load_dotenv
import models

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

# PUBLIC ROUTES

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/movies", methods=["GET"])
def get_movies():
    movies = models.get_all_movies()
    return jsonify(movies)

@app.route("/api/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = models.get_movie_by_id(movie_id)
    if movie:
        return jsonify(movie)
    return jsonify({"error": "Movie not found"}), 404

# ADMIN AUTH ROUTES

@app.route("/admin")
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login_page"))
    return render_template("admin.html")

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if (username == os.getenv("ADMIN_USERNAME") and
            password == os.getenv("ADMIN_PASSWORD")):
        session["logged_in"] = True
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Wrong username or password"}), 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/debug-env")
def debug_env():
    """Temporary: check what env variables Flask sees."""
    return jsonify({
        "ADMIN_USERNAME": os.getenv("ADMIN_USERNAME"),
        "ADMIN_PASSWORD": os.getenv("ADMIN_PASSWORD"),
    })

# ADMIN CRUD ROUTES

def admin_required():
    return session.get("logged_in", False)

@app.route("/api/movies", methods=["POST"])
def add_movie():
    """Add a new movie - admin only."""
    if not admin_required():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    models.create_movie(
        title=data.get("title"),
        genre=data.get("genre"),
        year=data.get("year"),
        description=data.get("description"),
        rating=data.get("rating"),
        poster_url=data.get("poster_url")
    )
    return jsonify({"success": True, "message": "Movie added!"})

@app.route("/api/movies/<int:movie_id>", methods=["PUT"])
def edit_movie(movie_id):
    """Update an existing movie - admin only."""
    if not admin_required():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    models.update_movie(
        movie_id=movie_id,
        title=data.get("title"),
        genre=data.get("genre"),
        year=data.get("year"),
        description=data.get("description"),
        rating=data.get("rating"),
        poster_url=data.get("poster_url")
    )
    return jsonify({"success": True, "message": "Movie updated!"})

@app.route("/api/movies/<int:movie_id>", methods=["DELETE"])
def remove_movie(movie_id):
    """Delete a movie - admin only."""
    if not admin_required():
        return jsonify({"error": "Unauthorized"}), 401
    models.delete_movie(movie_id)
    return jsonify({"success": True, "message": "Movie deleted!"})

# START SERVER

if __name__ == "__main__":
    import time
    for i in range(10):
        try:
            models.setup_db()
            break
        except Exception as e:
            print(f"⏳ Waiting for database... attempt {i+1}/10 ({e})")
            time.sleep(3)
    app.run(host="0.0.0.0", port=5000, debug=True)