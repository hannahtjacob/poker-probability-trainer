# PokerSense

PokerSense is a full-stack Texas Hold'em probability trainer for exploring hand
equity, pot odds, and decision-making under uncertainty. It uses Monte Carlo
simulation to estimate outcomes, presents the results in a React dashboard,
stores analysis history in PostgreSQL, and can generate optional educational
explanations with a local Ollama model.

The project is designed as a learning and software-engineering tool. Simulation
results are estimates, not guarantees, and the application is not intended to
encourage gambling.

## Features

- Validate and normalize standard card notation such as `As`, `Kh`, `Td`, and
  `2c`
- Simulate Texas Hold'em outcomes against one to eight opponents
- Report win, tie, loss, and equity percentages
- Produce deterministic simulations when a random seed is supplied
- Compare estimated equity with the break-even equity implied by pot odds
- Generate beginner-friendly rule-based recommendations
- Visualize outcome probabilities with Plotly
- Save and review recent analyses in PostgreSQL
- Request optional explanations from a locally running Ollama model
- Run backend tests and frontend builds in GitHub Actions

## Tech Stack

**Backend**

- Python 3.11
- FastAPI and Uvicorn
- SQLAlchemy 2
- PostgreSQL 16 and `psycopg2`
- Treys poker hand evaluator
- Pydantic 2
- Pytest
- Ollama Python client

**Frontend**

- React 19
- TypeScript
- Vite
- Axios
- Plotly and `react-plotly.js`

**Infrastructure**

- Docker and Docker Compose
- GitHub Actions

## Architecture

```text
React + Vite frontend
        |
        | HTTP / JSON
        v
FastAPI application
  |-- simulation routes
  |-- pot-odds and recommendation logic
  |-- history routes
  |-- optional Ollama explanation route
        |
        v
PostgreSQL
```

The backend separates HTTP routing from poker-domain logic:

- `backend/app/` contains FastAPI routes, schemas, database configuration,
  SQLAlchemy models, and CRUD operations.
- `backend/poker/` contains card validation, Treys evaluation, Monte Carlo
  simulation, pot-odds calculations, recommendations, and AI explanations.
- `frontend/src/` contains the React dashboard, API client, reusable components,
  and shared TypeScript response types.

Database tables are registered and created when the FastAPI application starts.

## Monte Carlo Simulation

For each requested simulation, PokerSense:

1. Validates the hero cards and known community cards.
2. Removes those cards from a standard 52-card deck.
3. Shuffles the remaining deck with an optional deterministic seed.
4. Deals two cards to every opponent.
5. Completes the community board to five cards.
6. Evaluates the hero and opponent hands with Treys.
7. Records a win, tie, or loss based on the best opponent score.

Treys uses lower scores for stronger hands. PokerSense calculates:

```text
equity = win_probability + (tie_probability / 2)
```

Pot-odds analysis calculates the minimum equity required for a call to break
even:

```text
required_equity = call_amount / (pot_size + call_amount) * 100
```

These values are educational estimates based on sampled outcomes and simplified
opponent assumptions.

## Install Without Docker

### Prerequisites

- Python 3.11
- Node.js 20
- PostgreSQL
- Optional: Ollama

### 1. Create the database

Start PostgreSQL and create a database named `pokersense`:

```sql
CREATE DATABASE pokersense;
```

The default local connection is:

```text
postgresql://postgres:postgres@localhost:5432/pokersense
```

Set `DATABASE_URL` if your PostgreSQL credentials or host differ.

### 2. Start the backend

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/pokersense"
uvicorn app.main:app --reload
```

The API will be available at:

- API: `http://127.0.0.1:8000`
- Swagger documentation: `http://127.0.0.1:8000/docs`

### 3. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

The frontend defaults to `http://127.0.0.1:8000/api`. To use another backend:

```bash
export VITE_API_BASE_URL="http://127.0.0.1:8000/api"
npm run dev
```

## Install With Docker Compose

From the repository root:

```bash
docker compose up --build
```

This starts:

- PostgreSQL on `localhost:5432`
- FastAPI on `localhost:8000`
- Vite on `localhost:5173`

PostgreSQL data is stored in the named `postgres_data` volume.

Stop the services with:

```bash
docker compose down
```

To remove the database volume as well:

```bash
docker compose down -v
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | API status and documentation URL |
| `POST` | `/api/simulate` | Run an equity simulation |
| `POST` | `/api/analyze` | Simulate, calculate optional pot odds, recommend, and optionally save |
| `GET` | `/api/history?limit=20` | Return recent saved simulations |
| `POST` | `/api/explain` | Explain a generic analysis object with Ollama or a fallback |

Example analysis request:

```json
{
  "hero_cards": ["As", "Kh"],
  "community_cards": ["Qd", "Jc", "2h"],
  "num_opponents": 2,
  "simulations": 10000,
  "seed": 42,
  "pot_size": 100,
  "call_amount": 20,
  "save_result": true
}
```

## Frontend Usage

1. Enter the two hero cards.
2. Add zero to five comma-separated community cards.
3. Select the number of opponents and simulation count.
4. Optionally enter the pot size and call amount.
5. Submit the form to view probabilities, equity, and recommendations.
6. Review saved analyses in the recent simulations table.

Card notation uses an uppercase rank and lowercase suit:

- Ranks: `2 3 4 5 6 7 8 9 T J Q K A`
- Suits: `s h d c`

## Optional Ollama Setup

Install Ollama from [ollama.com](https://ollama.com/) and pull the default model:

```bash
ollama pull llama3.2
ollama serve
```

The `/api/explain` endpoint uses `llama3.2` by default and calls the local Ollama
service. If the package, service, or model is unavailable, the backend returns
`success: false` with a rule-based educational fallback instead of crashing.

Ollama is not included as a Docker Compose service. When running the backend in
Docker, additional host networking or a dedicated Ollama container is required
for the container to reach a host Ollama instance.

## Running Tests

Backend:

```bash
cd backend
python -m pytest
```

Frontend type-check and production build:

```bash
cd frontend
npm run build
```

The GitHub Actions workflow runs both checks on pushes and pull requests.
