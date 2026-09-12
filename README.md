<<<<<<< HEAD
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
=======
# KrishiSetu 

*Agri-input marketplace + equipment rental platform for Indian farmers*
---

## 1. Final Problem Definition

Small and marginal farmers in India face two separate, well-documented frictions:

1. **Input access** — buying seeds, fertilizer, and pesticides through local dealers, with no easy way to compare prices, brands, or availability across sellers.
2. **Equipment access** — owning machinery like tractors or tillers is uneconomical for most small farms because usage is highly seasonal (intense demand at sowing/harvesting, idle otherwise). Renting is common but informal — arranged by phone call, with no standardized booking, pricing, or fairness when multiple farmers want the same machine in the same week.

Krishisetu solves both with one platform: an **input marketplace** (farmers buy from vendors) and an **equipment rental module** where equipment can come from individual farmers renting out idle machinery (C2C) *or* a dealer/fleet account (B2C) — with a fair, automated **FCFS queue + 24-hour confirmation window** replacing the informal "whoever calls first" system.

This is a scoped **student build**, not a commercial launch — pan-India in concept, generic rather than hyperlocal, deployed live for demonstration and evaluation.

## 2. Target Users & Roles

| Role | Description |
|---|---|
| **Farmer** | Primary user. Buys inputs from vendors. Can also list their own equipment for rent (C2C) and/or book equipment from others. |
| **Vendor** | Sells agricultural inputs (seeds, fertilizer, pesticides) through the marketplace. |
| **Equipment Owner** | Lists equipment for rent — either an individual farmer (same account type as Farmer, dual capability) or a dealer/fleet operator with multiple machines. |
| **Admin** | Platform operator (your team, for demo purposes) — approves listings, resolves disputes, monitors bookings/orders. |

## 3. Final Requirements

**Functional — Marketplace (inputs)**
- Vendor registration and product listing (name, category, price, stock, images, description)
- Farmer browsing, search, filter by category/price
- Cart, checkout, Razorpay payment
- Order history and status (placed → confirmed → shipped → delivered) — kept simple; no real logistics integration
- Vendor dashboard to manage listings and view orders

**Functional — Equipment Rental**
- Equipment listing (owner/dealer side): type, specs, rate (per day/hour), location, availability calendar
- Farmer search/filter by equipment type, location, date range
- Booking request → if the slot is contested, request enters an FCFS queue
- 24-hour confirmation window on the top of the queue; Spring `@Scheduled` job auto-expires unconfirmed bookings and promotes the next farmer in queue
- Booking status tracking: queued → confirmed → active → completed / expired / cancelled
- Owner dashboard: approve/reject, view booking calendar

**User requirements**
- Simple, low-friction registration and browsing (assume low digital literacy — keep flows short, use clear labels, avoid jargon)

**Technical requirements**
- backend, React frontend,database, deployed live

## 4. Proposed Solution

**Core solution:** One platform, two modules, one shared user identity — an input marketplace and an FCFS-queued equipment rental system, deployed live as a working demo.

## 5. MVP & Advanced Features

| Feature | Priority | Why |
|---|---|---|
| Auth (register/login, farmer & vendor roles) | 🔴 Critical |  |
| Input product listing & browsing | 🔴 Critical | Core marketplace loop |
| Cart & Razorpay checkout | 🔴 Critical | Core marketplace loop |
| Equipment listing (owner side) | 🔴 Critical | Core rental loop |
| Equipment booking + FCFS queue + 24hr expiry job | 🔴 Critical | standout technical feature |
| Order/booking history & status | 🟡 Important | Expected UX, not hard to build |
| Search/filter (category, equipment type, location) | 🟡 Important | Usability, moderate effort |
| Admin panel (approve listings, view all orders/bookings) | 🟡 Important | Useful for demo and dispute-handling story |
| Ratings/reviews (vendors, equipment owners) | 🟢 Optional | Nice-to-have |
| Email/SMS notifications on booking events | 🟢 Optional | Adds polish |
| Multi-language UI | 🟢 Optional (future) | Real-world relevant |

## 6. User / System Workflow

**Marketplace flow:** Farmer registers → browses/searches products → adds to cart → checks out → order recorded → vendor sees order in dashboard → order status updated manually by vendor (placed/shipped/delivered).

**Rental flow:** Owner registers/lists equipment → farmer searches by type/date → farmer sends booking request → system checks slot:
- If free → booking auto-confirmed
- If contested → request joins FCFS queue → the farmer at the head of the queue gets a 24-hour confirmation window → confirms in time → booking locked in; doesn't confirm in time → `@Scheduled` job expires it and promotes the next farmer in queue automatically

**Admin flow:** Views all users, listings, orders, and bookings; can suspend a listing or user if needed for the demo.


## 7. Tech Stack

| Layer | Choice | |
|---|---|---|
| Backend | FastAPI[PYTHON] | keeps DB code approachable once basics are learned |
| Frontend | React | large beginner-friendly ecosystem and tutorials |
| Database | PostgreSQL | free-tier hosting widely available (Supabase) |
| Auth | FastAPI tools & JWT | Standard, well-documented pattern for beginners |
| Payments | Razorpay (test mode) | Already decided; has a sandbox that doesn't require real settlement |
| Deployment (backend) | Supabase | Simplest path to "deployed" |
| Deployment (frontend) | Vercel | Near-zero-config React deployment |
| Deployment (DB) | Managed PostgreSQL | Avoids self-hosting a database |


## 8. Database Design (core entities)

- **User** — id, name, phone/email, password_hash, role flags (is_vendor, is_equipment_owner), location
- **Product** — id, vendor_id (FK→User), name, category, price, stock, description, image_url
- **Order** — id, farmer_id (FK→User), status, total_amount, razorpay_payment_id, created_at
- **OrderItem** — id, order_id (FK), product_id (FK), quantity, price_at_purchase
- **Equipment** — id, owner_id (FK→User), type, description, rate, rate_unit (hour/day), location
- **AvailabilitySlot** — id, equipment_id (FK), start_date, end_date, is_booked
- **BookingRequest** — id, equipment_id (FK), farmer_id (FK), requested_slot, status (queued/confirmed/expired/completed/cancelled), queue_position, confirmation_deadline

Relationships: one Vendor→many Products; one Farmer→many Orders→many OrderItems→one Product; one Owner→many Equipment→many AvailabilitySlots; one Equipment→many BookingRequests (queued), one active confirmed booking at a time.

## 9. API Requirements (representative, not exhaustive)

- `POST /auth/register`, `POST /auth/login`
- `GET /products`, `GET /products/{id}`, `POST /products` (vendor), `PUT /products/{id}`
- `POST /orders`, `GET /orders/my`, Razorpay webhook/callback endpoint for payment confirmation
- `GET /equipment`, `POST /equipment` (owner), `GET /equipment/{id}/availability`
- `POST /bookings`, `GET /bookings/my`, `POST /bookings/{id}/confirm`
- `GET /admin/...` — protected admin-only endpoints

## 10. Security

- JWT-based session auth; role-based route protection (farmer/vendor/admin)
- Razorpay secret key kept server-side only, in environment variables — n
- Input validation on all forms (server-side, not just client-side)
- HTTPS enforced on deployed URLs (default on Render/Vercel)

## 11. Development Phases 


| Weeks | Focus |
|---|---|
| 1–2 | Learn basics: React fundamentals for members; set up Git repo, project skeleton, DB schema |
| 3–4 | Auth (register/login) end-to-end; basic product listing + browsing (marketplace skeleton) |
| 5–6 | Cart + Razorpay checkout; equipment listing + plain booking (no queue yet — get the simple path working first) |
| 7 | FCFS queue logic + `@Scheduled` expiry job |
| 8 | Admin panel, order/booking history views, UI polish |
| 9 | Deployment (backend, frontend, DB), end-to-end testing, bug fixing |
| 10 | Buffer week — testing, report writing, demo rehearsal |


## 12. Testing

- Manual end-to-end testing of both flows (marketplace purchase, rental booking with queue contention) before deployment
- Specifically test the expiry job with a short artificial timeout (e.g., 1–2 minutes instead of 24 hours) during development so you can actually observe the queue-promotion behavior without waiting a day
- Basic input validation testing (empty fields, invalid prices, past dates for bookings)
- Test Razorpay in sandbox/test mode only

## 13. Deployment

- Backend → FastAPI[PYTHON]
- Frontend → Vercel (React build deploy)
- Database → managed PostgreSQL instance on the same platform as backend, to avoid cross-network latency/config issues
- Environment variables (DB credentials, Razorpay keys, JWT secret)

## 14. Final Project Summary

Krishisetu is a two-module agritech platform: an input marketplace where farmers buy seeds/fertilizer/pesticides from vendors, and an equipment rental system where farmers or dealers list machinery and other farmers book it through a fairness-driven FCFS queue with automatic 24-hour-expiry handling. Built with React, FastAPI and PostgreSQL, deployed live. — the project's strength lies in a clean, correctly-implemented core workflow and a genuinely well-engineered scheduled-job queue mechanic.

---
>>>>>>> e57baee815c51c99522bbf1d59ec0f653d9efa1d
