from django.db import models
from datetime import datetime

class GP(models.Model):
    id = models.AutoField(primary_key=True)
    appointment_ids = models.ManyToManyField('Appointment')
    name = models.CharField(max_length=255, default="Default Name")
    slots = models.DateField(default=datetime.now)  # Date field to represent the available slots
    description = models.TextField(default="No description available")
    
    @classmethod
    def get_appointments_for_gp(cls, gp_id):
        try:
            gp = cls.objects.get(pk=gp_id)
            return gp.appointment_ids.all()
        except cls.DoesNotExist:
            return None  # GP not found
        
    @classmethod
    def get_appointments_for_gp_and_date(cls, gp_id, target_date):
        try:
            gp = cls.objects.get(pk=gp_id)
            appointments = gp.appointment_ids.filter(time_stamp__date=target_date)
            return appointments
        except cls.DoesNotExist:
            return None  # GP not found
    @classmethod
    def get_all_gp(cls):

            return cls.objects.all()

    @classmethod
    def add_appointment_to_gp(cls, gp_id, user_id, time_stamp):
        try:
            gp = cls.objects.get(pk=gp_id)
            appointment_time = datetime.fromisoformat(time_stamp)
            appointment = Appointment(user=user_id, time_stamp=appointment_time)
            appointment.save()
            
            gp.appointment_ids.add(appointment)
            return appointment
        except GP.DoesNotExist:
            return None  # GP not found
        except Exception as e:
            print(e)  # Handle any potential exceptions
            return None

    def __str__(self):
        return f"GP {self.id}"
    
class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField()
    time_stamp = models.DateTimeField()
    
    @classmethod
    def get_appointments_for_user(cls, user_id):
        try:
            return cls.objects.filter(user=user_id)
        except cls.DoesNotExist:
            return None  # User not found
    
    @classmethod
    def delete_appointment(cls, appointment_id):
        try:
            appointment = cls.objects.get(pk=appointment_id)
            appointment.delete()
            return True
        except cls.DoesNotExist:
            return False  # Appointment not found

    @classmethod
    def add_appointment(cls, user_id, time_stamp):
        try:
            appointment_time = datetime.fromisoformat(time_stamp)
            appointment = cls(user=user_id, time_stamp=appointment_time)
            appointment.save()
            return appointment.id
        except Exception as e:
            print(e)  # Handle any potential exceptions
            return False
    
    def __str__(self):
        return f"Appointment {self.id}"