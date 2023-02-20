from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from .serializers import HomeroomSerializer
from accounts.models import PlayUser
from rest_framework.permissions import IsAuthenticated
from .models import homeroom
import random


class CreateRoomView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        copy_data = request.data.copy()
        if request.user.get_type() == "teacher":
            if 'homeroom_id' not in copy_data:
                homeroom_id = random.randint(10000000, 99999999)
                copy_data['homeroom_id'] = homeroom_id
            elif homeroom.objects.filter(homeroom_id=copy_data['homeroom_id']).first() is not None:
                return Response("Room already exists", status=400)
            copy_data['teacher_id'] = request.user.email
            serializers = HomeroomSerializer(data=copy_data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)
        else:
            return Response("Must be a registered teacher", status=401)

class JoinRoomView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        copy_data = request.data.copy()
        if 'homeroom_id' not in copy_data:
            return Response("Please enter a room id", status=400)
        
        homeroom_id = copy_data['homeroom_id']
        if homeroom.objects.filter(homeroom_id = homeroom_id).first() is None:
            return Response("Enter a valid room id", status=400)
        
        request.user.homeroom_id = homeroom_id
        request.user.save()
        return Response("Joined room: " + str(homeroom_id))

class LeaveRoomView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        if request.user.homeroom_id is None:
            return Response("Currently not in a room", status=400)
        else:
            homeroom_id = request.user.homeroom_id
            request.user.homeroom_id = None
            request.user.save()
            return Response("Left room " + str(homeroom_id))

class EndRoomView(DestroyAPIView):
    permission_classes = [IsAuthenticated, ]

    serializer_class = HomeroomSerializer
    model = homeroom

    def post(self, request):
        if 'homeroom_id' not in self.request.data:
            return Response("Please enter a room id", status=400)
        if homeroom.objects.filter(homeroom_id=self.request.data['homeroom_id']).first() is None:
            return Response("Please enter a valid room that you started", status=400)
        
        if homeroom.objects.filter(
                homeroom_id=self.request.data['homeroom_id']).first().teacher_id == request.user.email:
            hmrm = homeroom.objects.filter(homeroom_id=self.request.data['homeroom_id'])
            users = PlayUser.objects.filter(homeroom_id=self.request.data['homeroom_id']).update(
                homeroom_id=None)
            hmrm.delete()
            return Response("Room Ended")
        else:
            return Response("You do not have permission to end this room", status=401)
