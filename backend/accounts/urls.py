from django.urls import path
from .views import RegistrationUser, RegistrationStudent, RegistrationTeacher

urlpatterns = [
     path('register-user/', RegistrationUser.as_view(), name='register_user'),
     path('register-student/', RegistrationStudent.as_view(), name='register_student'),
     path('register-teacher/', RegistrationTeacher.as_view(), name='register_teacher'),
]

