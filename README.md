# WebChat with Copilot Studio Agent

This project demonstrates how to connect a frontend built with WebChat to a Microsoft Copilot Studio Agent (formerly Power Virtual Agents) using a Python backend. The backend issues Direct Line tokens to the browser so that the chat UI can securely talk to the agent.

## Project Structure

```
backend/    # FastAPI service that issues Direct Line tokens
frontend/   # Static WebChat page
docker-compose.yml  # Optional Docker setup for local dev
```

## Setup and Run Instructions

1. **Clone the repo and install dependencies**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```

2. **Create a `.env` file** inside `backend/` based on `.env.example` and set your Direct Line secret.

3. **Run the backend**

   ```bash
   python backend/main.py
   ```

4. **Serve the frontend** (any static server will work). For quick testing you can use Python:

   ```bash
   cd frontend
   python -m http.server 8080
   ```

   Visit `http://localhost:8080` and you should see the WebChat interface. Ensure
   the `API_BASE_URL` constant in `frontend/index.html` matches the backend URL.

### Docker (optional)

If you have Docker installed you can run both services with one command:

```bash
docker compose up --build
```

The frontend will be available on `http://localhost:8080` and will connect to the backend on `http://localhost:3978`.

## Installation and Dependency Guide

- [Python 3.8+](https://www.python.org/)
- [`fastapi`](https://fastapi.tiangolo.com/) – web framework
- [`uvicorn`](https://www.uvicorn.org/) – ASGI server
- [`requests`](https://docs.python-requests.org/) – HTTP client to call Direct Line
- [`python-dotenv`](https://github.com/theskumar/python-dotenv) – load environment variables

Install them with `pip install -r backend/requirements.txt`.

## Environment Setup

Configuration is done via environment variables loaded from `backend/.env`:

| Variable | Description |
|----------|-------------|
| `DIRECT_LINE_SECRET` | Secret for the Direct Line channel of your Copilot Studio agent |
| `PORT` | Port for the FastAPI server (default `3978`) |
| `HOST` | Host interface to bind (default `0.0.0.0`) |

## Testing and Debugging

- Access `http://localhost:3978/api/token` to verify the backend returns a token.
- Open the browser console on `http://localhost:8080` to inspect WebChat activity.
- Use tools like [ngrok](https://ngrok.com/) if you need to expose the bot externally for testing.

## Deployment Hints

The backend is a small FastAPI application and can be deployed to any platform that supports Python, such as Azure App Service or Azure Container Apps. The frontend can be served from a static web host (e.g., Azure Static Web Apps).

## System Architecture

```mermaid
graph TD
    A[Browser with WebChat] -->|Requests token| B(FastAPI Token Service)
    B -->|Calls Direct Line generate token API| C[Direct Line]
    A -->|Uses token to start conversation| C
    C -->|Routes messages| D[Copilot Studio Agent]
```

## Managing Copilot Studio Agent Environments

Environments for Copilot Studio agents are created and managed in the **Power Platform Admin Center** (<https://admin.powerplatform.microsoft.com>). Each environment corresponds to an Azure resource group behind the scenes. Use the Admin Center to create new environments, assign security roles, and configure channels (e.g., Direct Line). You can view the associated resources in the Azure Portal by navigating to the resource group named after your Power Platform environment.

## Self‑Review

- **Modularity** – The backend is a simple FastAPI app with a single responsibility: issuing Direct Line tokens. Frontend code is kept minimal.
- **Environment Variables** – All secrets and configuration are read from `.env` using `python-dotenv`.
- **Docker** – Provided only as an optional convenience for running both services.
- **Idiomatic Code** – The code uses type hints with `pydantic` models and follows FastAPI conventions.

