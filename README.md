# Memory-Place
# Secure Geometric Password API

## Overview
This project implements a secure password management system based on geometric patterns. Users can create passwords using predefined geometric patterns, which are then securely stored and retrieved via an API.

## Features
- **Pattern-based password generation**: Users create passwords based on geometric patterns (square, triangle, line).
- **Secure storage**: Passwords are stored securely using hashed encryption (bcrypt/PBKDF2).
- **JWT Authentication**: Token-based authentication to secure API access.
- **SQLite Database**: Persistent storage for users and passwords.
- **Mobile & Browser Support**: Can be extended for mobile visualization and browser extensions.
- **Zero-Knowledge Authentication**: Validates user identity without revealing their full password.

## How It Works
1. **User Registration**:
   - A user registers with a username, email, and a selected base pattern.
   - The system validates the pattern before saving the user data in SQLite.
2. **Password Generation**:
   - A password is generated based on the user's pattern, service name, and the current month.
   - The password follows the format: `base_pattern-ServiceInitial@MonthInitial`.
3. **Secure Storage**:
   - The generated password is hashed and stored in the database.
   - bcrypt ensures passwords cannot be reversed.
4. **Authentication**:
   - Users receive a JWT token upon login.
   - This token is required for secure API requests.
5. **Mobile & Browser Support**:
   - A mobile app can visualize and animate the password pattern.
   - A browser extension can detect websites and auto-fill passwords.

## API Endpoints

### User Management
- `POST /users/` → Create a new user
- `POST /login/` → Authenticate user & get JWT token

### Password Management
- `POST /generate_password/` → Generate and store a password for a service
- `GET /patterns/` → Retrieve predefined patterns

## Technologies Used
- **FastAPI** - Web framework for the API
- **SQLite** - Lightweight database for storage
- **bcrypt** - Secure password hashing
- **JWT** - Secure user authentication
- **Uvicorn** - ASGI server for running the API

## Setup Instructions
1. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn pydantic sqlite3 bcrypt jwt
   ```
2. **Initialize Database**:
   ```bash
   python -c "from main import init_db; init_db()"
   ```
3. **Run the API**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Future Enhancements
- **Blockchain Integration**: Decentralized password storage.
- **Multi-Factor Authentication (MFA)**: Extra security layer.
- **Biometric Authentication**: Face/Fingerprint recognition.
- **Decentralized Identity Support**: Use of DID for authentication.

## Contributing
Contributions are welcome! Fork the repository and submit a pull request with improvements.

## License
MIT License - Free to use and modify.

