# connorbot
A Discord bot I have been working on in my free time on and off.

## Prerequisites
This bot only runs on Docker, so the only prerequisite is a computer that has [Docker](https://docs.docker.com/engine/install/) and, optionally, [Docker Compose](https://docs.docker.com/compose/install/).

## Installation
You can pull the image using the following command:

`$ docker pull connorswislow/connorbot:latest`

Here's the link to the Docker repository: [connorswislow/connorbot](https://hub.docker.com/r/connorswislow/connorbot)

## Running

Connor Bot has a few environmental variables that need to be set:
- BOT_TOKEN=token
- PREFIX=|
- ASCII_ART=true
- ECRYPTION=true
- IDENTITY=true
- THE_LIST=true

By default, these will all be false, so in the command, you must set each one.

### Docker
It'll look something like this:

`$ docker run -d -e BOT_TOKEN=token -e PREFIX=| -e THE_LIST=true connorswislow/connorbot:latest`

### Docker Compose

Make a file called `docker-compose.yml`

In that file, insert the following information:

```yml
version: 3.7
services:
    connorbot:
        image: connorswislow/connorbot
        environment:
            - BOT_TOKEN=token
            - PREFIX=|
            - ASCII_ART=true
            - ECRYPTION=true
            - IDENTITY=true
            - THE_LIST=true
```
Then, run the following command:

`$ docker-compose up -d`

