import csv
import random

# Seed for reproducible high-quality data generation
random.seed(42)

# Curated List of Real Iconic Global Movies
ICONIC_MOVIES = [
    # English Classics & Hits
    ("Inception", "Sci-Fi", "English", 8.8, 2010, "Christopher Nolan", "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page", "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.", 148, "Mind-Bending", "Dreams, Heist, Reality"),
    ("The Dark Knight", "Action", "English", 9.0, 2008, "Christopher Nolan", "Christian Bale, Heath Ledger, Aaron Eckhart", "When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of the greatest psychological tests.", 152, "Epic", "Superhero, Crime, Chaos"),
    ("Interstellar", "Sci-Fi", "English", 8.7, 2014, "Christopher Nolan", "Matthew McConaughey, Anne Hathaway, Jessica Chastain", "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", 169, "Epic", "Space, Time, Black Hole"),
    ("Pulp Fiction", "Crime", "English", 8.9, 1994, "Quentin Tarantino", "John Travolta, Uma Thurman, Samuel L. Jackson", "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", 154, "Fun & Entertaining", "Non-Linear, Gangster, Cult Classic"),
    ("The Shawshank Redemption", "Drama", "English", 9.3, 1994, "Frank Darabont", "Tim Robbins, Morgan Freeman, Bob Gunton", "Over the course of several years, two convicts form a friendship, seeking consolation and eventual redemption through basic compassion.", 142, "Inspiring", "Hope, Prison, Friendship"),
    ("The Godfather", "Crime", "English", 9.2, 1972, "Francis Ford Coppola", "Marlon Brando, Al Pacino, James Caan", "Don Vito Corleone, head of a mafia family, decides to hand over his empire to his youngest son Michael.", 175, "Epic", "Mafia, Family, Power"),
    ("Forrest Gump", "Drama", "English", 8.8, 1994, "Robert Zemeckis", "Tom Hanks, Robin Wright, Gary Sinise", "The history of the United States from the 1950s to the '70s unfolds from the perspective of an Alabama man with an IQ of 75.", 142, "Heartwarming", "Life, Destiny, Romance"),
    ("The Matrix", "Sci-Fi", "English", 8.7, 1999, "Lana Wachowski, Lilly Wachowski", "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss", "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth about the simulated reality.", 136, "Mind-Bending", "Cyberpunk, VR, Philosophy"),
    ("Gladiator", "Action", "English", 8.5, 2000, "Ridley Scott", "Russell Crowe, Joaquin Phoenix, Connie Nielsen", "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.", 155, "Epic", "Ancient Rome, Revenge, Honor"),
    ("Avatar", "Sci-Fi", "English", 7.9, 2009, "James Cameron", "Sam Worthington, Zoe Saldana, Sigourney Weaver", "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world.", 162, "Epic", "Aliens, Nature, Visual Spectacle"),
    ("Spider-Man: Into the Spider-Verse", "Animation", "English", 8.4, 2018, "Bob Persichetti, Peter Ramsey", "Shameik Moore, Jake Johnson, Hailee Steinfeld", "Teen Miles Morales becomes the new Spider-Man and must join forces with five spider-powered individuals from other dimensions.", 117, "Fun & Entertaining", "Multiverse, Animation, Origin"),
    ("Oppenheimer", "Biography", "English", 8.9, 2023, "Christopher Nolan", "Cillian Murphy, Emily Blunt, Matt Damon", "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.", 180, "Inspiring", "History, Atomic Bomb, Science"),
    ("Spirited Away", "Animation", "Japanese", 8.6, 2001, "Hayao Miyazaki", "Rumi Hiiragi, Miyu Irino, Mari Natsuki", "During her family's move to the suburbs, a 10-year-old girl wanders into a world ruled by gods, witches and spirits.", 125, "Heartwarming", "Studio Ghibli, Fantasy, Magic"),
    ("Your Name", "Animation", "Japanese", 8.4, 2016, "Makoto Shinkai", "Ryunosuke Kamiki, Mone Kamishibaiashi", "Two strangers find themselves linked in a bizarre way. When a connection forms, will distance be the only thing to keep them apart?", 106, "Emotional", "Body Swap, Fate, Romance"),
    ("Parasite", "Thriller", "Korean", 8.5, 2019, "Bong Joon Ho", "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong", "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.", 132, "Thrilling", "Social Commentary, Plot Twist, Masterpiece"),
    ("Train to Busan", "Horror", "Korean", 7.6, 2016, "Yeon Sang-ho", "Gong Yoo, Jung Yu-mi, Ma Dong-seok", "While a zombie virus breaks out in South Korea, passengers struggle to survive on the train from Seoul to Busan.", 118, "Scary", "Zombies, Survival, Action"),
    ("Oldboy", "Thriller", "Korean", 8.4, 2003, "Park Chan-wook", "Choi Min-sik, Yoo Ji-tae, Kang Hye-jung", "After being kidnapped and imprisoned for fifteen years, Oh Dae-su is released, only to find that he must find his captor in five days.", 120, "Dark", "Revenge, Mystery, Neo-Noir"),
    ("3 Idiots", "Comedy", "Hindi", 8.4, 2009, "Rajkumar Hirani", "Aamir Khan, Madhavan, Sharman Joshi", "Two friends are searching for their long lost companion. They revisit their college days and recall the memories of their friend who inspired them.", 170, "Heartwarming", "College, Friendship, Dreams"),
    ("Dangal", "Sports", "Hindi", 8.3, 2016, "Nitesh Tiwari", "Aamir Khan, Sakshi Tanwar, Fatima Sana Shaikh", "Former wrestler Mahavir Singh Phogat and his two wrestler daughters struggle towards glory at the Commonwealth Games.", 161, "Inspiring", "Wrestling, Family, Passion"),
    ("Lagaan", "Drama", "Hindi", 8.1, 2001, "Ashutosh Gowariker", "Aamir Khan, Gracy Singh, Rachel Shelley", "The people of a small village in Victorian India stake their future on a game of cricket against their ruthless British rulers.", 224, "Epic", "Cricket, Freedom, History"),
    ("Sholay", "Action", "Hindi", 8.2, 1975, "Ramesh Sippy", "Dharmendra, Amitabh Bachchan, Sanjeev Kumar", "After his family is murdered by a notorious bandit, a former police officer enlists the help of two outlaws to capture him.", 204, "Epic", "Cult Classic, Western, Revenge"),
    ("Baahubali: The Beginning", "Action", "Telugu", 8.0, 2015, "S.S. Rajamouli", "Prabhas, Rana Daggubati, Anushka Shetty", "In ancient India, an adventurous and daring man becomes involved in a decade-old feud between two warring people.", 159, "Epic", "Kingdom, War, Legend"),
    ("RRR", "Action", "Telugu", 7.8, 2022, "S.S. Rajamouli", "N.T. Rama Rao Jr., Ram Charan, Ajay Devgn", "A fearless revolutionary and an officer in the British force join hands to fight against tyranny.", 187, "Epic", "Friendship, Revolution, Action"),
    ("Vikram Vedha", "Action", "Tamil", 8.2, 2017, "Pushkar-Gayathri", "Madhavan, Vijay Sethupathi, Varalaxmi Sarathkumar", "A pragmatic police officer sets out to track down and kill an equally tough gangster. A moral dilemma arises when the gangster surrenders.", 147, "Mind-Bending", "Crime, Morality, Riddles"),
    ("Super Deluxe", "Drama", "Tamil", 8.3, 2019, "Thiagarajan Kumararaja", "Vijay Sethupathi, Fahadh Faasil, Samantha Ruth Prabhu", "An unfaithful wife, an angry boy, a transgender woman, and a priest find themselves in unexpected situations on a single day.", 176, "Dark", "Hyperlink, Drama, Neo-Noir"),
    ("Kantara", "Action", "Kannada", 8.2, 2022, "Rishab Shetty", "Rishab Shetty, Sapthami Gowda, Kishore", "When greed paves the way for betrayal, scheming, and murder, a young man takes up the torch of his ancestors to protect his village.", 148, "Epic", "Folklore, Nature, Divine"),
    ("Money Heist: The Movie", "Crime", "Spanish", 8.1, 2021, "Álvaro Morte", "Álvaro Morte, Úrsula Corberó, Itziar Ituño", "An unusual group of robbers attempt to carry out the most perfect robbery in Spanish history - stealing billions of euros.", 130, "Thrilling", "Heist, Strategy, Resistance"),
    ("Pan's Labyrinth", "Fantasy", "Spanish", 8.2, 2006, "Guillermo del Toro", "Ivana Baquero, Sergi López, Maribel Verdú", "In the Falangist Spain of 1944, the bookish young stepdaughter of a sadistic army officer escapes into an eerie fantasy world.", 118, "Dark", "Dark Fantasy, Magic, History"),
    ("Amélie", "Comedy", "French", 8.3, 2001, "Jean-Pierre Jeunet", "Audrey Tautou, Mathieu Kassovitz, Rufus", "Amélie is an innocent and naive girl in Paris with her own sense of justice. She decides to help those around her and finds love along the way.", 122, "Heartwarming", "Whimsical, Paris, Romance"),
    ("The Intouchables", "Biography", "French", 8.5, 2011, "Olivier Nakache, Éric Toledano", "François Cluzet, Omar Sy, Anne Le Ny", "After he becomes a quadriplegic from a paragliding accident, an aristocrat hires a young man from the projects to be his caregiver.", 112, "Heartwarming", "Friendship, Humor, True Story"),
    ("Dark Sight", "Sci-Fi", "German", 7.9, 2020, "Baran bo Odar", "Louis Hofmann, Oliver Masucci", "A missing child sets four families on a frantic hunt for answers as they unearth a mind-bending mystery that spans three generations.", 124, "Mind-Bending", "Time Travel, Mystery, Dark"),
    ("Life Is Beautiful", "Comedy", "Italian", 8.6, 1997, "Roberto Benigni", "Roberto Benigni, Nicoletta Braschi", "When an open-minded Jewish librarian and his son become victims of the Holocaust, he uses a perfect mixture of will, humor, and imagination.", 116, "Emotional", "War, Family, Hope"),
    ("Crouching Tiger, Hidden Dragon", "Action", "Mandarin", 7.9, 2000, "Ang Lee", "Chow Yun-Fat, Michelle Yeoh, Zhang Ziyi", "A young Chinese warrior steals a sword from a famed swordsman and then escapes into a world of romantic adventure with a mysterious man.", 120, "Epic", "Martial Arts, Romance, Swords"),
]

# Vocabulary generator helpers for procedurally building 1,200 total movies
ADJECTIVES = [
    "Silent", "Golden", "Forgotten", "Electric", "Midnight", "Infinite", "Rising", "Crystal", 
    "Parallel", "Northern", "Secret", "Mysterious", "Endless", "Wild", "Brave", "Falling", 
    "Bright", "Dark", "Royal", "Eternal", "Frozen", "Cosmic", "Phantom", "Quantum", "Shadow",
    "Hidden", "Neon", "Velvet", "Spectral", "Blazing", "Celestial", "Stormy", "Prismatic", "Enchanted"
]

NOUNS = [
    "Horizon", "Legacy", "Code", "Kingdom", "Signal", "Promise", "Beginning", "Discovery", 
    "Chapter", "Mission", "Destiny", "Empire", "Warrior", "Bridge", "Castle", "Garden", 
    "Planet", "Project", "Storm", "Miracle", "Frontier", "Sanctuary", "Eclipse", "Paradox",
    "Voyage", "Specter", "Matrix", "Rebellion", "Odyssey", "Labyrinth", "Ascent", "Chronicle"
]

GENRES = [
    "Action", "Sci-Fi", "Comedy", "Drama", "Thriller", "Romance", 
    "Horror", "Mystery", "Fantasy", "Animation", "Crime", "Adventure", "Sports"
]

LANGUAGES = [
    "English", "Hindi", "Korean", "Japanese", "Spanish", "French", "Tamil", "Telugu", "German", "Italian", "Mandarin"
]

DIRECTORS = [
    "Christopher Nolan", "Quentin Tarantino", "Steven Spielberg", "S.S. Rajamouli", "Bong Joon Ho",
    "Hayao Miyazaki", "Guillermo del Toro", "Denis Villeneuve", "Martin Scorsese", "Greta Gerwig",
    "Ridley Scott", "James Cameron", "Park Chan-wook", "Rajkumar Hirani", "Mani Ratnam", "Luc Besson"
]

CAST_MEMBERS = [
    "Leonardo DiCaprio, Joseph Gordon-Levitt", "Christian Bale, Heath Ledger", "Aamir Khan, Madhavan",
    "Song Kang-ho, Choi Min-sik", "Prabhas, Rana Daggubati", "Keanu Reeves, Laurence Fishburne",
    "Tom Hanks, Robin Wright", "Vijay Sethupathi, Fahadh Faasil", "Audrey Tautou, Mathieu Kassovitz",
    "Shah Rukh Khan, Deepika Padukone", "Robert Downey Jr., Scarlett Johansson", "Cillian Murphy, Emily Blunt"
]

MOODS = [
    "Mind-Bending", "Thrilling", "Heartwarming", "Dark", "Fun & Entertaining", "Epic", "Inspiring", "Scary", "Emotional"
]

def generate_full_dataset():
    movies = []
    movie_id = 1
    used_titles = set()

    # 1. Add iconic curated movies first
    for item in ICONIC_MOVIES:
        title, genre, language, rating, year, director, cast, desc, duration, mood, tags = item
        used_titles.add(title.lower())
        movies.append({
            "id": movie_id,
            "title": title,
            "genre": genre,
            "language": language,
            "rating": rating,
            "year": year,
            "director": director,
            "cast": cast,
            "description": desc,
            "poster_url": f"https://images.unsplash.com/photo-{1536440136628 + (movie_id % 100)}?w=400&q=80",
            "duration_min": duration,
            "mood": mood,
            "tags": tags
        })
        movie_id += 1

    # 2. Procedurally generate high-quality realistic movies up to 1,250 entries
    target_count = 1250
    while len(movies) < target_count:
        adj = random.choice(ADJECTIVES)
        noun = random.choice(NOUNS)
        title = f"The {adj} {noun}"
        if random.random() > 0.5:
            title = f"{adj} {noun}"

        if title.lower() in used_titles:
            continue

        used_titles.add(title.lower())

        genre = random.choice(GENRES)
        language = random.choice(LANGUAGES)
        
        # Realistic rating distribution skewed towards 6.0 - 9.2
        rating = round(random.triangular(5.2, 9.5, 7.6), 1)
        year = random.randint(1990, 2025)
        director = random.choice(DIRECTORS)
        cast = random.choice(CAST_MEMBERS)
        duration = random.randint(90, 180)
        mood = random.choice(MOODS)

        desc = f"An exhilarating {genre.lower()} cinematic experience in {language} about a secret {noun.lower()} that changes everything."
        tags = f"{genre}, {language}, {adj}, Cinema"

        # Varied Unsplash movie aesthetic poster placeholder images
        poster_id = 1500000000000 + (movie_id * 137 % 900000000)
        poster_url = f"https://picsum.photos/seed/movie_{movie_id}/400/600"

        movies.append({
            "id": movie_id,
            "title": title,
            "genre": genre,
            "language": language,
            "rating": rating,
            "year": year,
            "director": director,
            "cast": cast,
            "description": desc,
            "poster_url": poster_url,
            "duration_min": duration,
            "mood": mood,
            "tags": tags
        })
        movie_id += 1

    return movies

def save_to_csv(movies, filename="data/movies.csv"):
    fieldnames = [
        "id", "title", "genre", "language", "rating", "year", 
        "director", "cast", "description", "poster_url", "duration_min", "mood", "tags"
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for movie in movies:
            writer.writerow(movie)

if __name__ == "__main__":
    data = generate_full_dataset()
    save_to_csv(data)
    print(f"Successfully generated {len(data)} movies in data/movies.csv!")
