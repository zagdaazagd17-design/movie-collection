import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

# CONNECTION
def get_connection():
    """Create and return a database connection using .env settings."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

# SETUP
def setup_db():
    """Create the movies table if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            title       VARCHAR(255) NOT NULL,
            genre       VARCHAR(100),
            year        INT,
            description TEXT,
            rating      FLOAT,
            poster_url  VARCHAR(500)
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database ready!")

# CREATE 
def create_movie(title, genre, year, description, rating, poster_url):
    """Insert a new movie into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO movies (title, genre, year, description, rating, poster_url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (title, genre, year, description, rating, poster_url))
    conn.commit()
    conn.close()

# READ 
def get_all_movies():
    """Return all movies from the database as a list of dicts."""
    conn = get_connection()
    # dictionary=True means each row comes back as {id: 1, title: "...", ...}
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies ORDER BY id DESC")
    movies = cursor.fetchall()
    conn.close()
    return movies

# READ
def get_movie_by_id(movie_id):
    """Return a single movie by its ID."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    conn.close()
    return movie

# UPDATE 
def update_movie(movie_id, title, genre, year, description, rating, poster_url):
    """Update a movie's details by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE movies
        SET title=%s, genre=%s, year=%s,
            description=%s, rating=%s, poster_url=%s
        WHERE id=%s
    """, (title, genre, year, description, rating, poster_url, movie_id))
    conn.commit()
    conn.close()

# DELETE
def delete_movie(movie_id):
    """Delete a movie from the database by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
    conn.commit()
    conn.close()