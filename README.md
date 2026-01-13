# 🛒 Online Shop API

A RESTful Online Shop API built with **Django Rest Framework**.  
Users can register, verify email, manage profiles, browse products, add items to cart, place orders, and leave comments.

---

## 📌 Tech Stack

- Backend: Python, Django, Django Rest Framework  
- Authentication: JWT (SimpleJWT)  
- Database: SQLite3  
- Media: Django MEDIA_URL (local storage)  
- Admin Panel: Django Admin  
- API Docs: Swagger & Redoc  

---

## 🚀 Project Setup

### Clone Repository
```bash
git clone <your-github-repo-url>
cd shop-api
```

### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Server
```bash
python manage.py runserver
```

---

## 📚 API Documentation

- Swagger: http://127.0.0.1:8000/swagger/
- Redoc: http://127.0.0.1:8000/redoc/

---

## 🔐 Authentication

### Register
POST /api/auth/register/

```json
{
  "email": "user@gmail.com"
}
```

### Verify Email
POST /api/auth/verify-email/

```json
{
  "email": "user@gmail.com",
  "code": "123456"
}
```

### Create Profile
PATCH /api/auth/profile-create/

```json
{
  "email": "user@gmail.com",
  "full_name": "John Doe",
  "username": "john_doe",
  "password": "StrongPass123"
}
```

### Login (Email or Username)
POST /api/auth/login/

```json
{
  "email": "john_doe",
  "password": "StrongPass123"
}
```

---

## 🛍 Products

- GET /api/products/
- GET /api/products/{id}/
- POST /api/products/ (admin)
- PATCH /api/products/{id}/ (admin)
- DELETE /api/products/{id}/ (admin)
- GET /api/products/search/?q=phone

---

## 💬 Comments

- GET /api/products/{id}/comments/
- POST /api/products/{id}/comments/
- PATCH /api/comments/{id}/
- DELETE /api/comments/{id}/
- GET /api/products/comments/

---

## 🛒 Cart

- GET /api/cart/
- POST /api/cart/add/
- PATCH /api/cart/update/
- POST /api/cart/remove/
- POST /api/cart/clear/

---

## 📦 Orders

- POST /api/order/create/
- GET /api/orders/
- GET /api/orders/{id}/
- DELETE /api/orders/{id}/cancel/
- PATCH /api/orders/{id}/status/ (admin)

---

## 👨‍💻 Author
Johnibek Abdurakhmanov
