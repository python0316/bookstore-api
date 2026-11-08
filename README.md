# Bookstore - Login & Authentication API

Bookstore loyihasi uchun foydalanuvchilarni autentifikatsiya qilish, JWT token berish va joriy foydalanuvchi ma'lumotlarini olish (Current User) backend API tizimi.

Loyiha Django va Django REST Framework asosida qurilgan bo'lib, JWT autentifikatsiyasi uchun `djangorestframework-simplejwt` kutubxonasidan foydalanilgan.

---

## O'rnatish va ishga tushirish

### 1. Virtual muhitni yaratish va faollashtirish

```bash
python -m venv .venv
```

Windows uchun:
```bash
.venv\Scripts\activate
```

Linux / macOS uchun:
```bash
source .venv/bin/activate
```

### 2. Kerakli paketlarni o'rnatish

```bash
pip install -r requirements.txt
```

### 3. Ma'lumotlar bazasini sozlash va migratsiya

Loyiha sukut bo'yicha PostgreSQL'dan foydalanadi (kerak bo'lsa `.env` orqali o'zgartirish yoki `USE_SQLITE=True` qilib SQLite'da ham ishlatish mumkin):

```bash
python manage.py migrate
```

### 4. Test foydalanuvchisini yaratish

Vazifada so'ralgan standart test foydalanuvchisini (`testuser` / `test12345`) bir buyruq bilan avtomatik yaratish:

```bash
python manage.py setup_test_data
```

*(Yoki mustaqil ravishda `python manage.py createsuperuser` orqali ham yangi foydalanuvchi yaratishingiz mumkin)*

### 5. Serverni ishga tushirish

```bash
python manage.py runserver
```

Server odatda `http://127.0.0.1:8000/` manzilida ishga tushadi.

---

## API Endpointlar

| Metod | Endpoint | Tavsif | Ruxsat |
|---|---|---|---|
| POST | `/api/auth/login/` | Foydalanuvchi tizimga kirishi va JWT tokenlar olish | Har kimga ochiq |
| GET | `/api/auth/me/` | Joriy tizimga kirgan foydalanuvchi ma'lumotlari | Faqat token bilan (Bearer) |
| POST | `/api/auth/register/` | Yangi foydalanuvchini ro'yxatdan o'tkazish | Har kimga ochiq |
| POST | `/api/auth/token/refresh/` | Access tokenni yangilash | Har kimga ochiq |

---

## API Sinov Natijalari (curl misollari)

Quyida barcha talab qilingan 6 ta holat bo'yicha amalda tekshirilgan curl buyruqlari va qaytgan javoblar keltirilgan.

### 1. To'g'ri login va password (200 OK)

So'rov:
```bash
curl -i -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "test12345"}'
```

Javob:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Login successful",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

---

### 2. Noto'g'ri password kiritilganda (400 Bad Request)

So'rov:
```bash
curl -i -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "wrongpassword"}'
```

Javob:
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "detail": ["Incorrect password."],
  "error": ["Incorrect password."]
}
```

---

### 3. Mavjud bo'lmagan username kiritilganda (400 Bad Request)

So'rov:
```bash
curl -i -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "mavjudemas", "password": "test12345"}'
```

Javob:
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "detail": ["User with this username does not exist."],
  "error": ["User with this username does not exist."]
}
```

---

### 4. Bo'sh login ma'lumotlari yuborilganda (400 Bad Request)

So'rov:
```bash
curl -i -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "", "password": ""}'
```

Javob:
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "username": ["Username cannot be blank."],
  "password": ["Password cannot be blank."]
}
```

---

### 5. Login qilmasdan /api/auth/me/ ga murojaat (401 Unauthorized)

So'rov:
```bash
curl -i -X GET http://127.0.0.1:8000/api/auth/me/
```

Javob:
```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "detail": "Authentication credentials were not provided."
}
```

---

### 6. To'g'ri token bilan /api/auth/me/ ga murojaat (200 OK)

So'rov:
```bash
curl -i -X GET http://127.0.0.1:8000/api/auth/me/ \
  -H "Authorization: Bearer <access_token>"
```

Javob:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com"
}
```

---

## Avtomatik testlarni ishga tushirish

Barcha holatlar uchun yozilgan testlarni quyidagi buyruq orqali tekshirish mumkin:

```bash
python manage.py test
```

Natija:
```
Creating test database for alias 'default'...
........
----------------------------------------------------------------------
Ran 8 tests in 6.694s

OK
Destroying test database for alias 'default'...
```

---

## Loyihada yaratilgan asosiy fayllar

- `config/settings.py` — DRF va SimpleJWT sozlamalari, PostgreSQL va SQLite qo'llab-quvvatlashi.
- `config/urls.py` — Bosh yo'naltirishlar (`/api/auth/` va `/api/books/`).
- `accounts/serializers.py` — `LoginSerializer`, `UserSerializer` va validatsiyalar.
- `accounts/views.py` — `LoginView`, `CurrentUserView` (IsAuthenticated) va `RegisterView`.
- `accounts/urls.py` — Autentifikatsiya endpointlari.
- `accounts/tests.py` — Barcha 6+ ta test holatlarini qamrab olgan avtotestlar.
- `accounts/management/commands/setup_test_data.py` — Test foydalanuvchisini avtomatik yaratish buyrug'i.
- `books/` — Bookstore domeni uchun kitoblar modeli va API'si.
- `requirements.txt` — Loyihaga kerakli barcha kutubxonalar ro'yxati.
