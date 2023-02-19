from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from .serializers import HomeroomSerializer
from accounts.models import PlayUser
from .models import homeroom
import random


class CreateRoomView(APIView):
    def post(self, request):
        copy_data = request.data.copy()
        email = copy_data['email']
        Usr = PlayUser.objects.filter(email=email).first()
        if Usr.get_type() == "teacher":
            homeroom_id = random.randint(10000000, 99999999)
            copy_data['homeroom_id'] = homeroom_id
            copy_data['teacher_id'] = email
            serializers = HomeroomSerializer(data=copy_data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)
        else:
            return Response("Must be a registered teacher")

class JoinRoomView(APIView):

    def post(self, request):
        copy_data = request.data.copy()
        email = copy_data['email']
        PlayUse = PlayUser.objects.filter(email=email).first()
        homeroom_id = copy_data['homeroom_id']
        if homeroom.objects.get(homeroom_id = homeroom_id) is None:
            return Response("Enter a valid room id")
        PlayUse.homeroom_id = homeroom_id
        PlayUse.save()
        return Response("Joined room: " + str(homeroom_id))

class LeaveRoomView(APIView):
    def post(self, request):
        copy_data = request.data.copy()
        email = copy_data['email']
        PlayUse = PlayUser.objects.filter(email=email).first()
        if PlayUse.homeroom_id is None:
            return Response("Currently not in a room")
        else:
            homeroom_id = PlayUse.homeroom_id
            PlayUse.homeroom_id = None
            PlayUse.save()
            return Response("Left room " + str(homeroom_id))

class EndRoomView(DestroyAPIView):
    serializer_class = HomeroomSerializer
    model = homeroom

    def post(self, request):
        if homeroom.objects.filter(homeroom_id=self.request.data['homeroom_id']).first() is None:
            return Response("Please enter a valid room that you started")
        if homeroom.objects.filter(
                homeroom_id=self.request.data['homeroom_id']).first().teacher_id == \
                self.request.data["email"]:
            hmrm = homeroom.objects.filter(homeroom_id=self.request.data['homeroom_id'])
            users = PlayUser.objects.filter(homeroom_id=self.request.data['homeroom_id']).update(
                homeroom_id=None)
            hmrm.delete()
            return Response("Room Ended")
        else:
            return Response("You do not have permission to end this room")
