import requests
import sqlite3
import tkinter as tk
from tkinter.ttk import Combobox
from textblob import TextBlob
from PIL import Image, ImageTk
import io

# TMDB API details
API_KEY = '966abb94029dbf93fe955ddea2e568f4'  
BASE_URL = 'https://api.themoviedb.org/3'
IMG_URL = 'https://image.tmdb.org/t/p/w200'
# TMDB (The Movie Database) is a popular, community-maintained database for movies, TV shows, and actors. 
# It provides a rich API that allows developers to access detailed metadata, including genres, overviews, 
# ratings, release dates, and poster images. The API supports advanced search and discovery features, 
# making it ideal for building movie recommendation systems or entertainment-related applications.

# Genre mapping based on sentiment analysis
SENTIMENT_GENRE_MAP = {
    'positive': 35,  # Comedy
    'neutral': 28,   # Action
    'negative': 18   # Drama
}

# Genre mapping based on age
AGE_GENRE_MAP = {
    'child': 16,     # Animation
    'teen': 10749,   # Romance
    'adult': 18,     # Drama
}

# SQLite setup
def setup_database():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY,
            sentiment TEXT NOT NULL,
            movie_title TEXT NOT NULL,
            overview TEXT NOT NULL,
            release_date TEXT,
            rating REAL,
            user_name TEXT,
            user_age INTEGER,
            user_gender TEXT
        )
    ''')
    conn.commit()
    return conn, c

conn, c = setup_database()

# Sentiment prediction logic
def predict_sentiment(text):
    blob = TextBlob(text)
    if blob.sentiment.polarity > 0:
        return 'positive'
    elif blob.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# Age category logic
def age_to_category(age):
    if age <= 12:
        return 'child'
    elif 13 <= age <= 19:
        return 'teen'
    else:
        return 'adult'

# Map sentiment and age to genre
def sentiment_and_age_to_genre_id(sentiment, age):
    age_category = age_to_category(age)
    genre_from_age = AGE_GENRE_MAP.get(age_category, 18)  # Default to Drama for adults
    genre_from_sentiment = SENTIMENT_GENRE_MAP.get(sentiment, 35)  # Default to Comedy
    return [genre_from_sentiment, genre_from_age]

# Fetch movie recommendations from TMDB
def get_movie_recommendations_from_tmdb(sentiment, age):
    genre_ids = sentiment_and_age_to_genre_id(sentiment, age)
    url = f"{BASE_URL}/discover/movie"
    query_params = {
        'api_key': API_KEY,
        'with_genres': ','.join(map(str, genre_ids)),
        'sort_by': 'popularity.desc',
        'language': 'en-US'
    }
    try:
        response = requests.get(url, params=query_params, timeout=10)
        response.raise_for_status()
        data = response.json().get('results', [])[:5]
        return [(movie['title'],
                 movie.get('overview', 'No description'),
                 movie.get('release_date', 'Unknown'),
                 movie.get('vote_average', 0),
                 IMG_URL + movie['poster_path'] if movie.get('poster_path') else None) for movie in data]
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []

# Display movie recommendations
def display_recommendations(recommendations):
    # Clear previous recommendations
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    if not recommendations:
        tk.Label(scrollable_frame, text="No recommendations available.", wraplength=500, bg="#F7F7F7", fg="black").pack()

    for title, overview, release_date, rating, poster_url in recommendations:
        frame = tk.Frame(scrollable_frame, bg="#F7F7F7")
        frame.pack(pady=10, anchor="w", fill="x")

        # Display poster image
        if poster_url:
            try:
                response = requests.get(poster_url, stream=True)
                img_data = response.content
                img = Image.open(io.BytesIO(img_data))
                img = img.resize((100, 150), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                img_label = tk.Label(frame, image=img_tk, bg="#F7F7F7")
                img_label.image = img_tk
                img_label.grid(row=0, column=0, rowspan=4, padx=5, pady=5)
            except Exception as e:
                print(f"Failed to load image for {title}: {e}")
                tk.Label(frame, text="Image not available", bg="#F7F7F7", fg="black").grid(row=0, column=0, rowspan=4, padx=5, pady=5)

        # Display movie details
        tk.Label(frame, text=f"Title: {title}", font=("Helvetica Neue", 12, "bold"), bg="#F7F7F7", fg="#007AFF").grid(row=0, column=1, sticky='w')
        tk.Label(frame, text=f"Overview: {overview[:100]}...", wraplength=400, bg="#F7F7F7", fg="black").grid(row=1, column=1, sticky='w')
        tk.Label(frame, text=f"Release Date: {release_date}", bg="#F7F7F7", fg="black").grid(row=2, column=1, sticky='w')
        tk.Label(frame, text=f"Rating: {rating}", bg="#F7F7F7", fg="black").grid(row=3, column=1, sticky='w')

    # Update scrollregion after content is added
    canvas.config(scrollregion=canvas.bbox("all"))

# Save recommendations to database
def save_recommendations_to_db(recommendations, sentiment, user_name, user_age, user_gender):
    for title, overview, release_date, rating, _ in recommendations:
        c.execute(''' 
            INSERT INTO recommendations (sentiment, movie_title, overview, release_date, rating, user_name, user_age, user_gender)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (sentiment, title, overview, release_date, rating, user_name, user_age, user_gender))
    conn.commit()

# Handle submit button click
def on_submit():
    try:
        user_name = name_entry.get().strip()
        user_feeling = feeling_entry.get().strip()
        user_gender = gender_combobox.get().strip()
        user_age = int(age_entry.get().strip())
        
        sentiment = predict_sentiment(user_feeling)
        recommendations = get_movie_recommendations_from_tmdb(sentiment, user_age)
        
        display_recommendations(recommendations)
        save_recommendations_to_db(recommendations, sentiment, user_name, user_age, user_gender)
    except ValueError:
        print("Please enter valid details.")

# Set up main window (macOS theme style)
root = tk.Tk()
root.title("Manochitram")
root.geometry("600x600")
root.config(bg="#F7F7F7")  # macOS light background

# Header
header_frame = tk.Frame(root, bg="#007AFF")
header_frame.pack(fill="x", pady=10)
header_label = tk.Label(header_frame, text="Manochitram - Movie Recommender", font=("Helvetica Neue", 16, "bold"), bg="#007AFF", fg="white")
header_label.pack(pady=10)

# Input Frame
form_frame = tk.Frame(root, bg="#F7F7F7")
form_frame.pack(pady=20)

tk.Label(form_frame, text="Name:", bg="#F7F7F7", fg="black").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(form_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Feeling:", bg="#F7F7F7", fg="black").grid(row=1, column=0, padx=5, pady=5)
feeling_entry = tk.Entry(form_frame)
feeling_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Gender:", bg="#F7F7F7", fg="black").grid(row=2, column=0, padx=5, pady=5)
gender_combobox = Combobox(form_frame, values=["Male", "Female", "Other"])
gender_combobox.grid(row=2, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Age:", bg="#F7F7F7", fg="black").grid(row=3, column=0, padx=5, pady=5)
age_entry = tk.Entry(form_frame)
age_entry.grid(row=3, column=1, padx=5, pady=5)

submit_button = tk.Button(form_frame, text="Submit", command=on_submit, bg="#007AFF", fg="white")
submit_button.grid(row=4, columnspan=2, pady=10)

# Scrollable Canvas for Recommendations
canvas = tk.Canvas(root, bg="#F7F7F7")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#F7F7F7")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Run the application
root.mainloop()
