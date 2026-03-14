# Scalable REST API & Frontend

This repository contains a Scalable REST API built with Node.js, Express, and MongoDB, alongside a React (Vite) frontend.

## Features
- **Backend**: User authentication (JWT + bcrypt), Role-based access, CRUD APIs.
- **Frontend**: Basic UI for registering, logging in, and dashboard interaction.
- **Security**: Validations and password hashing.

## Project Structure
- `/backend`: Node.js Express server
- `/frontend`: React application

## Scalability Note
The backend is designed using the MVC (Model-View-Controller) pattern, meaning each module (like auth, tasks) is separated for easy maintainability. To scale this further:
1. **Containerization**: Use Docker to containerize both frontend and backend for scalable deployments.
2. **Caching**: Implement a Redis caching layer for frequently accessed routes to decrease database load.
3. **Load Balancing**: Deploy multiple instances of the backend application behind a Load Balancer (like NGINX or AWS ALB) to handle larger traffic.
4. **Microservices (Future Strategy)**: The current monolith can be logically divided by splitting authentication, tasks/entities, and notifications into separate loosely coupled services.

## Setup and Running

### 1. Backend (Python FastAPI)
1. Navigate to the `backend` folder: `cd backend`
2. Activate the virtual environment: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `python -m uvicorn main:app --port 8000 --reload`
   - The API will be available at `http://localhost:8000`
git
### 2. Frontend (React Vite)
1. Navigate to the `frontend` folder: `cd frontend`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`
   - The UI will be available at `http://localhost:5173`

