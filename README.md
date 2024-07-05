# Flask RESTful API

This is a web application developed with Flask that provides a RESTful API for managing users, posts, messages, and images. The application also includes JWT authentication and CORS support.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your_username/your_repository.git
    cd your_repository
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Make sure to configure the following variables in your configuration file:

```python
app.config['JWT_SECRET_KEY'] = 'GRUWIN-ADMIN-ACCOUNT'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
```

## Usage

Run the application:

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000/`.

## Endpoints

### Authentication

- `POST /signup`: Register new users.
- `POST /login`: Log in existing users.

### Users

- `GET /users`: Get all users (Requires JWT authentication).
- `POST /users`: Add a new user.
- `GET /user/<string:id>`: Get a user by ID (Requires JWT authentication).

### Posts

- `GET /post`: Get all posts (Requires JWT authentication).
- `POST /post`: Create a new post.

### Image Posts

- `GET /imagepost/<int:postid>`: Get an image post by post ID (Requires JWT authentication).
- `POST /imagepost`: Create a new image post.

### Messages

- `GET /messages/<string:sender_id>/<string:recipient_id>`: Get messages between two users (Requires JWT authentication).
- `POST /messages`: Create a new message (Requires JWT authentication).
- `PUT /messages/<string:id>`: Update a message by ID (Requires JWT authentication).
- `DELETE /messages/<string:id>`: Delete a message by ID (Requires JWT authentication).

### Emails

- `POST /email`: Send an email (Requires JWT authentication).

### Protected Routes

- `GET /protected`: Protected route that returns a welcome message with the current user's ID (Requires JWT authentication).

## Error Handling

- `404 Not Found`: Returned when the requested URL is not found on the server.

## Dependencies

- Flask
- Flask-RESTful
- Flask-JWT-Extended
- Flask-CORS
- smtplib
- email.mime
