from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from users.helpers import (
    list_users,
    create_user,
)
from users.serializers import UserSchema


class UserList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tasks = list_users()
        ser = UserSchema()
        return Response(ser.dump(tasks, many=True).data)


class UserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        ser = UserSchema()
        results = ser.load(request.data)
        if results.errors:
            return Response(results.errors, status=status.HTTP_400_BAD_REQUEST)
        user = create_user(
            email=results.data['email'],
            password=results.data['password'],
            first_name=results.data['first_name'],
            last_name=results.data['last_name'],
        )
        return Response(ser.dump(user).data, status=status.HTTP_201_CREATED)

# TODO: workflow for forgetting and resetting password
