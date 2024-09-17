db = db.getSiblingDB('conviniencer');

db.books.createIndex({'user_id': 1, 'name': 1}, {unique: true});
db.links.createIndex({'user_id': 1, 'name': 1}, {unique: true});
db.photos.createIndex({'user_id': 1, 'name': 1}, {unique: true});
db.archives.createIndex({'user_id': 1, 'name': 1}, {unique: true});
