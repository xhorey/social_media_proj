from django.core.management.base import BaseCommand
from core.models import Category, KeyWord

categories = {

    "Technology": [
        "technology", "tech", "gadgets", "innovation", "hardware",
        "software", "devices", "electronics", "future", "digital",
        "computing", "engineering", "internet", "machines", "science",
        "research", "industry", "development", "modern technology", "tech news"
    ],

    "Programming": [
        "programming", "coding", "developer", "software development", "algorithms",
        "computer science", "code", "debugging", "open source", "development",
        "software", "programmer", "programming languages", "engineering", "projects",
        "application", "development tools", "source code", "technical", "coding tutorial"
    ],

    "Python": [
        "python", "django", "flask", "fastapi", "pandas",
        "numpy", "automation", "scripting", "backend", "pip",
        "python programming", "machine learning", "data science", "programming",
        "jupyter", "scikit learn", "python developer", "pytest", "asyncio", "python code"
    ],

    "JavaScript": [
        "javascript", "typescript", "nodejs", "react", "vue",
        "angular", "frontend", "web development", "npm", "ecmascript",
        "js", "web apps", "browser", "nextjs", "express",
        "javascript programming", "web applications", "frontend development",
        "react native", "webpack"
    ],

    "C Programming": [
        "c", "c programming", "gcc", "pointers", "memory",
        "low level", "systems programming", "embedded", "malloc", "linux",
        "compiler", "programming", "data structures", "operating systems",
        "computer science", "debugging", "header files", "c language",
        "performance", "software"
    ],

    "C++": [
        "cpp", "c++", "cplusplus", "programming", "object oriented",
        "stl", "templates", "game development", "unreal engine", "pointers",
        "memory management", "software", "algorithms", "competitive programming",
        "classes", "inheritance", "performance", "systems programming",
        "compiler", "coding"
    ],

    "Rust": [
        "rust", "rustlang", "cargo", "systems programming", "memory safety",
        "ownership", "borrowing", "programming", "backend", "webassembly",
        "wasm", "compiler", "low level", "software", "performance",
        "async rust", "tokio", "crates", "developer", "coding"
    ],

    "Web Development": [
        "web development", "website", "html", "css", "frontend",
        "backend", "full stack", "api", "web design", "responsive",
        "web app", "javascript", "server", "database", "developer",
        "web programming", "frontend development", "backend development",
        "websites", "internet"
    ],

    "Frontend Development": [
        "frontend", "frontend development", "html", "css", "javascript",
        "react", "vue", "angular", "ui", "user interface",
        "web design", "responsive design", "web apps", "browser",
        "typescript", "nextjs", "tailwind", "components", "website", "developer"
    ],

    "Backend Development": [
        "backend", "backend development", "server", "api", "database",
        "django", "nodejs", "python", "php", "java",
        "authentication", "rest api", "graphql", "microservices", "web server",
        "software", "programming", "cloud", "scaling", "developer"
    ],

    "Mobile Development": [
        "mobile", "android", "ios", "iphone", "app development",
        "flutter", "react native", "swift", "kotlin", "smartphone",
        "mobile apps", "app developer", "mobile software", "google play",
        "app store", "ios development", "android development", "cross platform",
        "applications", "technology"
    ],

    "Artificial Intelligence": [
        "ai", "artificial intelligence", "machine learning", "deep learning", "neural networks",
        "chatgpt", "llm", "automation", "robotics", "generative ai",
        "computer vision", "natural language processing", "data", "algorithms",
        "models", "training", "research", "openai", "ai tools", "technology"
    ],

    "Machine Learning": [
        "machine learning", "ml", "artificial intelligence", "data science", "deep learning",
        "neural networks", "algorithms", "training", "models", "prediction",
        "classification", "regression", "python", "tensorflow", "pytorch",
        "datasets", "statistics", "automation", "research", "ai"
    ],

    "Data Science": [
        "data science", "data", "analytics", "python", "machine learning",
        "statistics", "ai", "big data", "visualization", "programming",
        "pandas", "numpy", "datasets", "data analysis", "research",
        "sql", "models", "business intelligence", "mathematics", "technology"
    ],

    "Cybersecurity": [
        "cybersecurity", "hacking", "security", "ethical hacking", "malware",
        "privacy", "encryption", "penetration testing", "vulnerability", "infosec",
        "cyber attack", "network security", "passwords", "firewall", "threats",
        "security research", "digital security", "cyber crime", "defense", "linux"
    ],

    "Linux": [
        "linux", "ubuntu", "unix", "open source", "terminal",
        "bash", "server", "programming", "operating system", "software",
        "debian", "arch linux", "fedora", "shell", "command line",
        "kernel", "system administration", "linux desktop", "gnu", "computer"
    ],

    "Cloud Computing": [
        "cloud", "aws", "azure", "google cloud", "servers",
        "devops", "infrastructure", "hosting", "technology", "computing",
        "cloud services", "cloud storage", "virtual machines", "kubernetes",
        "docker", "serverless", "cloud security", "deployment", "databases", "software"
    ],

    "DevOps": [
        "devops", "docker", "kubernetes", "ci cd", "deployment",
        "automation", "linux", "cloud", "servers", "infrastructure",
        "github actions", "jenkins", "terraform", "monitoring", "containers",
        "software development", "devops engineer", "cloud computing", "scripting", "backend"
    ],

    "Databases": [
        "database", "sql", "postgresql", "mysql", "sqlite",
        "mongodb", "redis", "data", "backend", "orm",
        "query", "database design", "nosql", "postgres", "relational database",
        "data storage", "server", "programming", "analytics", "software"
    ],

    "Game Development": [
        "game development", "games", "unity", "unreal engine", "gamedev",
        "programming", "game design", "indie games", "video games", "developer",
        "csharp", "c++", "3d", "2d", "graphics",
        "game engine", "level design", "characters", "gameplay", "gaming"
    ],

    "Unity": [
        "unity", "unity3d", "game development", "csharp", "games",
        "game engine", "indie game", "3d", "2d", "gamedev",
        "assets", "shader", "gameplay", "animation", "physics",
        "mobile games", "vr", "ar", "developer", "video games"
    ],

    "Unreal Engine": [
        "unreal engine", "ue5", "ue4", "game development", "gaming",
        "c++", "blueprints", "3d", "game engine", "gamedev",
        "graphics", "metahuman", "nanite", "lumen", "virtual production",
        "gameplay", "animation", "level design", "video games", "developer"
    ],

    "Robotics": [
        "robotics", "robots", "automation", "engineering", "ai",
        "machines", "technology", "programming", "research", "future",
        "robot", "mechanical engineering", "electronics", "sensors", "hardware",
        "artificial intelligence", "industrial robots", "drones", "innovation", "science"
    ],

    "Engineering": [
        "engineering", "mechanical", "electrical", "civil", "software",
        "design", "technology", "construction", "innovation", "science",
        "engineering projects", "systems", "manufacturing", "research",
        "mathematics", "physics", "automation", "industry", "engineer"
    ],

    # =========================
    # SCIENCE
    # =========================

    "Science": [
        "science", "research", "discovery", "experiment", "laboratory",
        "physics", "chemistry", "biology", "scientist", "innovation",
        "scientific research", "technology", "medicine", "space",
        "nature", "evidence", "theory", "experiments", "knowledge"
    ],

    "Physics": [
        "physics", "quantum physics", "relativity", "mechanics", "energy",
        "particles", "space", "gravity", "matter", "quantum",
        "theoretical physics", "astrophysics", "thermodynamics", "electromagnetism",
        "physics research", "science", "universe", "atoms", "waves", "mathematics"
    ],

    "Chemistry": [
        "chemistry", "molecules", "atoms", "chemical reactions", "laboratory",
        "elements", "organic chemistry", "chemicals", "periodic table", "science",
        "inorganic chemistry", "biochemistry", "experiments", "research",
        "compounds", "molecular", "chemical engineering", "physics", "biology", "laboratory work"
    ],

    "Biology": [
        "biology", "cells", "genetics", "evolution", "animals",
        "plants", "microbiology", "organisms", "nature", "life",
        "biotechnology", "ecology", "human biology", "research",
        "science", "dna", "molecular biology", "biology research", "species", "medicine"
    ],

    "Space": [
        "space", "nasa", "astronomy", "universe", "planets",
        "stars", "galaxy", "black holes", "rocket", "cosmos",
        "astrophysics", "space news", "astronauts", "moon",
        "mars", "telescope", "solar system", "science", "space exploration", "宇宙"
    ],

    "Space Exploration": [
        "space exploration", "nasa", "spacex", "rockets", "moon",
        "mars", "astronauts", "spacecraft", "science", "astronomy",
        "satellites", "apollo", "space mission", "rocket launch",
        "international space station", "iss", "cosmos", "universe", "technology", "aerospace"
    ],

    "Environment": [
        "environment", "climate", "global warming", "sustainability", "pollution",
        "recycling", "nature", "energy", "conservation", "earth",
        "carbon", "emissions", "ecology", "green energy", "climate change",
        "wildlife", "renewable energy", "environmental protection", "planet", "sustainability"
    ],

    "Climate": [
        "climate", "climate change", "global warming", "weather", "environment",
        "carbon", "emissions", "sustainability", "science", "earth",
        "climate crisis", "greenhouse gases", "temperature", "drought",
        "flooding", "renewable energy", "environment", "research", "pollution", "planet"
    ],

    "Medicine": [
        "medicine", "medical", "doctor", "hospital", "healthcare",
        "disease", "treatment", "research", "surgery", "patients",
        "medical science", "health", "pharmaceuticals", "diagnosis",
        "clinical", "biology", "medicine news", "healthcare system", "therapy", "science"
    ],

    "Psychology": [
        "psychology", "mental health", "behavior", "mind", "brain",
        "personality", "emotions", "therapy", "science", "psychology research",
        "human behavior", "cognitive science", "relationships", "memory",
        "motivation", "psychologist", "mental wellbeing", "neuroscience", "personality types", "mindset"
    ],

    "Neuroscience": [
        "neuroscience", "brain", "neuron", "neural", "psychology",
        "cognition", "memory", "consciousness", "biology", "science",
        "neurobiology", "brain research", "mental health", "neurotechnology",
        "behavior", "mind", "medical research", "learning", "nervous system", "medicine"
    ],

    # =========================
    # GAMING
    # =========================

    "Gaming": [
        "gaming", "games", "video games", "gamer", "esports",
        "console", "pc gaming", "gameplay", "gaming news", "streaming",
        "multiplayer", "single player", "game review", "gaming community",
        "game releases", "game industry", "online gaming", "competitive gaming",
        "gaming setup", "entertainment"
    ],

    "PC Gaming": [
        "pc gaming", "steam", "gaming pc", "graphics card", "keyboard",
        "mouse", "fps", "mods", "hardware", "games",
        "computer gaming", "gaming setup", "nvidia", "amd", "gaming monitor",
        "gaming laptop", "pc build", "steam games", "gameplay", "gaming hardware"
    ],

    "PlayStation": [
        "playstation", "ps5", "ps4", "sony", "console",
        "dual sense", "playstation plus", "exclusive", "gaming", "psn",
        "playstation games", "ps5 games", "playstation news", "controller",
        "god of war", "spider man", "the last of us", "gran turismo",
        "console gaming", "video games"
    ],

    "Xbox": [
        "xbox", "xbox series x", "xbox series s", "microsoft", "game pass",
        "console", "halo", "forza", "gaming", "controller",
        "xbox games", "xbox live", "xbox news", "gaming console",
        "game pass ultimate", "microsoft gaming", "console gaming", "video games",
        "xbox one", "games"
    ],

    "Nintendo": [
        "nintendo", "switch", "mario", "zelda", "pokemon",
        "animal crossing", "console", "games", "gaming", "switch 2",
        "nintendo games", "super mario", "legend of zelda", "kirby",
        "splatoon", "smash bros", "pokemon games", "handheld", "console gaming", "video games"
    ],

    "Mobile Gaming": [
        "mobile games", "android games", "ios games", "gacha", "clash royale",
        "genshin impact", "honkai", "gaming", "multiplayer", "free to play",
        "mobile gaming", "smartphone games", "app games", "rpg",
        "strategy games", "online games", "phone games", "gaming apps", "competitive gaming", "games"
    ],

    "Esports": [
        "esports", "competitive gaming", "tournament", "league", "championship",
        "professional gaming", "players", "team", "competition", "gaming",
        "esports news", "pro gaming", "tournaments", "world championship",
        "gaming competition", "esports teams", "esports players", "gaming league",
        "competitive games", "streaming"
    ],

    "Dota 2": [
        "dota", "dota 2", "moba", "valve", "heroes",
        "ancient", "ranked", "tournament", "esports", "gaming",
        "the international", "ti", "dota gameplay", "dota heroes",
        "mmr", "support", "carry", "mid lane", "offlane", "steam"
    ],

    "League of Legends": [
        "league of legends", "lol", "moba", "riot games", "champions",
        "summoners rift", "ranked", "esports", "gaming", "tournament",
        "league gameplay", "worlds", "lcs", "mid lane",
        "top lane", "adc", "support", "jungler", "riot", "champions"
    ],

    "Minecraft": [
        "minecraft", "mojang", "survival", "creative", "building",
        "crafting", "minecraft server", "mods", "redstone", "gaming",
        "minecraft gameplay", "minecraft update", "blocks", "villagers",
        "nether", "ender dragon", "minecraft community", "sandbox", "multiplayer", "video games"
    ],

    "RPG Games": [
        "rpg", "role playing games", "games", "characters", "story",
        "quests", "open world", "fantasy", "gaming", "leveling",
        "party", "combat", "loot", "adventure", "turn based",
        "action rpg", "jrpg", "character progression", "video games", "gameplay"
    ],

    "Strategy Games": [
        "strategy games", "strategy", "real time strategy", "rts", "turn based",
        "tactics", "civilization", "age of empires", "gaming", "games",
        "management", "war games", "strategy gaming", "build order",
        "resource management", "competitive gaming", "board games", "simulation", "planning", "gameplay"
    ],

    "Horror Games": [
        "horror games", "horror", "survival horror", "scary games", "games",
        "resident evil", "silent hill", "monsters", "zombies", "gaming",
        "fear", "psychological horror", "indie horror", "jumpscare",
        "horror gameplay", "dead by daylight", "outlast", "alan wake", "thriller", "video games"
    ],

    # =========================
    # MOVIES, TV & ANIME
    # =========================

    "Movies": [
        "movies", "films", "cinema", "hollywood", "actors",
        "directors", "blockbuster", "movie review", "film", "entertainment",
        "new movies", "movie news", "film industry", "screenplay",
        "movie trailer", "action movies", "drama movies", "comedy movies",
        "movie recommendations", "cinematography"
    ],

    "TV Shows": [
        "tv", "television", "series", "netflix", "hbo",
        "amazon prime", "streaming", "episodes", "drama", "entertainment",
        "tv series", "show recommendations", "tv news", "season",
        "characters", "television shows", "streaming series", "new shows",
        "watching", "episodes"
    ],

    "Anime": [
        "anime", "manga", "japan", "otaku", "shonen",
        "isekai", "animation", "anime news", "characters", "japanese",
        "shoujo", "seinen", "mecha", "cosplay", "anime recommendations",
        "anime series", "japanese animation", "weeb", "anime community", "otaku culture"
    ],

    "Manga": [
        "manga", "japanese comics", "anime", "manhwa", "webtoon",
        "shonen", "shoujo", "seinen", "manga reader", "japan",
        "manga recommendations", "manga series", "comic books", "otaku",
        "mangaka", "illustration", "fiction", "characters", "japanese culture", "reading"
    ],

    "Science Fiction": [
        "science fiction", "sci fi", "space", "future", "aliens",
        "robots", "books", "movies", "technology", "fiction",
        "dystopia", "time travel", "artificial intelligence", "space opera",
        "cyberpunk", "fantasy", "science fiction movies", "science fiction books",
        "futuristic", "speculative fiction"
    ],

    "Horror": [
        "horror", "scary", "films", "movies", "ghosts",
        "monsters", "supernatural", "thriller", "fear", "books",
        "psychological horror", "horror movies", "horror stories", "paranormal",
        "vampires", "zombies", "creepy", "haunted", "slasher", "dark"
    ],

    "Comedy": [
        "comedy", "funny", "humor", "stand up", "jokes",
        "comedian", "entertainment", "memes", "laughs", "fun",
        "comedy shows", "funny videos", "satire", "parody",
        "comedy movies", "standup comedy", "improv", "sketch comedy", "humour", "laughing"
    ],

    "Documentaries": [
        "documentary", "documentaries", "real stories", "nonfiction", "history",
        "science", "nature", "investigation", "journalism", "film",
        "documentary film", "true story", "society", "culture",
        "politics", "biography", "research", "real life", "streaming", "education"
    ],

    # =========================
    # MUSIC
    # =========================

    "Music": [
        "music", "songs", "albums", "artists", "concerts",
        "music industry", "playlist", "new music", "singing", "entertainment",
        "music news", "musician", "recording", "songwriting", "lyrics",
        "music production", "live music", "music recommendations", "audio", "sound"
    ],

    "Hip Hop": [
        "hip hop", "rap", "rapper", "trap", "hip hop music",
        "freestyle", "beats", "album", "artist", "music",
        "rap music", "hip hop culture", "lyrics", "mixtape",
        "producer", "underground rap", "drill", "hip hop news", "bars", "emcee"
    ],

    "Rock Music": [
        "rock", "rock music", "guitar", "band", "metal",
        "punk", "alternative", "concert", "album", "music",
        "classic rock", "hard rock", "indie rock", "rock band",
        "lead guitar", "bass", "drums", "rock concert", "music history", "musician"
    ],

    "Electronic Music": [
        "edm", "electronic music", "techno", "house", "dubstep",
        "dj", "festival", "producer", "beats", "music",
        "trance", "drum and bass", "electro", "deep house",
        "dance music", "music production", "synthesizer", "rave", "club music", "remix"
    ],

    "Classical Music": [
        "classical music", "orchestra", "piano", "violin", "symphony",
        "composer", "concert", "bach", "mozart", "beethoven",
        "classical", "opera", "music theory", "conductor",
        "string instruments", "piano music", "musician", "baroque", "romantic music", "instrumental"
    ],

    "Music Production": [
        "music production", "producer", "fl studio", "ableton", "logic pro",
        "recording", "mixing", "mastering", "beats", "music",
        "audio engineering", "sound design", "vst", "plugins",
        "synthesizer", "drums", "songwriting", "studio", "producer tips", "music technology"
    ],

    # =========================
    # SPORTS
    # =========================

    "Sports": [
        "sports", "athletics", "competition", "championship", "team",
        "players", "training", "tournament", "fitness", "sports news",
        "professional sports", "athletes", "games", "sporting events",
        "competition", "league", "sports community", "coaching", "performance", "exercise"
    ],

    "Football": [
        "football", "soccer", "premier league", "champions league", "fifa",
        "goals", "clubs", "players", "transfer", "football news",
        "world cup", "uefa", "la liga", "bundesliga",
        "serie a", "ligue 1", "football match", "manager", "striker", "defender"
    ],

    "Basketball": [
        "basketball", "nba", "wnba", "nba finals", "dunk",
        "players", "teams", "basketball news", "sports", "game",
        "college basketball", "playoffs", "basketball player", "point guard",
        "shooting guard", "center", "forward", "basketball training", "hoops", "league"
    ],

    "Tennis": [
        "tennis", "atp", "wta", "grand slam", "wimbledon",
        "us open", "french open", "australian open", "players", "sports",
        "tennis match", "tennis player", "serve", "forehand",
        "backhand", "court", "ranking", "championship", "racket", "tournament"
    ],

    "Formula 1": [
        "formula 1", "f1", "racing", "grand prix", "ferrari",
        "mercedes", "red bull racing", "drivers", "motorsport", "racing",
        "formula one", "f1 news", "race weekend", "qualifying",
        "pit stop", "formula 1 drivers", "motorsport news", "cars", "championship", "racing team"
    ],

    "MMA": [
        "mma", "ufc", "fighting", "martial arts", "fighter",
        "boxing", "wrestling", "kickboxing", "combat sports", "fight",
        "ufc news", "championship", "knockout", "grappling",
        "jiu jitsu", "muay thai", "octagon", "fighter training", "mixed martial arts", "sports"
    ],

    "Boxing": [
        "boxing", "boxer", "fight", "knockout", "heavyweight",
        "championship", "training", "fighter", "sports", "boxing news",
        "professional boxing", "boxing match", "boxing gym", "punch",
        "ring", "title fight", "boxing training", "mma", "combat sports", "boxing champion"
    ],

    "Fitness": [
        "fitness", "workout", "gym", "exercise", "training",
        "muscle", "strength", "cardio", "health", "bodybuilding",
        "fitness motivation", "weight loss", "fitness tips", "personal trainer",
        "gym workout", "exercise routine", "physical health", "athletic", "wellness", "sports"
    ],

    "Bodybuilding": [
        "bodybuilding", "muscles", "gym", "workout", "lifting",
        "protein", "strength", "fitness", "training", "physique",
        "muscle growth", "bodybuilder", "weightlifting", "hypertrophy",
        "gym motivation", "bodybuilding competition", "workout routine", "nutrition", "lean muscle", "fitness"
    ],

    "Running": [
        "running", "marathon", "jogging", "training", "cardio",
        "exercise", "fitness", "runners", "race", "health",
        "running shoes", "half marathon", "long distance", "sprint",
        "running training", "athletics", "5k", "10k", "running motivation", "sports"
    ],

    # =========================
    # FOOD & LIFESTYLE
    # =========================

    "Cooking": [
        "cooking", "recipes", "food", "kitchen", "chef",
        "baking", "dinner", "ingredients", "homemade", "meal",
        "cooking tips", "home cooking", "recipe ideas", "lunch",
        "breakfast", "cuisine", "cooking tutorial", "food preparation", "chef recipes", "delicious"
    ],

    "Baking": [
        "baking", "cake", "bread", "cookies", "dessert",
        "pastry", "flour", "oven", "recipes", "food",
        "chocolate", "cupcakes", "sourdough", "baking recipes",
        "cakes", "pie", "desserts", "baking tips", "homemade baking", "sweet"
    ],

    "Restaurants": [
        "restaurants", "food", "dining", "restaurant review", "cafe",
        "cuisine", "dinner", "lunch", "chef", "foodie",
        "restaurant recommendations", "fine dining", "fast food", "local food",
        "menu", "food review", "eating out", "brunch", "dining experience", "cooking"
    ],

    "Nutrition": [
        "nutrition", "food", "diet", "healthy eating", "vitamins",
        "protein", "calories", "meal", "health", "wellness",
        "macros", "micronutrients", "nutrition tips", "healthy food",
        "meal planning", "supplements", "carbohydrates", "fats", "nutrition science", "fitness"
    ],

    "Travel": [
        "travel", "vacation", "tourism", "trip", "holiday",
        "adventure", "hotel", "flight", "destination", "tourist",
        "travel tips", "backpacking", "travel guide", "tourist attractions",
        "beach", "mountains", "international travel", "road trip", "travel photography", "exploration"
    ],

    "Canada": [
        "canada", "toronto", "montreal", "vancouver", "ottawa",
        "canadian", "quebec", "news", "travel", "canadian life",
        "alberta", "ontario", "british columbia", "canadian politics",
        "canadian culture", "canadian cities", "weather", "immigration", "montreal life", "canadian news"
    ],

    "Quebec": [
        "quebec", "montreal", "quebec city", "french canada", "canadian",
        "quebec politics", "quebec culture", "francophone", "french", "canada",
        "sherbrooke", "laval", "longueuil", "quebec news",
        "montreal news", "quebec life", "winter", "education", "immigration", "province"
    ],

    "United States": [
        "usa", "america", "united states", "new york", "california",
        "politics", "american", "travel", "news", "culture",
        "texas", "florida", "los angeles", "washington",
        "american life", "us news", "american politics", "cities", "economy", "society"
    ],

    "Europe": [
        "europe", "european", "travel", "countries", "culture",
        "history", "tourism", "politics", "cities", "lifestyle",
        "european union", "eu", "europe news", "european culture",
        "travel europe", "european cities", "international", "languages", "economy", "society"
    ],

    "Fashion": [
        "fashion", "clothing", "style", "outfits", "designer",
        "streetwear", "trends", "beauty", "shopping", "lifestyle",
        "fashion trends", "fashion week", "clothes", "fashion design",
        "style inspiration", "mens fashion", "womens fashion", "luxury fashion", "brands", "outfit ideas"
    ],

    "Streetwear": [
        "streetwear", "sneakers", "fashion", "clothing", "style",
        "supreme", "nike", "outfits", "street fashion", "brands",
        "jordan", "adidas", "hoodies", "street style",
        "sneaker culture", "fashion brands", "urban fashion", "hypebeast", "clothing brands", "shoes"
    ],

    "Beauty": [
        "beauty", "makeup", "skincare", "cosmetics", "hair",
        "fashion", "style", "self care", "beauty tips", "lifestyle",
        "skin care", "hair care", "beauty products", "cosmetic",
        "makeup tutorial", "beauty routine", "nails", "fragrance", "wellness", "personal care"
    ],

    "Home Improvement": [
        "home", "renovation", "interior design", "furniture", "diy",
        "construction", "decor", "house", "repair", "improvement",
        "home renovation", "home projects", "tools", "remodeling",
        "painting", "flooring", "kitchen renovation", "bathroom renovation", "building", "house projects"
    ],

    "Interior Design": [
        "interior design", "home decor", "furniture", "architecture", "decor",
        "design", "house", "room", "style", "renovation",
        "living room", "bedroom", "minimalism", "modern design",
        "home inspiration", "interior decoration", "home styling", "apartment", "architecture", "interior"
    ],

    "DIY": [
        "diy", "do it yourself", "projects", "crafts", "home improvement",
        "building", "tools", "repair", "creative", "handmade",
        "woodworking", "crafting", "maker", "tutorial", "construction",
        "upcycling", "home projects", "creative projects", "hobby", "design"
    ],

    # =========================
    # FINANCE & BUSINESS
    # =========================

    "Personal Finance": [
        "finance", "money", "budget", "saving", "investing",
        "income", "expenses", "banking", "financial advice", "wealth",
        "personal finance", "debt", "credit", "financial planning",
        "money management", "savings", "financial freedom", "taxes", "bank", "economy"
    ],

    "Investing": [
        "investing", "stocks", "shares", "portfolio", "dividends",
        "etf", "markets", "trading", "wealth", "finance",
        "stock market", "long term investing", "index funds", "investor",
        "financial markets", "investment strategy", "passive income", "assets", "returns", "money"
    ],

    "Cryptocurrency": [
        "crypto", "bitcoin", "ethereum", "blockchain", "defi",
        "nft", "web3", "cryptocurrency", "trading", "finance",
        "altcoins", "crypto news", "digital currency", "wallet",
        "exchange", "ethereum", "decentralized finance", "token", "web3 technology", "bitcoin news"
    ],

    "Business": [
        "business", "company", "entrepreneur", "startup", "management",
        "leadership", "marketing", "strategy", "career", "finance",
        "business news", "corporation", "economy", "sales",
        "customers", "business ideas", "entrepreneurship", "organization", "industry", "success"
    ],

    "Startups": [
        "startup", "entrepreneur", "founder", "venture capital", "business",
        "innovation", "technology", "investment", "company", "funding",
        "startup founder", "venture capital", "seed funding", "business idea",
        "startup news", "entrepreneurship", "product", "growth", "investors", "technology startup"
    ],

    "Marketing": [
        "marketing", "advertising", "social media", "branding", "seo",
        "content marketing", "business", "customers", "sales", "digital marketing",
        "marketing strategy", "online marketing", "email marketing", "brand",
        "advertisements", "audience", "marketing campaign", "growth", "promotion", "business"
    ],

    "Career": [
        "career", "jobs", "work", "employment", "resume",
        "interview", "skills", "professional", "salary", "workplace",
        "job search", "career advice", "professional development", "office",
        "remote work", "career growth", "hiring", "employment opportunities", "work life", "profession"
    ],

    "Real Estate": [
        "real estate", "property", "houses", "apartments", "mortgage",
        "rent", "housing", "investment", "home", "property market",
        "real estate investing", "housing market", "realtor", "buying a house",
        "selling property", "rental property", "commercial real estate", "landlord", "tenant", "construction"
    ],

    "Economics": [
        "economics", "economy", "inflation", "interest rates", "gdp",
        "markets", "finance", "business", "money", "government",
        "economic news", "recession", "employment", "trade",
        "global economy", "central bank", "economic policy", "prices", "financial markets", "growth"
    ],

    # =========================
    # EDUCATION & SOCIETY
    # =========================

    "Education": [
        "education", "school", "college", "university", "students",
        "learning", "teachers", "study", "academic", "knowledge",
        "education system", "online learning", "exams", "homework",
        "classroom", "teaching", "degree", "scholarship", "research", "education news"
    ],

    "History": [
        "history", "ancient", "war", "civilization", "empire",
        "historical", "culture", "past", "archaeology", "events",
        "world history", "ancient history", "historical events", "museum",
        "historian", "revolution", "medieval", "ancient civilization", "history research", "heritage"
    ],

    "Politics": [
        "politics", "government", "elections", "president", "parliament",
        "policy", "politicians", "law", "democracy", "political news",
        "political debate", "election", "political party", "government policy",
        "international politics", "political science", "leadership", "voting", "democracy", "society"
    ],

    "World News": [
        "news", "world news", "breaking news", "international", "events",
        "politics", "government", "conflict", "current events", "journalism",
        "global news", "news update", "international news", "world events",
        "reporting", "media", "geopolitics", "crisis", "society", "current affairs"
    ],

    "Law": [
        "law", "legal", "court", "lawyer", "justice",
        "rights", "crime", "government", "regulations", "policy",
        "legal advice", "constitution", "lawsuit", "criminal law",
        "civil law", "legal system", "attorney", "court case", "legislation", "justice system"
    ],

    "Philosophy": [
        "philosophy", "ethics", "existence", "meaning", "knowledge",
        "logic", "society", "mind", "ideas", "thinkers",
        "metaphysics", "epistemology", "morality", "consciousness",
        "philosophical debate", "ancient philosophy", "existentialism", "reason", "truth", "thought"
    ],

    "Religion": [
        "religion", "faith", "spirituality", "belief", "philosophy",
        "christianity", "islam", "buddhism", "culture", "community",
        "judaism", "hinduism", "religious studies", "prayer",
        "religious history", "spiritual life", "beliefs", "religious culture", "theology", "faith"
    ],

    "Relationships": [
        "relationships", "dating", "love", "marriage", "couples",
        "advice", "romance", "breakup", "friendship", "social",
        "relationship advice", "dating advice", "communication", "partner",
        "love life", "emotions", "family", "trust", "couples advice", "personal life"
    ],

    "Self Improvement": [
        "self improvement", "motivation", "productivity", "habits", "goals",
        "discipline", "success", "personal growth", "mindset", "life advice",
        "confidence", "personal development", "motivation", "success habits",
        "self discipline", "better life", "growth mindset", "learning", "focus", "mental strength"
    ],

    "Productivity": [
        "productivity", "organization", "time management", "focus", "work",
        "habits", "planning", "efficiency", "goals", "study",
        "task management", "productivity tips", "routine", "calendar",
        "deep work", "focus techniques", "time management tips", "work habits", "planning", "organization"
    ],

    "Lifestyle": [
        "lifestyle", "life", "wellness", "fashion", "travel",
        "food", "hobbies", "culture", "daily life", "personal",
        "living", "routine", "lifestyle tips", "experiences",
        "self care", "home", "social life", "personal interests", "wellbeing", "life advice"
    ],

    # =========================
    # ART & CREATIVE
    # =========================

    "Photography": [
        "photography", "camera", "photos", "photographer", "portrait",
        "landscape", "editing", "lens", "photography tips", "visual",
        "street photography", "photo editing", "camera gear", "photography tutorial",
        "composition", "lighting", "portrait photography", "nature photography", "photoshoot", "creative"
    ],

    "Videography": [
        "videography", "video", "filmmaking", "camera", "editing",
        "cinema", "film", "production", "youtube", "content creation",
        "video production", "camera gear", "cinematography", "filmmaker",
        "video editing", "short film", "directing", "visual storytelling", "production", "creative"
    ],

    "Graphic Design": [
        "design", "graphic design", "photoshop", "illustrator", "branding",
        "logo", "typography", "art", "creative", "visual design",
        "adobe", "poster design", "ui design", "illustration",
        "branding design", "digital design", "creative work", "layout", "graphics", "designer"
    ],

    "Art": [
        "art", "drawing", "painting", "artist", "illustration",
        "digital art", "creative", "gallery", "design", "artwork",
        "fine art", "sketching", "visual art", "artistic",
        "traditional art", "creative process", "art community", "painting techniques", "drawing tutorial", "artist"
    ],

    "Digital Art": [
        "digital art", "illustration", "drawing", "artist", "photoshop",
        "procreate", "concept art", "design", "creative", "art",
        "digital painting", "character art", "artwork", "ipad art",
        "drawing tablet", "digital illustration", "concept artist", "creative process", "visual art", "artist"
    ],

    "Writing": [
        "writing", "authors", "stories", "novels", "poetry",
        "creative writing", "books", "fiction", "writers", "literature",
        "writing tips", "short stories", "storytelling", "screenwriting",
        "writing community", "novelist", "writer", "creative work", "fiction writing", "characters"
    ],

    "Books": [
        "books", "reading", "literature", "novels", "authors",
        "fiction", "nonfiction", "book review", "writing", "library",
        "book recommendations", "reading list", "classic literature", "fantasy books",
        "science fiction books", "book club", "new books", "author", "readers", "literary"
    ],

    "Comics": [
        "comics", "manga", "graphic novels", "superheroes", "marvel",
        "dc", "illustration", "characters", "books", "art",
        "comic books", "comic art", "superhero comics", "indie comics",
        "comic creator", "graphic novel", "illustration", "fiction", "storytelling", "characters"
    ],

    # =========================
    # INTERNET & ENTERTAINMENT
    # =========================

    "Memes": [
        "memes", "funny", "humor", "internet", "viral",
        "jokes", "comedy", "reaction", "social media", "trending",
        "meme culture", "internet memes", "funny memes", "shitposting",
        "online humor", "viral memes", "reaction memes", "meme page", "laughing", "internet culture"
    ],

    "Internet Culture": [
        "internet culture", "memes", "viral", "social media", "online",
        "trends", "communities", "influencers", "digital", "humor",
        "online culture", "internet trends", "viral content", "forums",
        "online communities", "social trends", "digital culture", "web culture", "memes", "internet"
    ],

    "Social Media": [
        "social media", "instagram", "youtube", "tiktok", "twitter",
        "facebook", "content", "influencers", "online", "viral",
        "social networks", "creator", "followers", "posts",
        "social media marketing", "online community", "digital creator", "trending", "social platforms", "internet"
    ],

    "YouTube": [
        "youtube", "videos", "creator", "content creator", "streaming",
        "vlogging", "subscribers", "entertainment", "video", "channel",
        "youtube channel", "youtube creator", "youtube shorts", "video creator",
        "content", "youtube news", "online video", "creator economy", "influencer", "digital media"
    ],

    "Streaming": [
        "streaming", "twitch", "youtube", "livestream", "content creator",
        "gaming", "video", "broadcast", "entertainment", "online",
        "live streaming", "streamer", "streaming platform", "twitch streamer",
        "streaming community", "broadcasting", "content", "live video", "creator", "internet"
    ],

    "Podcasts": [
        "podcast", "audio", "episodes", "interview", "conversation",
        "spotify", "news", "entertainment", "talk", "radio",
        "podcast show", "podcast host", "podcasting", "audio content",
        "podcast episode", "discussion", "media", "microphone", "storytelling", "streaming"
    ],

    # =========================
    # CARS & TRANSPORT
    # =========================

    "Cars": [
        "cars", "automotive", "vehicles", "driving", "car news",
        "engine", "automobile", "cars review", "motor", "transportation",
        "car culture", "car enthusiast", "new cars", "car modifications",
        "sports cars", "luxury cars", "car maintenance", "automotive news", "vehicle", "driving"
    ],

    "Electric Vehicles": [
        "electric cars", "ev", "tesla", "electric vehicle", "battery",
        "charging", "automotive", "sustainability", "cars", "technology",
        "electric car", "ev news", "electric mobility", "charging station",
        "battery technology", "tesla news", "green transportation", "vehicles", "automotive technology", "clean energy"
    ],

    "Motorcycles": [
        "motorcycle", "motorbike", "bikes", "riding", "biker",
        "engine", "motorsport", "helmet", "transportation", "motorcycle news",
        "motorcycle riding", "motorcycle culture", "sport bike", "cruiser",
        "motorcycle gear", "rider", "bike trip", "motorcycle maintenance", "motorcycle racing", "vehicles"
    ],

    # =========================
    # NATURE & ANIMALS
    # =========================

    "Nature": [
        "nature", "environment", "wildlife", "forests", "animals",
        "outdoors", "earth", "landscape", "conservation", "ecology",
        "natural world", "mountains", "rivers", "ocean",
        "nature photography", "plants", "wilderness", "hiking", "environment", "planet"
    ],

    "Animals": [
        "animals", "pets", "wildlife", "dogs", "cats",
        "nature", "cute animals", "zoo", "biology", "animal news",
        "animal behavior", "mammals", "birds", "reptiles",
        "animal photography", "wild animals", "species", "veterinary", "animal lovers", "nature"
    ],

    "Dogs": [
        "dogs", "puppy", "pets", "puppies", "dog training",
        "animals", "dog breeds", "pets", "cute", "canine",
        "dog lover", "dog videos", "dog care", "pet care",
        "dog behavior", "rescue dogs", "dog walking", "puppy training", "animals", "best friend"
    ],

    "Cats": [
        "cats", "kittens", "pets", "animals", "cat videos",
        "cute", "kitten", "cat breeds", "feline", "funny cats",
        "cat lover", "cat care", "pet cats", "cat behavior",
        "rescue cats", "cat memes", "cute cats", "pet care", "animals", "kittens"
    ],

    # =========================
    # PERSONAL & GENERAL
    # =========================

    "Hobbies": [
        "hobbies", "crafts", "collecting", "gaming", "reading",
        "music", "photography", "sports", "creative", "leisure",
        "free time", "interests", "activities", "collections",
        "fun", "personal hobbies", "creative hobbies", "outdoors", "entertainment", "lifestyle"
    ],

    "Pets": [
        "pets", "dogs", "cats", "animals", "pet care",
        "puppies", "kittens", "veterinary", "pet food", "animal lovers",
        "pet health", "pet training", "adoption", "rescue",
        "pet products", "cute animals", "domestic animals", "animal care", "pets", "companions"
    ],

    "Parenting": [
        "parenting", "children", "kids", "family", "babies",
        "parent advice", "motherhood", "fatherhood", "education", "child development",
        "parenting tips", "family life", "new parents", "childcare",
        "school", "toddlers", "teenagers", "parenting advice", "children", "family"
    ],

    "Mental Wellness": [
        "mental health", "wellness", "self care", "stress", "anxiety",
        "mindfulness", "meditation", "therapy", "mental wellbeing", "health",
        "emotional health", "relaxation", "mind", "wellbeing",
        "self improvement", "personal growth", "sleep", "emotions", "calm", "lifestyle"
    ],

    "Meditation": [
        "meditation", "mindfulness", "relaxation", "stress", "mental health",
        "wellness", "breathing", "mind", "peace", "self care",
        "guided meditation", "mindful living", "calm", "focus",
        "mental wellbeing", "spirituality", "relaxation techniques", "meditation practice", "health", "wellness"
    ],

    "Sleep": [
        "sleep", "sleeping", "insomnia", "rest", "health",
        "wellness", "bedtime", "dreams", "sleep schedule", "relaxation",
        "sleep health", "sleep tips", "fatigue", "tired",
        "circadian rhythm", "bedroom", "night routine", "mental health", "recovery", "wellbeing"
    ],

    "Architecture": [
        "architecture", "buildings", "design", "construction", "cities",
        "architect", "urban design", "houses", "engineering", "art",
        "modern architecture", "historic buildings", "urban planning", "skyscrapers",
        "interior design", "architecture photography", "architecture design", "buildings", "city design", "construction"
    ],

    "Military": [
        "military", "army", "navy", "air force", "defense",
        "war", "weapons", "soldiers", "history", "geopolitics",
        "military news", "armed forces", "military technology", "defense industry",
        "military history", "strategy", "national security", "military equipment", "warfare", "soldiers"
    ],

    "Geopolitics": [
        "geopolitics", "politics", "international relations", "countries", "government",
        "war", "conflict", "diplomacy", "world news", "foreign policy",
        "international politics", "global affairs", "nations", "security",
        "economy", "international relations", "geopolitical news", "power", "military", "world"
    ],

    "Urbanism": [
        "urbanism", "cities", "urban planning", "architecture", "transportation",
        "public transit", "infrastructure", "housing", "city life", "development",
        "urban design", "smart cities", "streets", "public spaces",
        "architecture", "city planning", "walkability", "urban development", "neighborhoods", "cities"
    ],

    "Science Fiction": [
        "science fiction", "sci fi", "future", "space", "aliens",
        "robots", "technology", "fiction", "dystopia", "time travel",
        "cyberpunk", "space opera", "artificial intelligence", "future technology",
        "science fiction books", "science fiction movies", "fantasy", "speculative fiction", "futuristic", "science"
    ],

    "Personal Development": [
        "personal development", "goals", "motivation", "success", "mindset",
        "habits", "confidence", "discipline", "growth", "life",
        "self improvement", "personal growth", "success mindset", "learning",
        "productivity", "motivation", "life advice", "self discipline", "better habits", "achievement"
    ],

    "Technology News": [
        "tech news", "technology", "gadgets", "software", "ai",
        "apple", "google", "microsoft", "innovation", "internet",
        "technology news", "tech industry", "new technology", "startup",
        "hardware", "cybersecurity", "software news", "science", "digital", "computing"
    ],
}



class Command(BaseCommand):
    help = "Seeds the database with categories and keywords"

    def handle(self, *args, **kwargs):

        for category_name, keyword_names in categories.items():

            category, created = Category.objects.get_or_create(
                name=category_name.lower()
            )

            for keyword_name in keyword_names:
                KeyWord.objects.get_or_create(
                    word=keyword_name.lower(),
                    category = category
                )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created category: {category_name}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Categories and keywords successfully seeded!"
            )
        )

