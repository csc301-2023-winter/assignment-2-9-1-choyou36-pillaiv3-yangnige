from django.urls import path
from views import RegistrationUser, RegistrationStudent, RegistrationTeacher

urlpatterns = [
    path('register_as_user/', RegistrationUser.as_view(), name='register_user'),
    path('register_as_student/', RegistrationStudent.as_view(),
         name='register_student'),
    path('register_as_teacher/', RegistrationTeacher.as_view(),
         name='register_teacher'),
]

