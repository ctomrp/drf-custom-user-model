from .models import Status
from dataclasses import dataclass
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import exceptions
from src.apps.user.services import UserDataClass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .models import Status
    from src.apps.user.models import User


@dataclass
class StatusDataClass:
    content: str
    date_published: datetime = None
    user: UserDataClass = None
    id: int = None

    @classmethod
    def from_instance(cls, status_model: "Status") -> "StatusDataClass":
        return cls(
            content=status_model.content,
            date_published=status_model.date_published,
            id=status_model.id,
            user=status_model.user,
        )


def create_status(user, status: "StatusDataClass") -> "StatusDataClass":
    status_create = Status.objects.create(content=status.content, user=user)

    return StatusDataClass.from_instance(status_model=status_create)


def get_user_status(user: "User") -> list["StatusDataClass"]:
    user_status = Status.objects.filter(user=user)

    return [
        StatusDataClass.from_instance(single_status) for single_status in user_status
    ]


def get_user_status_detail(status_id: int) -> "StatusDataClass":
    status = get_object_or_404(Status, pk=status_id)

    return StatusDataClass.from_instance(status_model=status)


def delete_user_status(user: "User", status_id: int) -> "StatusDataClass":
    status = get_object_or_404(Status, pk=status_id, user=user)

    if user.id != status.user.id:
        raise exceptions.PermissionDenied("You're not the user fool")

    status.delete()


def update_user_status(user: "User", status_id: int, status_data: "StatusDataClass"):
    status = get_object_or_404(Status, pk=status_id, user=user)

    if user.id != status.user.id:
        raise exceptions.PermissionDenied("You're not the user fool")

    status.content = status_data.content
    status.save()

    return StatusDataClass.from_instance(status_model=status)
