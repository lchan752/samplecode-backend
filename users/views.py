from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.helpers import list_users
from users.serializers import UserSchema


class UserList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tasks = list_users()
        ser = UserSchema()
        return Response(ser.dump(tasks, many=True).data)
