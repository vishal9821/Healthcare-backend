# Healthcare Backend API

This repository contains the backend code for the Healthcare management system, built with Django and Django REST Framework.

---

## Project Structure

The main backend codebase is located inside:


You will find the Django project and apps within that folder.

Example directory structure:

Healthcare-backend/
└── whatbyte/
  └── HealthCare/
  ├── manage.py
  ├── healthcare_app/
  ├── requirements.txt
  └── ...

---

## Setup and Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd Healthcare-backend/whatbyte/HealthCare
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 
```

# API Endpoints

POST /api/auth/register/ - Register a new user

POST /api/auth/login/ - Login and obtain JWT tokens

POST /api/patients/ - Add a new patient (authenticated users only)

GET /api/patients/ - Retrieve all patients of the authenticated user

GET /api/patients/<id>/ - Get patient details

PUT /api/patients/<id>/ - Update patient details

DELETE /api/patients/<id>/ - Delete a patient record

POST /api/mappings/ - Assign a doctor to a patient

GET /api/mappings/ - Retrieve all patient-doctor mappings

GET /api/mappings/<patient_id>/ - Get all doctors assigned to a patient

DELETE /api/mappings/<id>/ - Remove a doctor from a patient

# Postman Collection

You can import the provided Postman collection file (Healthcare.postman_collection.json) to test all the API endpoints easily.

How to import:

Download the Postman collection file from the repo.

Open Postman.

Click on Import > Upload Files.

Select the collection file.

Use the collection to test requests with example payloads.

# Notes
Make sure to include the JWT token in the Authorization header as Bearer <access_token> for protected routes.

If you want to change JWT token lifespans, configure them in settings.py.

# Contributing
Feel free to fork and open pull requests!

## Postman Collections

You can test the API using the following Postman collections:

1. [User Authentication Collection](https://vvv888-1903.postman.co/workspace/whatbytes~c9b072a2-58b2-47a3-b566-4b5bf51af305/collection/38813735-4d6b393e-8c72-480f-95fe-3750b8eefab0?action=share&creator=38813735)
2. [Patients API Collection](https://vvv888-1903.postman.co/workspace/whatbytes~c9b072a2-58b2-47a3-b566-4b5bf51af305/collection/38813735-ac151237-d13e-4c09-81a8-497354165d73?action=share&creator=38813735)
3. [Doctors Mapping API Collection](https://vvv888-1903.postman.co/workspace/whatbytes~c9b072a2-58b2-47a3-b566-4b5bf51af305/collection/38813735-1429b3bb-aa23-4177-964a-3fa3c7aae65b?action=share&creator=38813735)
4. [All Combined API Collection](https://vvv888-1903.postman.co/workspace/whatbytes~c9b072a2-58b2-47a3-b566-4b5bf51af305/collection/38813735-efe396b6-cd64-4742-a545-71a36df923a8?action=share&creator=38813735)


