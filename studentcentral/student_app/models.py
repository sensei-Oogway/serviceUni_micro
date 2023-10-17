from django.db import models

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_code = models.CharField(max_length=20,default="ABC123")  # Add subject code field
    name = models.CharField(max_length=255)
    details = models.TextField(default='No details available')  # Add details field

    @classmethod
   
    def get_all_subjects(cls):
        return cls.objects.all()
    
    def __str__(self):
        return self.name
    
class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField()
    subjects = models.ManyToManyField(Subject)  # Add a ManyToManyField for subjects

    @classmethod
    def add_enrollment(cls, user_id, subject_ids):
        try:
            enrollment = cls(user=user_id)
            enrollment.save()
            for subject_id in subject_ids:
                subject = Subject.objects.get(pk=subject_id)
                enrollment.subjects.add(subject)
            return enrollment
        except Subject.DoesNotExist:
            return None  # Subject not found

    @classmethod
    def delete_enrollment(cls, user_id, subject_ids):
        try:
            enrollment = cls.objects.get(user_id=user_id)
            for subject_id in subject_ids:
                subject = Subject.objects.get(pk=subject_id)
                enrollment.subjects.remove(subject)
            return True
        except cls.DoesNotExist:
            return False  # Enrollment not found
        except Subject.DoesNotExist:
            return False  # Subject not found
        
    @classmethod
    def get_subjects_for_user(cls, user_id):
        try:
            user_enrollment = cls.objects.get(user_id=user_id)
            return user_enrollment.subjects.all()
        except cls.DoesNotExist:
            return []

    def __str__(self):
        return f"Enrollment {self.id}"