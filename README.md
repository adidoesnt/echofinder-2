# EchoFinder 2

## Overview

[EchoFinder 2](https://github.com/adidoesnt/echofinder-2) is the second iteration of the EchoFinder project. It combines the functionality of 2 projects that I previously built:

- [EchoFinder](https://github.com/adidoesnt/echofinder) - A Telegram bot that uses RAG to find messages in a conversation that relate to a given query.
- [TeleDr](https://github.com/adidoesnt/teledr) - A Telegram bot that uses RAG to summarise conversations.

## Tech Stack

- **Python**: I used the [pyTelegramBotAPI](https://github.com/eternnoai/pyTelegramBotAPI) library to interact with the Telegram API.
- **Telegram**: The bot is hosted on Telegram's servers.
- **OpenAI**: I used the [OpenAI](https://openai.com/) API to generate embeddings and summaries.
- **ChromaDB**: I used [ChromaDB](https://www.chromadb.dev/) to store the embeddings and the metadata for the messages.
- **GitHub Actions**: I used [GitHub Actions](https://github.com/features/actions) to deploy the bot and ChromaDB.
- **Docker**: I used [Docker](https://www.docker.com/) to containerise the bot and ChromaDB.
- **Heroku**: I used [Heroku](https://www.heroku.com/) to host containerised versions of the bot and ChromaDB.

## Using the Bot

1. Visit the [EchoFinder 2 Bot](https://t.me/echofinder_bot) on Telegram.
2. Either add the bot to a group chat or start a private chat with it.
3. Use the `/start` command to get started.

## Commands

- `/start` - Start the bot.
- `/help` - Get help.
- `/examples` - Get examples of how to use the bot.
- `/search <query>` - Search for messages in a conversation.
    - The query can be omitted, in which case the bot will prompt you for a query.
- `/tldr <n>` - Summarise the last `n` messages in a conversation.
    - The number of messages to summarise can be omitted, in which case the bot will prompt you for a number.

## Local Development

1. Clone the repository:

```bash
git clone https://github.com/adidoesnt/echofinder-2.git
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

```bash
source .venv/bin/activate
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

5. Open up `docker-compose.yml` and comment out the `bot` service.

```bash
# docker-compose.yml

services:
  chromadb:
    # Important: Don't change the image version, 0.5.4 has a bug with creating collections
    image: chromadb/chroma:0.5.3
    ports:
      - 8000:8000
    env_file:
      - .env
    volumes:
      - chroma_data:/data
    networks:
      - echofinder_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 10s
      timeout: 5s
      retries: 5

#   bot:
#     build:
#       context: .
#       dockerfile: Dockerfile
#     env_file:
#       - .env
#     depends_on:
#       chromadb:
#         condition: service_healthy
#     networks:
#       - echofinder_network

volumes:
  chroma_data:

networks:
  echofinder_network:
    driver: bridge
```

5. Spin up ChromaDB using Docker Compose:

```bash
docker compose up -d
```

6. Run the bot:

```bash
python -m src.echofinder.main
```

7. Interact with the bot on Telegram.
