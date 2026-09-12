# Krishisetu

Agricultural marketplace and equipment rental platform for Indian farmers.

## Tech Stack

- **Frontend**: React + Tailwind CSS (Vite)
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL (Supabase)
- **Auth**: JWT + bcrypt

---

## Setup Instructions

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd Krishisetu
```

### 2. Backend Setup

#### Create a virtual environment

```bash
cd backend
python -m venv venv
```

#### Activate it

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

#### Install dependencies

```bash
pip install -r requirements.txt
```

#### Set up environment variables

```bash
copy .env.example .env
```

Open `.env` and fill in your values:

- **DATABASE_URL**: Get this from your Supabase project → Settings → Database → Connection string (URI). Use the **direct connection** (port 5432), not the pooled one (port 6543).
- **JWT_SECRET**: Any random string. Use something strong like `openssl rand -hex 32` to generate one.

#### Set up the database

1. Go to your [Supabase Dashboard](https://supabase.com/dashboard)
2. Open your project → SQL Editor
3. Paste the contents of `init_db.sql` and run it
4. This creates the `users` table

#### Seed the admin account

```bash
python seed_admin.py
```

This creates an admin account:
- Email: `admin@krishisetu.com`
- Password: `admin123`
- **Change this password after first login!**

#### Run the backend

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API docs (Swagger): `http://localhost:8000/docs`

---

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
```

#### Run the frontend

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

---

## How It Works

```
React (Vite)  →  FastAPI REST API  →  PostgreSQL (Supabase)
   :5173              :8000               Supabase cloud
```

1. The React frontend sends HTTP requests to the FastAPI backend
2. FastAPI validates requests using Pydantic schemas
3. The backend connects to Supabase PostgreSQL using asyncpg
4. Authentication uses JWT tokens:
   - On login, the backend verifies the password (bcrypt) and returns a JWT
   - The frontend stores the JWT in localStorage
   - Every subsequent request includes the JWT in the Authorization header
   - Protected endpoints verify the JWT and check user roles

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | No | Register a new user |
| POST | `/auth/login` | No | Login and get JWT token |
| GET | `/users/me` | Yes | Get current user profile |
| GET | `/admin/users` | Admin | List all registered users |

---

## Project Structure

```
Krishisetu/
├── backend/
│   ├── app/
│   │   ├── auth/           # Password hashing + JWT
│   │   ├── dependencies/   # FastAPI auth dependencies
│   │   ├── models/         # Database schema reference
│   │   ├── routers/        # API route handlers
│   │   ├── schemas/        # Pydantic request/response models
│   │   ├── config.py       # Environment variable loading
│   │   ├── database.py     # PostgreSQL connection pool
│   │   └── main.py         # FastAPI app entry point
│   ├── .env.example
│   ├── init_db.sql
│   ├── requirements.txt
│   └── seed_admin.py
├── frontend/
│   ├── src/
│   │   ├── components/     # Navbar, ProtectedRoute
│   │   ├── context/        # AuthContext (React Context)
│   │   ├── pages/          # Login, Register, Dashboard, Admin, 404
│   │   ├── services/       # Axios API client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
└── README.md
```

---

## Current Milestone (40%)

What's been built:

- [x] User registration with validation
- [x] User login with JWT authentication
- [x] Password hashing (bcrypt)
- [x] User roles (farmer, vendor, admin)
- [x] Protected API routes
- [x] Role-based access control
- [x] Admin panel with user management table
- [x] React frontend with routing
- [x] Frontend ↔ Backend ↔ Database communication
- [x] Environment-based configuration

## What's Next

Upcoming features for future milestones:

1. **Marketplace module** — Products, categories, cart, orders, vendor dashboard
2. **Equipment rental module** — Equipment listings, FCFS booking queue, 24-hour confirmation window
3. **Payment integration** — Razorpay
4. **Enhanced admin** — Product approvals, order management, dispute handling
5. **User profile management** — Edit profile, change password
