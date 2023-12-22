from .serializers import StatusSerializer
from .services import (
    create_status,
    delete_user_status,
    get_user_status,
    get_user_status_detail,
    update_user_status,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from src.apps.user.authentication import CustomUserAuthentication


class StatusCreateListApi(APIView):
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        serializer.instance = create_status(user=request.user, status=data)
        return Response(data=serializer.data)

    def get(self, request):
        status_collection = get_user_status(user=request.user)
        serializer = StatusSerializer(status_collection, many=True)
        return Response(data=serializer.data)


class StatusRetrieveUpdateDelete(APIView):
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, status_id):
        status = get_user_status_detail(status_id=status_id)
        serializer = StatusSerializer(status)
        return Response(data=serializer.data)

    def delete(self, request, status_id):
        delete_user_status(user=request.user, status_id=status_id)
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, status_id):
        serializer = StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status = serializer.validated_data
        serializer.instance = update_user_status(
            user=request.user, status_id=status_id, status_data=status
        )

        return Response(data=serializer.data)
