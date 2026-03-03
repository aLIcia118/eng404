# ENG404 – Progress and Goals

## Project Overview

This semester project is an API server for a geographic database.

The backend supports CRUD operations on geographic data, uses MongoDB for
persistent storage, and is deployed using CI/CD. The remainder of the
semester focuses on frontend integration, performance, testing, and security.

---

## Part 1: Progress So Far

### Backend API and Database

- Implemented an API server for geographic data.
- Added CRUD operations backed by MongoDB.
- Supported both local and cloud MongoDB connections.

**Related assignments**
- Use MongoDB locally  
- Connect to MongoDB in the cloud  
- Run your API server in the cloud  

---

### CI/CD and Deployment

- Configured GitHub Actions to automatically run tests.
- Ensured builds fail when tests fail.
- Used scripts to support deployment.

**Related assignments**
- GitHub Actions Working  

---

### Testing and Code Structure

- Added unit tests for core backend logic.
- Organized the project into modular components.
- Used Python decorators to manage database access.

**Related assignments**
- Use Python decorators  
- Fancier testing  

---

## Goals

### Load Script (DONE!)

**Goal**
- Add a script that generates load against the API.

**How**
- Create a script that repeatedly sends requests to API endpoints
  and observes system behavior under load.

---

### Create React Frontend to Your API Server (DONE!)

**Goal**
- Build a React frontend that connects to the backend API.

**How**
- Create a basic React application.
- Fetch data from backend endpoints and display results.

---

### Create at Least One Developer Endpoint (DONE!)

**Goal**
- Add an endpoint intended for developers.

**How**
- Create an endpoint for system status, metadata, or debugging.

---

### Design Frontend 

**Goal**
- Make the frontend clean, readable, and easy to use for testing the API.

**How**
- Use consistent layout and spacing (cards/sections for each endpoint).
- Render API outputs clearly with formatted JSON and previews for large responses.
- Add clear buttons, labels, and loading/error states.

---

### Use Environment Variables to Re-direct Frontend 

**Goal**
- Configure the frontend to switch between local and cloud APIs.

**How**
- Store API URLs in environment variables.
- Use different values for development and production.

---

### Implement React Testing 

**Goal**
- Add automated tests for the React frontend.

**How**
- Write basic component and integration tests.
- Ensure tests can run automatically.

### Security

**Goal**
- Improve overall system security.

**How**
- Review input validation and error handling.
- Ensure sensitive configuration is not exposed.

---

### Add API Documentation

**Goal**
- Document all API endpoints and data formats.

**How**
- Create a simple API specification in the README or docs/ folder.
- List all endpoints with:
  - HTTP method and path  
  - Required parameters  
  - Example request / response JSON  
  - Error response formats (400, 404, 500)  
- Keep this documentation updated as the API evolves.

---

## Summary

The backend portion of the project is complete and functional.
The remaining work focuses on frontend development, testing,
performance, and security to fully satisfy the semester requirements.
