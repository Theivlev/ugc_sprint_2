function log(level, message) {
    const timestamp = new Date().toISOString();
    print(`[${timestamp}] [${level}] ${message}`);
}

try {
    conn = new Mongo();
    db = conn.getDB("ugc_movies");
    log("INFO", "Успешное подключение к базе данных 'ugc_movies'");
} catch (error) {
    log("ERROR", `Ошибка подключения к базе данных: ${error}`);
    throw error;
}

db.createCollection("user_likes");
db.createCollection("user_bookmarks");
db.createCollection("user_reviews");


createUniqueIndex(db.user_likes, { movie_id: 1, user_id: 1 }, { unique: true });
createUniqueIndex(db.user_bookmarks, { movie_id: 1, user_id: 1 }, { unique: true });
createUniqueIndex(db.user_reviews, { movie_id: 1, user_id: 1 }, { unique: true });
