from flask import Flask, render_template, request, jsonify, send_from_directory, redirect
from werkzeug.middleware.proxy_fix import ProxyFix
import csv
import os

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# Support reverse proxy headers in production (Render, Railway, Heroku, Nginx, etc.)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "MovieMatch Recommendation Platform",
        "version": "1.0.0"
    }), 200

@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Resource not found", "status_code": 404}), 404
    return redirect("/")

@app.errorhandler(500)
def internal_error(error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Internal server error", "status_code": 500}), 500
    return jsonify({"error": "Internal server error"}), 500

@app.route("/static/style")
@app.route("/style.css")
def redirect_style():
    return send_from_directory(os.path.join(app.root_path, "static"), "style.css", mimetype="text/css")

# ==================================================
# LOAD MOVIES DATASET
# ==================================================

def load_movies():
    movies = []
    csv_path = os.path.join(os.path.dirname(__file__), "data", "movies.csv")
    
    if not os.path.exists(csv_path):
        return movies

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                movie = {
                    "id": int(row.get("id", 0)),
                    "title": row.get("title", "Untitled").strip(),
                    "genre": row.get("genre", "General").strip(),
                    "language": row.get("language", "English").strip(),
                    "rating": float(row.get("rating", 7.0)),
                    "year": int(row.get("year", 2020)),
                    "director": row.get("director", "Unknown Director").strip(),
                    "cast": row.get("cast", "Unknown Cast").strip(),
                    "description": row.get("description", "No description available.").strip(),
                    "poster_url": row.get("poster_url", "").strip(),
                    "duration_min": int(row.get("duration_min", 120)),
                    "mood": row.get("mood", "Entertaining").strip(),
                    "tags": row.get("tags", "").strip()
                }
                movies.append(movie)
            except (ValueError, TypeError):
                continue

    return movies


# ==================================================
# ADVANCED RULE-BASED RECOMMENDATION ENGINE
# ==================================================

def recommend_movies(
    movies,
    genre="",
    language="",
    min_rating=0.0,
    min_year=1970,
    max_year=2025,
    mood="",
    query="",
    algo_mode="standard",
    limit=24
):
    results = []

    for movie in movies:
        score = 0
        reasons = []

        # -----------------------------
        # SEARCH QUERY FILTER & SCORE
        # -----------------------------
        if query:
            q_lower = query.lower()
            t_lower = movie["title"].lower()
            d_lower = movie["director"].lower()
            c_lower = movie["cast"].lower()
            g_lower = movie["genre"].lower()
            tags_lower = movie["tags"].lower()

            if (q_lower not in t_lower and 
                q_lower not in d_lower and 
                q_lower not in c_lower and 
                q_lower not in g_lower and 
                q_lower not in tags_lower):
                continue
            
            score += 15
            reasons.append("Search Keyword Match (+15)")

        # -----------------------------
        # GENRE RULE
        # -----------------------------
        if genre:
            if movie["genre"].lower() != genre.lower():
                continue
            score += 30
            reasons.append(f"{genre} Genre Match (+30)")

        # -----------------------------
        # LANGUAGE RULE
        # -----------------------------
        if language:
            if movie["language"].lower() != language.lower():
                continue
            score += 20
            reasons.append(f"{language} Language Match (+20)")

        # -----------------------------
        # RATING RULE
        # -----------------------------
        if movie["rating"] < min_rating:
            continue

        if movie["rating"] >= 8.5:
            r_pts = 35 if algo_mode == "top_rated" else 30
            score += r_pts
            reasons.append(f"Masterpiece Rating ({movie['rating']} ⭐)")
        elif movie["rating"] >= 7.5:
            r_pts = 25 if algo_mode == "top_rated" else 20
            score += r_pts
            reasons.append(f"High Rating ({movie['rating']} ⭐)")
        elif movie["rating"] >= 6.0:
            score += 10
            reasons.append(f"Good Rating ({movie['rating']} ⭐)")

        # -----------------------------
        # YEAR & ERA RULE
        # -----------------------------
        if movie["year"] < min_year or movie["year"] > max_year:
            continue

        if algo_mode == "cult_classics" and movie["year"] < 2010 and movie["rating"] >= 8.0:
            score += 15
            reasons.append("Cult Classic Bonus (+15)")
        elif algo_mode == "recent_hits" and movie["year"] >= 2018:
            score += 15
            reasons.append("Recent Release Bonus (+15)")

        if movie["year"] >= 2020:
            score += 10
            reasons.append("2020s Era (+10)")
        elif movie["year"] >= 2010:
            score += 7
            reasons.append("2010s Era (+7)")
        else:
            score += 5
            reasons.append("Classic Era (+5)")

        # -----------------------------
        # MOOD BONUS RULE
        # -----------------------------
        if mood:
            if movie["mood"].lower() == mood.lower():
                score += 10
                reasons.append(f"{mood} Vibe Match (+10)")

        # Cap score at 100%
        final_score = min(100, score)

        movie_copy = movie.copy()
        movie_copy["score"] = final_score
        movie_copy["reasons"] = reasons
        results.append(movie_copy)

    # Initial sorting by recommendation score descending
    results.sort(key=lambda x: (x["score"], x["rating"]), reverse=True)
    return results[:limit]


# ==================================================
# HOME PAGE ROUTE
# ==================================================

@app.route("/")
def home():
    movies = load_movies()
    genres = sorted(list(set(m["genre"] for m in movies if m["genre"])))
    languages = sorted(list(set(m["language"] for m in movies if m["language"])))
    moods = sorted(list(set(m["mood"] for m in movies if m["mood"])))
    
    # Calculate stats for dataset dashboard
    avg_rating = round(sum(m["rating"] for m in movies) / len(movies), 1) if movies else 0.0
    
    return render_template(
        "index.html",
        total_movies=len(movies),
        genres=genres,
        languages=languages,
        moods=moods,
        avg_rating=avg_rating
    )


# ==================================================
# MOVIE SEARCH AUTOCOMPLETE
# ==================================================

@app.route("/search")
def search_movies():
    query = request.args.get("q", "").strip().lower()
    movies = load_movies()

    if not query:
        return jsonify([])

    matches = []
    for movie in movies:
        if (query in movie["title"].lower() or 
            query in movie["director"].lower() or 
            query in movie["cast"].lower() or
            query in movie["genre"].lower() or
            query in movie["tags"].lower()):
            matches.append({
                "id": movie["id"],
                "title": movie["title"],
                "genre": movie["genre"],
                "language": movie["language"],
                "rating": movie["rating"],
                "year": movie["year"],
                "director": movie["director"],
                "cast": movie["cast"],
                "poster_url": movie["poster_url"],
                "mood": movie["mood"]
            })

    # Sort matches by title relevance / rating
    matches.sort(key=lambda x: x["rating"], reverse=True)
    return jsonify(matches[:10])


# ==================================================
# RECOMMENDATIONS PAGE ROUTE
# ==================================================

@app.route("/recommendations", methods=["GET", "POST"])
def recommendations():
    movies = load_movies()

    if request.method == "POST":
        genre = request.form.get("genre", "")
        language = request.form.get("language", "")
        min_rating = float(request.form.get("rating", 0.0))
        min_year = int(request.form.get("min_year", 1970))
        max_year = int(request.form.get("max_year", 2025))
        mood = request.form.get("mood", "")
        query = request.form.get("query", "")
        algo_mode = request.form.get("algo_mode", "standard")
        sort_by = request.form.get("sort", "score")
    else:
        genre = request.args.get("genre", "")
        language = request.args.get("language", "")
        min_rating = float(request.args.get("rating", 0.0))
        min_year = int(request.args.get("min_year", 1970))
        max_year = int(request.args.get("max_year", 2025))
        mood = request.args.get("mood", "")
        query = request.args.get("query", "")
        algo_mode = request.args.get("algo_mode", "standard")
        sort_by = request.args.get("sort", "score")

    results = recommend_movies(
        movies,
        genre=genre,
        language=language,
        min_rating=min_rating,
        min_year=min_year,
        max_year=max_year,
        mood=mood,
        query=query,
        algo_mode=algo_mode,
        limit=30
    )

    # Sort results
    if sort_by == "rating":
        results.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == "year":
        results.sort(key=lambda x: x["year"], reverse=True)
    elif sort_by == "duration":
        results.sort(key=lambda x: x["duration_min"], reverse=True)
    elif sort_by == "title":
        results.sort(key=lambda x: x["title"].lower())
    else:
        results.sort(key=lambda x: (x["score"], x["rating"]), reverse=True)

    return render_template(
        "recommendations.html",
        recommendations=results,
        genre=genre,
        language=language,
        min_rating=min_rating,
        min_year=min_year,
        max_year=max_year,
        mood=mood,
        query=query,
        algo_mode=algo_mode,
        sort_by=sort_by
    )


# ==================================================
# API ENDPOINTS FOR FRONTEND INTERACTION
# ==================================================

@app.route("/api/movie/<int:movie_id>")
def get_movie_detail(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m["id"] == movie_id), None)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    
    # Also find 3 similar movies by genre
    similar = [m for m in movies if m["genre"] == movie["genre"] and m["id"] != movie["id"]]
    similar.sort(key=lambda x: x["rating"], reverse=True)
    
    movie_detail = movie.copy()
    movie_detail["similar_movies"] = similar[:3]
    return jsonify(movie_detail)


@app.route("/api/stats")
def api_stats():
    movies = load_movies()
    total = len(movies)
    
    genre_counts = {}
    lang_counts = {}
    for m in movies:
        genre_counts[m["genre"]] = genre_counts.get(m["genre"], 0) + 1
        lang_counts[m["language"]] = lang_counts.get(m["language"], 0) + 1

    top_rated = sorted(movies, key=lambda x: x["rating"], reverse=True)[:5]

    return jsonify({
        "total_movies": total,
        "genres": genre_counts,
        "languages": lang_counts,
        "top_rated": [{"id": m["id"], "title": m["title"], "rating": m["rating"], "genre": m["genre"]} for m in top_rated]
    })


# ==================================================
# RUN APP
# ==================================================

if __name__ == "__main__":
    import os
    import sys

    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")

    print("\n=======================================================")
    print("🎬 MovieMatch Production-Ready Server Running!")
    print(f"📍 Local Link: http://127.0.0.1:{port}")
    print(f"🌐 Host Binding: http://{host}:{port}")
    print("=======================================================\n")

    app.run(
        host=host,
        port=port,
        debug=False
    )