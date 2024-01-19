from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from zs_utils.support import constants
from zs_utils.views import CustomModelViewSet


__all__ = [
    "BaseSupportTicketView",
    "BaseSupportTicketMessageView",
    "BaseSupportTicketMessageFileView",
]


class BaseSupportTicketView(CustomModelViewSet):
    """
    Абстрактный View для создания и просмотра тикетов (SupportTicket)
    """
    not_allowed_actions = [
        "destroy",
        "update",
        "partial_update",
    ]
    staff_permission_classes = []

    @classmethod
    def get_support_ticket_service(cls):
        raise NotImplementedError("В отображении должен быть определён метод получения модели SupportTicketService")

    @classmethod
    def get_create_support_ticket_serializer(cls):
        raise NotImplementedError(
            "В отображении должен быть определён метод получения модели CreateSupportTicketSerializer"
        )

    def limit_queryset(self, queryset):
        """
        Фильтрация QuerySet относительно роли пользователя
        """
        user = self.get_user()

        if getattr(user, "is_admin", False) or getattr(user, "is_superuser", False):
            return queryset
        elif getattr(user, "is_staff", False):
            return queryset.filter(Q(manager=user) | Q(status=constants.SUPPORT_TICKET_STATUSES.PENDING))

        return super().limit_queryset(queryset)

    @action(detail=True, methods=["POST"])
    def close(self, request, *args, **kwargs):
        """
        Закрытие тикета
        """
        self.get_support_ticket_service().close_ticket(user=self.get_user(), ticket=self.get_object())
        return self.build_response()

    def create(self, request, *args, **kwargs):
        data = self.get_validated_data(serializer_class=self.get_create_support_ticket_serializer())
        message = data.pop("message") if "message" in data else None
        user = self.get_user()
        with transaction.atomic():
            instance = self.get_support_ticket_service().create_ticket(user=user, **data)
            if message:
                self.get_support_ticket_service().create_ticket_message(
                    ticket=instance, sender=user, is_system=False, **message
                )
        return self.build_response(data=self.get_serializer_class()(instance).data, status_code=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"], permission_classes=staff_permission_classes)
    def take_to_work(self, request, *args, **kwargs):
        """
        Взятие тикета в работу (для staff пользователей)
        """
        if not self.staff_permission_classes:
            raise NotImplementedError("В сервисе должен быть определён staff_permission_classes")

        self.get_support_ticket_service().take_ticket(manager=self.get_user(), ticket=self.get_object())
        return self.build_response()

    @action(detail=True, methods=["POST"])
    def reopen(self, request, *args, **kwargs):
        """
        Открыть закрытый тикет
        """
        self.get_support_ticket_service().reopen_ticket(user=self.get_user(), ticket=self.get_object())
        return self.build_response()

    @action(detail=True, methods=["POST"])
    def set_viewed(self, request, *args, **kwargs):
        self.get_support_ticket_service().set_ticket_viewed(user=self.get_user(), ticket=self.get_object())
        return self.build_response()

    @action(detail=False, methods=["GET"])
    def get_metadata(self, request, *args, **kwargs):
        """
        Получение метаданных тикета (возможные статусы и тип вопроса)
        """
        data = {
            "status": constants.SUPPORT_TICKET_STATUSES,
            "question_type": constants.SUPPORT_TICKET_QUESTION_TYPES,
        }
        return self.build_response(data=data)


class BaseSupportTicketMessageView(CustomModelViewSet):
    """
    Абстрактный View для создания/удаления/обновления/просмотра сообщений тикета (SupportTicketMessage)
    """
    not_allowed_actions = [
        "update",
        "partial_update",
        "destroy",
    ]

    @classmethod
    def get_support_ticket(cls):
        raise NotImplementedError("В отображении должен быть определён метод получения модели SupportTicket")

    @classmethod
    def get_support_ticket_service(cls):
        raise NotImplementedError("В отображении должен быть определён метод получения модели SupportTicketService")

    @classmethod
    def get_create_support_ticket_message_serializer(cls):
        raise NotImplementedError(
            "В отображении должен быть определён метод получения модели CreateSupportTicketMessageSerializer"
        )

    @staticmethod
    def get_signature():
        return ""

    def get_queryset_filter_kwargs(self) -> dict:
        return {"ticket": self.kwargs["ticket_id"]}

    def create(self, request, *args, **kwargs):
        """
        Подстановка тикета SupportTicket.id и пользователя (отправителя) при создании нового сообщения
        """
        data = self.get_validated_data(serializer_class=self.get_create_support_ticket_message_serializer())
        ticket = self.get_support_ticket().objects.get(id=kwargs["ticket_id"])
        sender = self.get_user()

        signature = self.get_signature()
        if signature:
            if data.get("text") and (sender == ticket.manager):
                data["text"] += signature

        instance = self.get_support_ticket_service().create_ticket_message(
            ticket=ticket, sender=sender, is_system=False, **data,
        )
        return self.build_response(data=self.serializer_class(instance).data, status_code=status.HTTP_201_CREATED)


class BaseSupportTicketMessageFileView(CustomModelViewSet):
    """
    Абстрактный View для создания/удаления/обновления/просмотра файлов сообщений (SupportTicketMessageFile)
    """
    parser_classes = (MultiPartParser,)
    not_allowed_actions = [
        "update",
        "partial_update",
        "destroy",
    ]
