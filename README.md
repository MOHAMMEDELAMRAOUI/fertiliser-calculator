## Running the Project with Docker

This project uses Docker Compose to orchestrate both the Python backend and the JavaScript frontend (Fertiliser app). Below are the specific instructions and requirements for running this project using Docker.

### Project-Specific Requirements

#### Backend (`./backend`)
- **Base Image:** `python:3.11-slim`
- **System Dependencies:**
  - `build-essential`, `libpq-dev` (for PostgreSQL/psycopg2)
  - `coinor-cbc`, `coinor-libcbc-dev` (for Pyomo solvers)
  - `libopenblas-dev`, `liblapack-dev` (for scientific computing)
- **Python Dependencies:** Installed via `requirements.txt` in a virtual environment (`.venv`).
- **Exposed Port:** `5000` (Flask default)
- **Environment Variables:** Loaded from `./backend/.env` (ensure this file exists and is configured).

#### Frontend (`./frontend/fertiliser`)
- **Node Version:** `22.13.1` (specified via `ARG NODE_VERSION`)
- **Build Tool:** Uses `npm ci` for deterministic installs and `npm run build` for production build.
- **Production Server:** `nginx:alpine`
- **Exposed Port:** `80`
- **Environment Variables:** If needed, configure `.env` in `./frontend/fertiliser` and uncomment in `docker-compose.yml`.

### Build and Run Instructions

1. **Ensure Required Files Exist:**
   - `./backend/.env` (required for backend environment variables)
   - `requirements.txt` in `./backend`
   - `package.json` and `package-lock.json` in `./frontend/fertiliser`

2. **Build and Start Services:**
   - From the project root, run:
     ```sh
     docker compose up --build
     ```
   - This will build both services and start them with the correct dependencies and environment variables.

3. **Accessing Services:**
   - **Backend (Flask):** http://localhost:5000
   - **Frontend (Fertiliser app):** http://localhost:80

### Special Configuration
- The backend uses a Python virtual environment (`.venv`) inside the container for isolation.
- System dependencies for scientific computing and optimization are pre-installed in the backend image.
- The frontend is built with a specific Node.js version (`22.13.1`) for compatibility.
- Both services run as non-root users for improved security.
- The Docker Compose network is named `appnet` (bridge driver).

### Ports Exposed
- **Backend:** `5000` (mapped to host `5000`)
- **Frontend:** `80` (mapped to host `80`)

---

*If you update environment variables or dependencies, ensure the relevant `.env` and lock files are kept up to date for reproducible builds.*
