from idlelib.iomenu import errors
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User, Patient, Doctor, PatientDoctorMapping
from .serializers import RegisterSerializer, LoginSerializer, AddPatientSerializer, DoctorSerializer, \
    PatientDoctorSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

# Register Route
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    serialized_input = RegisterSerializer(data=data)
    if serialized_input.is_valid():
        user = serialized_input.save()
        return Response({
            "message": "User registered successfully!",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized_input.errors, status=status.HTTP_400_BAD_REQUEST)

# Login Route
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = LoginSerializer(data=request.data)
    if data.is_valid():
        email = data.validated_data['email']
        password = data.validated_data['password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "token": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                },
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)



#patient Management endpoints

#adding new patient and getting all patients
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def patient(request):
    if request.method == 'POST':
        data = AddPatientSerializer(data = request.data)
        if data.is_valid():
            patient = data.save()
            return  Response({"message":"Patient Added successfully",
                              "patient":{
                                  "id":patient.id,
                                  "name":patient.name,
                                  "mobile":patient.mobile,
                                  "address":patient.address,
                                  "disease":patient.disease
                              }},status=status.HTTP_201_CREATED)
        return Response(data.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        try:
            patients = Patient.objects.all()
            serialized_patients = AddPatientSerializer(patients, many=True)
            return Response(serialized_patients.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Something went wrong", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message':"Method not allowed"},status=status.HTTP_400_BAD_REQUEST)

#getting , updating , deleting specific patient by id
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def get_patient_by_id(request,id):
    try:
        patient = Patient.objects.get(id=id)
        if patient:
            if request.method == 'GET':
                return Response({'message':f'Patient found with is {id}','Patient':{
                    'id':patient.id,
                    'name':patient.name,
                    'disease':patient.disease,
                    'mobile':patient.mobile,
                    'address':patient.address,
                    'age':patient.age
                }},status=status.HTTP_200_OK)
            elif request.method == 'PUT':
                serializer = AddPatientSerializer(patient, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'Patient updated successfully', 'patient': serializer.data},
                                    status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif request.method == 'DELETE':
                patient.delete()
                return Response({'message': 'Patient deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message':"Method not allowed"},status=status.HTTP_400_BAD_REQUEST)

    except Patient.DoesNotExist:
        return Response({'message':"patient not found"},status=status.HTTP_404_NOT_FOUND)


# Doctor Management endpoints

# Adding and getting all doctors from db

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def doctor(request):
    if request.method == 'POST':
        data = DoctorSerializer(data=request.data)
        if data.is_valid():
            new_doctor = data.save()
            return Response({'message':"Doctor Created successfully",'Doctor':{
                'name':new_doctor.name,
                'age':new_doctor.age,
                'mobile':new_doctor.mobile,
                'address':new_doctor.address,
                'specialist':new_doctor.specialist
            }},status=status.HTTP_201_CREATED)
        return Response(data.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        try:
            doctors = Doctor.objects.all()
            serialized_doc = DoctorSerializer(doctors,many=True)
            return Response(serialized_doc.data,status=status.HTTP_200_OK)
        except errors as e:
            return Response({"message": "Something went wrong", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message':"Method not allowed"},status=status.HTTP_400_BAD_REQUEST)

#getting , updating , deleting specific doctor by id
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def doctor_by_id(request,id):
    try:
        doctor = Doctor.objects.get(id=id)
        if doctor:
            if request.method == 'GET':
                return Response({'message':f'Doctor found at id {id}','doctor':{
                    'name':doctor.name,
                    'age':doctor.age,
                    'mobile':doctor.mobile,
                    'address':doctor.address,
                    'specialist':doctor.specialist
                }},status=status.HTTP_200_OK)
            elif request.method == 'PUT':
                updated_doc = DoctorSerializer(doctor,data=request.data,partial=True)
                if updated_doc.is_valid():
                    updated_doc.save()
                    return Response({'message':"Doctor Details updated successfully",'doctor':updated_doc.data},status=status.HTTP_200_OK)
                return Response(updated_doc.errors,status=status.HTTP_400_BAD_REQUEST)
            elif request.method == 'DELETE':
                doctor.delete()
                return Response({'message':'Doctor deleted successfully'},status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)

    except Doctor.DoesNotExist:
        return Response({'message':"Doctor not found"},status=status.HTTP_404_NOT_FOUND)


# Patient-Doctor Mapping endpoints

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def mapping(request):
    if request.method == 'POST':
        serializmapping = PatientDoctorSerializer(data=request.data)
        if serializmapping.is_valid():
            serializmapping.save()
            return Response({'message':'Doctor assign to patient'},status=status.HTTP_201_CREATED)
        return Response(serializmapping.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        try:
            all_mapping = PatientDoctorMapping.objects.all()
            serialize_all_mapping = PatientDoctorSerializer(all_mapping,many=True)
            return Response(serialize_all_mapping.data,status=status.HTTP_200_OK)
        except errors as e:
            return Response({'message':'Something went wrong','error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message':"Method not allowed"},status=status.HTTP_400_BAD_REQUEST)

#all doctors to a specific patient & Deleting doc from mapping with id

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def get_doctors_by_patient(request, patient_id):
    if request.method == 'GET':
        mappings = PatientDoctorMapping.objects.filter(patient__id=patient_id)
        if mappings:
            serializer = PatientDoctorSerializer(mappings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'DELETE':
        try:
            mapping_to_del = PatientDoctorMapping.objects.get(id=patient_id)
            mapping_to_del.delete()
            return Response({'message': 'Mapping deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except PatientDoctorMapping.DoesNotExist:
            return Response({'error': 'Mapping Not Found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message':"Method not allowed"},status=status.HTTP_400_BAD_REQUEST)










