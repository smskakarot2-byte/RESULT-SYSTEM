# GCUF Result Portal

A full-stack web application for GCUF (Ghazi University) examination result management with role-based access, PDF award-sheet parsing, GPA calculation, analytics, and transcript generation.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Features](#features)
- [Authentication](#authentication)
- [Setup & Installation](#setup--installation)
- [Commands](#commands)
- [Database](#database)
- [Important Notes](#important-notes)

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ with pnpm package manager
- PostgreSQL database
- Environment variables: `DATABASE_URL`, `SESSION_SECRET`

### Development Commands

```bash
# Frontend (React + Vite)
pnpm --filter @workspace/gcuf-web run dev
# Runs on port from $PORT, preview at `/`

# Backend API (Express)
pnpm --filter @workspace/api-server run dev
# Runs on port 8080, proxied at `/api`

# Database Migration
pnpm --filter @workspace/db run migrate

# API Code Generation (OpenAPI → Zod + React Query)
pnpm --filter @workspace/api-spec run codegen

# Build entire workspace
pnpm run build

# Type checking
pnpm run typecheck
```

## 🛠 Tech Stack

### Frontend

- **React** 19.1.0 + **Vite** 7 for fast development
- **Tailwind CSS** v4 for styling
- **shadcn/ui** for component library
- **Recharts** for data visualization
- **TanStack Query** (React Query) for server state management
- **Wouter** for lightweight routing
- **Framer Motion** for animations

### Backend

- **Express** 4 web framework
- **Pino** for structured logging
- **Multer** for file uploads (PDF handling)
- **Zod** for schema validation
- **Drizzle ORM** for database management

### Authentication

- Custom email/password authentication
- Replit Auth integration available (`@workspace/replit-auth-server` / `@workspace/replit-auth-web`)
- Session-based with PostgreSQL storage

### Database

- **PostgreSQL** via Drizzle ORM
- Tables: departments, students, courses, results, system_users, sessions

### PDF Processing

- **pdf-parse** v1.1.1 with `pagerender` hook
- X/Y position-based column detection for award sheet parsing

### API Contract

- **OpenAPI** specification → Zod schemas + React Query hooks via **Orval**

## 📁 Project Structure

```
RESULT-SYSTEM/
├── artifacts/
│   ├── api-server/src/
│   │   ├── app.ts                    # Express setup & middleware
│   │   ├── routes/                   # API endpoints
│   │   │   ├── auth.ts               # Authentication
│   │   │   ├── departments.ts        # Department management
│   │   │   ├── courses.ts            # Course & PDF upload
│   │   │   ├── results.ts            # Result management
│   │   │   ├── analytics.ts          # Analytics & statistics
│   │   │   └── users.ts              # User management
│   │   └── lib/
│   │       ├── pdfParser.ts          # PDF parsing (x-position detection)
│   │       └── grading.ts            # GCUF grading scale & GPA logic
│   │
│   └── gcuf-web/src/
│       ├── pages/                    # Route pages
│       │   ├── dashboard.tsx         # Main dashboard
│       │   ├── courses.tsx
│       │   ├── course-detail.tsx
│       │   ├── students.tsx
│       │   ├── analytics.tsx
│       │   ├── toppers.tsx           # Leaderboard
│       │   ├── departments.tsx
│       │   └── users.tsx
│       ├── components/               # Reusable components
│       └── index.css                 # Color palette
│
├── lib/
│   ├── db/src/
│   │   └── schema/gcuf.ts            # Complete DB schema
│   │
│   ├── api-spec/                     # OpenAPI specification
│   ├── api-client-react/             # Generated API hooks
│   ├── api-zod/                      # Generated Zod schemas
│   └── integrations/
│
├── package.json                      # Workspace root
├── pnpm-workspace.yaml               # pnpm monorepo config
└── tsconfig.base.json                # Base TypeScript config
```

## 🏗 Architecture

### PDF Parsing Strategy

The system uses `pdf-parse` with the `pagerender` hook to extract text items with X/Y coordinates from GCUF award sheets. Column boundaries are hard-coded based on standard GCUF PDF format:

- **Name**: x ≈ 63
- **Father Name**: x ≈ 199
- **CNIC**: x ≈ 328
- Roll numbers: always 6 digits

> ⚠️ **Note**: Column x-boundaries may need adjustment for different GCUF PDF layouts.

### Grading & GPA Calculation

- **Fail Rule**: If `status='Fail'`, `gradePoint` is stored as `0.00` in the database (enforced in both parser and GPA computation)
- **Ranking**: Toppers are sorted by **average percentage** (not CGPA) for fairness across multi-credit courses
- Grading scale defined in `artifacts/api-server/src/lib/grading.ts`

### API Contract Pattern

The project uses a **contract-first API** approach:

1. **OpenAPI Spec** defines the contract (`@workspace/api-spec`)
2. **Orval** code generation produces:
   - Zod schemas for server validation
   - Typed React Query hooks for the client
3. This ensures type safety across the entire stack

### Role-Based Access Control

All API routes (except `/api/healthz`, `/api/analytics/sessions`, `/api/results/student`) require Replit Auth session cookie or custom auth session.

## ✨ Features

### For Administrators

- 📊 Dashboard with system statistics
- 🏢 Department CRUD operations
- 👥 User management (create/edit professors)
- 📈 Cross-department analytics and charts
- 🏆 Toppers leaderboard

### For Professors

- 📤 Upload GCUF award-sheet PDF (auto-parses 100+ students)
- 📋 Per-course result card display
- 🔍 Student lookup with CGPA gauge
- 📝 Text transcript download

### For Students

- 🔐 Public landing page (roll-number lookup)
- 📊 View personal results and GPA
- 🎓 Download transcript

## 🔐 Authentication

### Default Admin Account

- **Email**: `smskakarot@gmail.com`
- **Password**: `GCUF2025`
- ⚠️ Seeded on every server startup

### User Management

- Professors: email/password accounts created by admin via Users panel
- Public landing page for unauthenticated visitors
- Sessions stored in `sessions` table

### Authentication Endpoints

```
POST   /api/auth/login      # User login
POST   /api/auth/logout     # User logout
GET    /api/auth/user       # Get current user info
```

## 📦 Setup & Installation

### 1. Clone Repository

```bash
git clone https://github.com/smskakarot2-byte/RESULT-SYSTEM.git
cd RESULT-SYSTEM
```

### 2. Install Dependencies

```bash
pnpm install
```

### 3. Environment Variables

Create a `.env` file in the root or set these variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/gcuf_db
SESSION_SECRET=your-secret-key-here
PORT=3000
```

### 4. Database Setup

```bash
pnpm --filter @workspace/db run migrate
```

### 5. Start Development Servers

**Terminal 1 - Frontend:**
```bash
pnpm --filter @workspace/gcuf-web run dev
```

**Terminal 2 - Backend:**
```bash
pnpm --filter @workspace/api-server run dev
```

Access the app at `http://localhost:3000`

## 🎯 Commands

| Command | Description |
|---------|-------------|
| `pnpm build` | Build entire workspace with type checking |
| `pnpm run typecheck` | Run TypeScript type checking |
| `pnpm run typecheck:libs` | Type check library code only |
| `pnpm --filter @workspace/api-spec run codegen` | Regenerate API client from OpenAPI spec |
| `pnpm --filter @workspace/db run migrate` | Run database migrations |
| `pnpm --filter @workspace/gcuf-web run dev` | Start frontend dev server |
| `pnpm --filter @workspace/api-server run dev` | Start backend API server |

## 🗄 Database

### Schema Overview

**Tables:**

- `departments` - GCUF departments
- `students` - Student information
- `courses` - Courses offered
- `results` - Student course results
- `system_users` - Admin and professor accounts
- `sessions` - User session management

View complete schema: `lib/db/src/schema/gcuf.ts`

## ⚠️ Important Notes

### PDF Parsing

- `pdf-parse` is marked as **external** in `artifacts/api-server/build.mjs` — **do NOT bundle** it (loads test fixtures at require-time)
- The `pagerender` callback uses a `pageIndex` counter; page processing order matches PDF page order
- Column x-boundaries (`const X = {...}` in `pdfParser.ts`) may need adjustment for different GCUF PDF formats

### User Interface

- **Theme**: Deep Dark default with Light mode toggle
- **Font**: Arial, Helvetica, sans-serif throughout
- **App Type**: Web app only (no desktop app)
- **Role-based Sidebar**: Admin sees all 7 menu items; professors see 5 (no Departments/Users)

### Roll Number Format

- GCUF roll numbers are always **6 digits** in the award sheet format
- Stored and validated consistently across the system

## 📚 Key Files Reference

| File | Purpose |
|------|---------|
| `artifacts/api-server/src/lib/grading.ts` | GCUF grading scale, GPA calculation, percentage logic |
| `lib/db/src/schema/gcuf.ts` | Complete database schema |
| `artifacts/api-server/src/lib/pdfParser.ts` | PDF parsing logic with x-position column detection |
| `artifacts/gcuf-web/src/index.css` | Color palette and global styles |

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is licensed under the **MIT License** - see the `package.json` for details.

---

**Built with ❤️ for GCUF**
