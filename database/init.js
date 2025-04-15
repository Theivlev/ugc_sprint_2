
try {
    conn = new Mongo();
    db = conn.getDB("ugc_movies");
} catch (error) {
    print(`Ошибка подключения к базе данных: ${error}`);
    throw error;
}


function createCollectionWithValidation(collectionName, validator) {
    try {
        if (!db.getCollectionNames().includes(collectionName)) {
            db.createCollection(collectionName, { validator });
            print(`Коллекция ${collectionName} успешно создана`);
        } else {
            print(`Коллекция ${collectionName} уже существует`);
        }
    } catch (error) {
        print(`Ошибка при создании коллекции ${collectionName}: ${error}`);
        throw error;
    }
}


function createUniqueIndex(collection, indexSpec, options) {
    try {
        collection.createIndex(indexSpec, options);
        print(`Уникальный индекс для ${collection.getName()} успешно создан`);
    } catch (error) {
        print(`Ошибка при создании индекса для ${collection.getName()}: ${error}`);
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

