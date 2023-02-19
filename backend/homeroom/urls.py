from django.urls import path
from .views import JoinRoomView, CreateRoomView, LeaveRoomView, EndRoomView

urlpatterns = [
    path('create-room/', CreateRoomView.as_view(), name='create_room'),
    path('join-room/', JoinRoomView.as_view(), name='join_room'),
    path('leave-room/', LeaveRoomView.as_view(), name='leave_room'),
    path('end-room/', EndRoomView.as_view(), name='end_room'),
]
