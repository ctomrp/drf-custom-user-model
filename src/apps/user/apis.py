from rest_framework import exceptions, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .services import UserDataClass
from . import authentication


class RegisterApi(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        serializer.instance = UserDataClass.create_user(user_dc=data)

        return Response(data={"hello": "world"})


class LoginApi(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = UserDataClass.user_email_selector(email=email)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        token = UserDataClass.create_token(user_id=user.id)

        resp = Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


class UserApi(APIView):
    """
    This endpoint will only be available
    it the user is authenticated
    """

    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutApi(APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        resp = Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "so long farewell"}

        return resp
