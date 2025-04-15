
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

function createCollectionWithValidation(collectionName, validator) {
    try {
        if (!db.getCollectionInfos({ name: collectionName }).length) {
            db.createCollection(collectionName, { validator });
            log("INFO", `Коллекция '${collectionName}' успешно создана`);
        } else {
            log("WARN", `Коллекция '${collectionName}' уже существует`);
        }
    } catch (error) {
        log("ERROR", `Ошибка при создании коллекции '${collectionName}': ${error}`);
        throw error;
    }
}


function createUniqueIndex(collection, indexSpec, options) {
    try {
        collection.createIndex(indexSpec, options);
        log("INFO", `Уникальный индекс для коллекции '${collection.getName()}' успешно создан`);
    } catch (error) {
        log("ERROR", `Ошибка при создании индекса для коллекции '${collection.getName()}': ${error}`);
        throw error;
    }
}


createCollectionWithValidation("user_likes", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["movie_id", "user_id", "liked_at"],
            properties: {
                movie_id: {
                    bsonType: "objectId",
                    description: "ID фильма (должен быть ObjectId)"
                },
                user_id: {
                    bsonType: "objectId",
                    description: "ID пользователя (должен быть ObjectId)"
                },
                liked_at: {
                    bsonType: "date",
                    description: "Дата лайка"
                }
            }
        }
    }
});


createCollectionWithValidation("user_bookmarks", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["movie_id", "user_id", "bookmarked_at"],
            properties: {
                movie_id: {
                    bsonType: "objectId",
                    description: "ID фильма (должен быть ObjectId)"
                },
                user_id: {
                    bsonType: "objectId",
                    description: "ID пользователя (должен быть ObjectId)"
                },
                bookmarked_at: {
                    bsonType: "date",
                    description: "Дата добавления в закладки"
                }
            }
        }
    }
});


createCollectionWithValidation("user_reviews", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["movie_id", "user_id", "review_text", "rating", "reviewed_at"],
            properties: {
                movie_id: {
                    bsonType: "objectId",
                    description: "ID фильма (должен быть ObjectId)"
                },
                user_id: {
                    bsonType: "objectId",
                    description: "ID пользователя (должен быть ObjectId)"
                },
                review_text: {
                    bsonType: "string",
                    description: "Текст отзыва"
                },
                rating: {
                    bsonType: "int",
                    minimum: 1,
                    maximum: 10,
                    description: "Оценка фильма (1-10)"
                },
                reviewed_at: {
                    bsonType: "date",
                    description: "Дата написания отзыва"
                }
            }
        }
    }
});


createUniqueIndex(db.user_likes, { movie_id: 1, user_id: 1 }, { unique: true });
createUniqueIndex(db.user_bookmarks, { movie_id: 1, user_id: 1 }, { unique: true });
createUniqueIndex(db.user_reviews, { movie_id: 1, user_id: 1 }, { unique: true });
