import sys
import os
sys.path.insert(0, os.path.abspath("."))
import app

movies = app.load_movies()
print(f"Loaded {len(movies)} movies.")

assert len(movies) >= 1200, "Movies dataset should have at least 1200 items"

# Test recommendation function
recs = app.recommend_movies(movies, genre="Sci-Fi", language="English", min_rating=7.0, mood="Mind-Bending")
print(f"Sci-Fi English recs count: {len(recs)}")
if recs:
    print("Top Rec Title:", recs[0]["title"], "| Score:", recs[0]["score"])

# Test Flask app client
with app.app.test_client() as client:
    res_home = client.get("/")
    assert res_home.status_code == 200, f"Home page returned {res_home.status_code}"
    print("Home page status 200 OK")

    res_search = client.get("/search?q=inception")
    assert res_search.status_code == 200, f"Search returned {res_search.status_code}"
    search_json = res_search.get_json()
    print("Search query result count:", len(search_json))

    res_recs = client.post("/recommendations", data={
        "genre": "Action",
        "language": "English",
        "rating": "8.0",
        "min_year": "2000",
        "max_year": "2025",
        "sort": "score",
        "algo_mode": "top_rated"
    })
    assert res_recs.status_code == 200, f"Recommendations page returned {res_recs.status_code}"
    print("Recommendations page status 200 OK")

    res_movie = client.get("/api/movie/1")
    assert res_movie.status_code == 200, f"Movie detail API returned {res_movie.status_code}"
    print("Movie detail API 200 OK for ID 1:", res_movie.get_json()["title"])

    res_stats = client.get("/api/stats")
    assert res_stats.status_code == 200, f"Stats API returned {res_stats.status_code}"
    print("Stats API 200 OK")

    res_health = client.get("/health")
    assert res_health.status_code == 200, f"Health check returned {res_health.status_code}"
    assert res_health.get_json()["status"] == "healthy", "Service health check healthy"
    print("Health check endpoint 200 OK")

print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
