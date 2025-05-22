from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class Patient(models.Model):
    objects = None
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    mobile = models.CharField(max_length=13, unique=True)
    address = models.CharField(max_length=256)
    disease = models.CharField(max_length=256)

    def __str__(self):
        return self.name


# SPECIALIST_CHOICES = [
#     ('Cardiologist', 'Cardiologist'),
#     ('Dermatologist', 'Dermatologist'),
#     ('Endocrinologist', 'Endocrinologist'),
#     ('Gastroenterologist', 'Gastroenterologist'),
#     ('Neurologist', 'Neurologist'),
#     ('Oncologist', 'Oncologist'),
#     ('Orthopedic Surgeon', 'Orthopedic Surgeon'),
#     ('Pediatrician', 'Pediatrician'),
#     ('Psychiatrist', 'Psychiatrist'),
#     ('Radiologist', 'Radiologist'),
#     ('Urologist', 'Urologist'),
#     ('General Physician', 'General Physician'),
#     ('ENT Specialist', 'ENT Specialist'),
#     ('Ophthalmologist', 'Ophthalmologist'),
#     ('Pulmonologist', 'Pulmonologist'),
#     ('Rheumatologist', 'Rheumatologist'),
#     ('Nephrologist', 'Nephrologist'),
#     ('Allergist', 'Allergist'),
#     ('Surgeon', 'Surgeon'),
#     ('Gynecologist', 'Gynecologist'),
# ]
class Doctor(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    address = models.CharField(max_length=256)
    mobile = models.CharField(max_length=15 , unique=True)
    specialist = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='doctor_mappings')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='patient_mappings')

    def __str__(self):
        return f"{self.patient.name} <-> {self.doctor.name}"