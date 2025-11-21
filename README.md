# Backend API
A robust RESTful API built with FastAPI that provides a complete backend solution for a social media application with posts, comments, and likes functionality. Features include JWT-based authentication, PostgreSQL database integration, and comprehensive CRUD operations.

## Features

- **User Authentication & Authorization**: JWT token-based authentication with secure password hashing
- **Posts Management**: Create, read, update, and delete posts with search functionality
- **Comments System**: Add and manage comments on posts
- **Likes/Reactions**: Like posts and comments
- **User Profiles**: User registration and profile management
- **Database Migrations**: Alembic for database version control
- **Security**: Password hashing with bcrypt, OAuth2 implementation
- **Search Functionality**: Search posts by title and content

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens) with python-jose
- **Password Hashing**: Bcrypt via passlib
- **Migrations**: Alembic
- **Validation**: Pydantic schemas
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone github.com/dhruvkshah75/Backend_API
   cd Backend_API
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory with the following variables:
   ```env
   # Database Configuration
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # JWT Configuration
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /login` - User login, returns JWT access token

### Users
- `POST /users` - Create a new user account
- `GET /users/{id}` - Get user details by ID

### Posts
- `GET /posts` - Get all posts (with pagination and search)
- `POST /posts` - Create a new post (requires authentication)
- `GET /posts/{id}` - Get a specific post by ID
- `PUT /posts/{id}` - Update a post (owner only)
- `DELETE /posts/{id}` - Delete a post (owner only)

### Comments
- `GET /comments` - Get comments for posts
- `POST /comments` - Add a comment to a post (requires authentication)
- `PUT /comments/{id}` - Update a comment (owner only)
- `DELETE /comments/{id}` - Delete a comment (owner only)

### Likes
- `POST /likes/posts/{id}` - Like/unlike a post
- `POST /likes/comments/{id}` - Like/unlike a comment

## Project Structure

```
API-Development/               <-- Root Directory
├── alembic/                   <-- Database migration files
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── README
├── app/                       <-- Main application source code
│   ├── routers/               <-- Route handlers
│   │   ├── __init__.py
│   │   ├── auth.py            <-- Login/Authentication routes
│   │   ├── post.py            <-- Post CRUD routes
│   │   ├── user.py            <-- User creation/retrieval routes
│   │   ├── comment.py         <-- Comment management routes
│   │   └── likes.py           <-- Likes/reactions routes
│   ├── __init__.py
│   ├── config.py              <-- Environment variable settings
│   ├── database.py            <-- Database connection logic
│   ├── main.py                <-- App entry point
│   ├── models.py              <-- SQLAlchemy database models
│   ├── oauth2.py              <-- JWT token creation & verification
│   ├── schemas.py             <-- Pydantic models (Request/Response schemas)
│   └── utils.py               <-- Password hashing utilities
├── .env                       <-- Environment variables (not in git)
├── .gitignore                 <-- Files to ignore in git
├── alembic.ini                <-- Alembic configuration
├── dockerfile                 <-- Docker image instructions
└── README.md                  <-- This file
```

## Database Models

### User
- `id` (Primary Key)
- `email` (Unique)
- `username_id` (Unique)
- `password` (Hashed)
- `created_at`

### Post
- `id` (Primary Key)
- `title`
- `content`
- `published`
- `created_at`
- `owner_id` (Foreign Key → User)

### Comment
- `id` (Primary Key)
- `content`
- `created_at`
- `owner_id` (Foreign Key → User)
- `post_id` (Foreign Key → Post)

### Likes_posts
- Composite Primary Key: (`user_id`, `post_id`)

### Like_comments
- Composite Primary Key: (`user_id`, `comment_id`)

## Security Features

- **Password Hashing**: All passwords are hashed using bcrypt before storage
- **JWT Authentication**: Secure token-based authentication
- **Authorization**: Route-level protection ensuring users can only modify their own content
- **Input Validation**: Pydantic schemas validate all incoming data

## Testing

Run tests using pytest:
```bash
pytest
```

## Docker Support

Build and run with Docker:
```bash
docker build -t backend-api .
docker run -p 8000:8000 backend-api
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Dhruv Shah

## Acknowledgments

- FastAPI documentation and community
- SQLAlchemy documentation
- PostgreSQL documentation