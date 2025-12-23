# bencyn-social-media-api

# Social Media API (Django + DRF)

A backend Social Media API built with **Django** and **Django REST Framework (DRF)**.
It supports **user registration & authentication (JWT)**, **post management**, **following/unfollowing users**, and **viewing follower statistics**.

This project simulates core features of a real-world social media platform.

---

## Features

* User registration & authentication (JWT)
* User profiles (bio, profile picture)
* Create, update, delete posts (CRUD)
* Follow & unfollow users
* View followers and following counts
* Secure endpoints using JWT authentication
* Django Admin support for managing users

---

## Tech Stack

* Python 3.x
* Django
* Django REST Framework
* Simple JWT (`djangorestframework-simplejwt`)
* PostgreSQL 

---

## Project Structure

```
bencyn_social_connect/
│
├── bencyn_social_connect/   # Main project settings
││   ├── settings.py
││   ├── urls.py
││   └── wsgi.py
│
├── users/                   # User & profile management
├── posts/                   # Posts CRUD
├── follows/                 # Follow system
│
├── manage.py
└── requirements.txt
```

---

## Setup Instructions

### Clone the repository

```bash
git clone <repository-url>
cd bencyn_social_connect
```

### Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### Run the development server

```bash
python manage.py runserver
```

Access admin panel:

```
http://127.0.0.1:8000/admin/
```

---

## Authentication (JWT)

This API uses **JWT authentication** via `djangorestframework-simplejwt`.

### Obtain Token

```
POST /api/auth/token/
```

**Request Body**:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response**:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### Refresh Token

```
POST /api/auth/token/refresh/
```

---

## User Endpoints

### Register New User

```
POST /api/users/register/
```

**Request Body**:

```json
{
  "username": "your_username",
  "email": "your_email",
  "password": "your_password"
}
```

---

## Post Endpoints

### Create Post

```
POST /api/posts/
```

**Headers**:

```
Authorization: Bearer <access_token>
```

**Request Body**:

```json
{
  "content": "Hello world!",
  "media": "https://example.com/image.jpg"
}
```

---

### Get All Posts

```
GET /api/posts/
```

---

### Update Post

```
PUT /api/posts/<post_id>/
```

(Only the post owner can update)

---

### Delete Post

```
DELETE /api/posts/<post_id>/
```

(Only the post owner can delete)

---

## Follow System

### Follow a User

```
POST /api/follows/follow/<user_id>/
```

**Headers**:

```
Authorization: Bearer <access_token>
```

---

### Unfollow a User

```
DELETE /api/follows/unfollow/<user_id>/
```

---

### View Follower / Following Count (Any User)

```
GET /api/follows/users/<user_id>/stats/
```

**Response**:

```json
{
  "id": 3,
  "username": "john",
  "followers_count": 5,
  "following_count": 2
}
```

---

### View Your Own Follow Stats

```
GET /api/follows/users/me/stats/
```

**Headers**:

```
Authorization: Bearer <access_token>
```

---

## Permissions & Rules

* Only authenticated users can:

  * Create, update, or delete posts
  * Follow or unfollow users
  * View their personal feed or stats
* Users cannot:

  * Edit or delete another user’s posts
  * Follow themselves

---

## Testing

You can test endpoints using:

* Postman
* curl
* HTTPie

Example:

```bash
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/api/posts/
```

---

## Deployment Notes

For production:

* Use **Gunicorn**
* Enable HTTPS
* Set:

  ```python
  DEBUG = False
  SECURE_SSL_REDIRECT = True
  ```

---

## Future Improvements

* Feed endpoint (posts from followed users)
* Comments & likes
* User search
* Notifications
* Pagination & caching

---

## Author

Built as part of a **Social Media API project using Django & DRF**.

