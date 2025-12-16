# School ERP (Open Source)

A starter **School Management System** backend (API + database schema) that covers:
- Students & teachers
- Enrollment (year/section)
- Attendance
- Assessments & results
- Fees, invoices, payments
- Role-based access: **ADMIN / REGISTRAR / TEACHER / FINANCE / STUDENT**

This repository is designed to be easy to run with **Docker**.

## Quick start (recommended)

1. Install Docker Desktop
2. From the repo folder run:

```bash
docker compose up --build
```

3. Create the database tables (migrations) and seed demo users:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_demo
```

4. Open:
- API: http://localhost:8000/
- Admin: http://localhost:8000/admin/

### Demo logins
After `seed_demo`, these users exist (password for all: `Passw0rd!`):
- admin@example.com (ADMIN)
- registrar@example.com (REGISTRAR)
- finance@example.com (FINANCE)
- teacher@example.com (TEACHER)
- student@example.com (STUDENT)

## API Auth (JWT)

Obtain tokens:
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"Passw0rd!"}'
```

Refresh:
```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<refresh token>"}'
```

Use access token:
```bash
curl http://localhost:8000/api/students/ \
  -H "Authorization: Bearer <access token>"
```

## Pushing to GitHub

1. Create a new repository on GitHub (e.g. `school-erp`)
2. In this folder:

```bash
git init
git add .
git commit -m "Initial commit: school ERP starter"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

## License
MIT
