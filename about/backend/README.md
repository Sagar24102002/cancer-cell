# Django backend (cancer_site)

Setup and run (Windows):

1. Create and activate a virtualenv (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run migrations and create superuser:

```powershell
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

4. Run development server:

```powershell
python manage.py runserver
```

The API root will be at `http://localhost:8000/api/` (e.g. `http://localhost:8000/api/patients/`).
