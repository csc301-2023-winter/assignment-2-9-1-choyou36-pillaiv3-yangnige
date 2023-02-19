from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, StudentSerializer, TeacherSerializer


class RegistrationUser(APIView):
    def post(self, request):
        serializers = UserSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)


class RegistrationStudent(APIView):
    def post(self, request):
        serializers = StudentSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)


class RegistrationTeacher(APIView):
    def post(self, request):
        serializers = TeacherSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)
