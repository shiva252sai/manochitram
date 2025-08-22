

# Manochitram – Mood-Based Movie Recommendation System

Manochitram is a modern, user-friendly desktop application that recommends movies based on the user's **mood** and **age group**. It features sentiment analysis using TextBlob, a macOS-inspired interface with light/dark mode, real-time TMDB API integration for movie posters, and an exportable recommendation history.

---

## Features

### 🎭 Personalized Movie Recommendations

Get movie suggestions tailored to your mood (happy, sad, neutral) and age group using **TextBlob sentiment analysis** and age-based genre mapping.

### 🧠 Sentiment Analysis Integration

Analyze user input to detect emotional tone (positive, neutral, or negative) and match suitable movie genres automatically.

### 🎨 macOS-Inspired User Interface

A clean, modern, and visually appealing UI styled like macOS with easy-to-use controls.

### 🌙 Light/Dark Mode Toggle

Switch between light and dark themes instantly for a comfortable viewing experience.

### 🖼️ Real-Time Movie Posters

Fetch high-quality poster images from the TMDB API with fallback images for missing posters.

### 📜 Recommendation History & Export

View your complete recommendation history (100+ entries) and export it to a CSV file for future use.

### 🔒 Secure API Key Management

Keep your TMDB API key in a separate file for security and easy updates.

---

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a TMDB API Key

* Sign up at [TMDB](https://www.themoviedb.org/)
* Navigate to **Profile → Settings → API**
* Generate an API key (v3)

### 3. Add Your API Key

Create a file named `apikeytmdb.txt` and add your API key:

```
tmdb api key :YOUR_TMDB_API_KEY
```

### 4. Run the Application

```bash
python manochitramcode.py
```

---

## Usage

1. Enter your **name, mood, gender, and age**.
2. Click **Submit** to get personalized recommendations.
3. Toggle **Dark Mode** for a different UI theme.
4. Click **View History** to see/export past recommendations.

---

## Tech Stack

* **Languages:** Python
* **Libraries & Tools:** Tkinter, TextBlob, Pillow, Requests, SQLite
* **APIs:** TMDB API

---

## Dependencies

* Python 3.x
* TextBlob
* Pillow
* Requests
* Tkinter

---

## License

This project is for personal and educational use. Refer to TMDB’s terms for API usage guidelines.

---

## Credits

* **TMDB API** – Movie database and poster integration
* **TextBlob** – Sentiment analysis
* **Pillow** – Image handling in Python

---

If you want, I can make a **diagram and screenshots section** so your README looks like a polished open-source project.
Do you want me to create that? It will make it visually impressive.
