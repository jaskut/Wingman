# OpenAI based VoiceAssistant

A VoiceAssistant capable of executing functions.

## Installation

First create a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

Install required packages.

```bash
pip install -r requirements.txt
```

Add the necessary data in a wingman/.env file, like listed in .env.example.

## Run Server

To run the server:

```bash
python -m wingman.server
```

## Run Client

To run the client:

```bash
python -m wingman.client
```