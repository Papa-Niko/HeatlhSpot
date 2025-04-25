# HealthSpot API

A FastAPI backend service for the HealthSpot application, providing user management and healthcare-related functionality.

## Project Overview

HealthSpot API is a RESTful backend service built with FastAPI and MongoDB. It provides endpoints for managing user data and healthcare information, with secure database connections and proper error handling. The API is designed to be deployed to cloud platforms like Render, Railway, or Heroku.

### Tech Stack

- **FastAPI**: Modern, high-performance web framework for building APIs
- **MongoDB Atlas**: Cloud database service for storing application data
- **Motor**: Asynchronous Python driver for MongoDB
- **Uvicorn**: ASGI server for running the FastAPI application
- **Python 3.7+**: Programming language

## Installation Instructions

### Prerequisites

- Python 3.7 or higher
- MongoDB Atlas account (or local MongoDB installation)
- Git

### Local Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd HealthSpot
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```
   MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/mydb?retryWrites=true&w=majority
   ALLOWED_ORIGINS=https://youfrontend.netlify.app
   ```

5. Run the application locally:
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at http://localhost:8000

## Deployment Steps

### Deploying to Render

1. **Create a Git repository** (if not already using one):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Sign up for Render** at https://render.com/

3. **Create a new Web Service**:
   - Connect your Git repository
   - Select the branch to deploy
   - Specify the build command: `pip install -r requirements.txt`
   - Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Configure environment variables**:
   - Add `MONGODB_URI` with your MongoDB connection string
   - Add `ALLOWED_ORIGINS` with comma-separated frontend URLs

5. **Deploy the application**:
   - Render will automatically build and deploy your application
   - You'll receive a URL to access your API

### Deploying to Heroku

1. **Install the Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**:
   ```bash
   heroku create healthspot-api
   ```

3. **Configure environment variables**:
   ```bash
   heroku config:set MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/mydb?retryWrites=true&w=majority
   heroku config:set ALLOWED_ORIGINS=https://youfrontend.netlify.app
   ```

4. **Deploy the application**:
   ```bash
   git push heroku main
   ```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb+srv://username:password@cluster.mongodb.net/mydb?retryWrites=true&w=majority` |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed frontend origins | `https://myapp.netlify.app,https://myapp-staging.netlify.app` |
| `PORT` | Port on which the application runs (set by hosting provider) | `8000` |

## API Documentation

After starting the application, visit `/docs` (e.g., http://localhost:8000/docs) for interactive Swagger documentation of all API endpoints.

### Endpoints

#### Health Check
```
GET /
```
Returns the API status.

#### User Management

```
POST /add-user
```
Creates a new user.

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30
}
```

**Response**:
```json
{
  "inserted_id": "507f1f77bcf86cd799439011"
}
```

```
GET /get-users
```
Retrieves all users.

**Response**:
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }
]
```

```
DELETE /delete-user/{user_id}
```
Deletes a user by ID.

**Response**:
```json
{
  "deleted_count": 1
}
```

## Error Handling

The API includes comprehensive error handling:
- 400: Bad Request (e.g., invalid user ID format)
- 404: Not Found (e.g., user not found)
- 500: Internal Server Error (with detailed logging)

## License

[MIT License](LICENSE)

