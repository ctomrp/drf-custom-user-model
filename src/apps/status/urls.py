from .apis import StatusCreateListApi, StatusRetrieveUpdateDelete
from django.urls import path

urlpatterns = [
    path("status/", StatusCreateListApi.as_view(), name="status"),
    path(
        "status/<int:status_id>",
        StatusRetrieveUpdateDelete.as_view(),
        name="status_detail",
    ),
]
