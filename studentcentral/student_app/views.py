from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SubjectSerializer, EnrollmentSerializer 
from .models import Subject, Enrollment

@api_view(['POST'])
def add_subject(request):
    if request.method == 'POST':
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def update_enrollment(request, enrollment_id):
    try:
        enrollment = Enrollment.objects.get(pk=enrollment_id)
    except Enrollment.DoesNotExist:
        return Response({'error': 'Enrollment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = EnrollmentSerializer(enrollment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def add_to_enrollment(request, user_id):
    try:
        user_enrollment, created = Enrollment.objects.get_or_create(user=user_id)
      
        if request.method == 'POST':
            subject_id = request.data.get('subject_id')
            try:
                subject = Subject.objects.get(pk=subject_id)

                # Check if the user is already enrolled in the subject
                if subject in user_enrollment.subjects.all():
                    return Response({'error': f'Student is already enrolled in the subject: {subject.name}'}, status=status.HTTP_400_BAD_REQUEST)

                # Add the subject to the user's enrollment
                user_enrollment.subjects.add(subject)

                return Response({'message': f'Subject {subject.name} added to enrollment successfully'}, status=status.HTTP_201_CREATED)

            except Subject.DoesNotExist:
                return Response({'error': f'Subject with ID {subject_id} not found'}, status=status.HTTP_404_NOT_FOUND)

    except Enrollment.DoesNotExist:
        return Response({'error': 'Enrollment not found for the user'}, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def view_subjects(request, user_id):
    try:
        enrollment = Enrollment.objects.get(user=user_id)
    except Enrollment.DoesNotExist:
        return Response({'error': 'Enrollment not found for the user'}, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        subjects = enrollment.subjects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def view_all_subjects(request):
    try:
        subject = Subject.get_all_subjects()

        # Serialize the medicines to JSON
        serialized_subjects = [{"id": subjects.id, "name": subjects.name, "subject_code": subjects.subject_code, "details": subjects.details} for subjects in subject]

        return Response(serialized_subjects, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)