# Backend_API


### Repo Structure
```
        API-Development/               <-- Root Directory
    ├── .github/
    │   └── workflows/
    │       └── build-deploy.yml  <-- CI/CD pipeline configuration
    ├── alembic/                  <-- Database migration files
    │   ├── versions/
    │   ├── env.py
    │   ├── script.py.mako
    │   └── README
    ├── app/                      <-- Main application source code
    │   ├── routers/              <-- Route handlers
    │   │   ├── __init__.py
    │   │   ├── auth.py           <-- Login/Authentication routes
    │   │   ├── post.py           <-- Post CRUD routes
    │   │   ├── user.py           <-- User creation/retrieval routes
    │   │   └── vote.py           <-- Voting routes
    │   ├── __init__.py
    │   ├── calculations.py       <-- Dummy file for testing tutorial
    │   ├── config.py             <-- Environment variable settings
    │   ├── database.py           <-- Database connection logic
    │   ├── main.py               <-- App entry point
    │   ├── models.py             <-- SQLAlchemy database models
    │   ├── oauth2.py             <-- JWT token creation & verification
    │   ├── schemas.py            <-- Pydantic models (Request/Response schemas)
    │   └── utils.py              <-- Password hashing utilities
    ├── tests/                    <-- Automated tests
    │   ├── __init__.py
    │   ├── conftest.py           <-- Pytest fixtures (client, session, etc.)
    │   ├── database.py           <-- Test database setup (kept for reference)
    │   ├── test_calculations.py  <-- Unit tests for calculations.py
    │   ├── test_posts.py         <-- Integration tests for posts
    │   ├── test_users.py         <-- Integration tests for users
    │   └── test_votes.py         <-- Integration tests for votes
    ├── .env                      <-- Environment variables (not pushed to git)
    ├── .gitignore                <-- Files to ignore in git
    ├── alembic.ini               <-- Alembic configuration
    ├── docker-compose-dev.yml    <-- Docker Compose for Development
    ├── docker-compose-prod.yml   <-- Docker Compose for Production
    ├── Dockerfile                <-- Instructions to build Docker image
    ├── Procfile                  <-- Startup command for Heroku
    └── requirements.txt          <-- Python dependencies
```