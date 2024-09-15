db = db.getSiblingDB('conviniencer');

db.books.createIndex({'name': 1}, {unique: true});
db.links.createIndex({'name': 1}, {unique: true});
db.photos.createIndex({'name': 1}, {unique: true});
