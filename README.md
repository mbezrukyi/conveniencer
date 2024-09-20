# ConveniencerBot
**conveniencer** is a Telegram Bot that helps to structure your files, documents, photos, etc.

## Setup
1. Clone the repository to your local machine.
2. Create and fill .bot file:
```
[bot]
token = ...

[mongo]
host = ... 
port = ...
username = ...
password = ...
```
3. Create and fill .env file:
```
MONGO_INITDB_ROOT_USERNAME=...
MONGO_INITDB_ROOT_PASSWORD=...
```
> **Info:** see more on [mongo](https://hub.docker.com/_/mongo/) image.

4. Compose the project with Docker: `docker compose -p app up -d`

## Usage
1. Open Telegram
2. Find the Bot (@ConveniencerBot)
3. Start the bot with `/start` command
