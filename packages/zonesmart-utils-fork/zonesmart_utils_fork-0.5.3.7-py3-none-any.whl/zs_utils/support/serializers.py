from rest_framework import serializers
from rest_framework.exceptions import ValidationError


__all__ = [
    "CommonSupportTicketSerializer",
    "CommonCreateSupportTicketSerializer",
    "CommonSupportTicketMessageSerializer",
    "CommonCreateSupportTicketMessageSerializer",
    "CommonSupportTicketMessageFileSerializer",
]


class CommonSupportTicketSerializer(serializers.ModelSerializer):
    user = None
    manager = None

    class Meta:
        fields = [
            "id",
            "number",
            "created",
            "user",
            "manager",
            "status",
            "question_type",
            "subject",
            "unread_messages",
        ]


class CommonCreateSupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "question_type",
            "subject",
        ]


class CommonSupportTicketMessageSerializer(serializers.ModelSerializer):
    sender = None
    files = None

    class Meta:
        fields = [
            "id",
            "created",
            "ticket",
            "sender",
            "text",
            "files",
            "is_system",
            "is_viewed",
        ]


class CommonCreateSupportTicketMessageSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, allow_null=True)
    files = None

    @staticmethod
    def get_signature():
        raise NotImplementedError(
            "В сериализаторе должен быть определён метод получения подписи сообщения для пользователя"
        )

    @classmethod
    def get_support_ticket(cls):
        raise NotImplementedError("В сериализаторе должен быть определён метод получения модели SupportTicket")

    def to_internal_value(self, data):
        signature = self.get_signature()
        if signature:
            user = self.get_support_ticket().objects.get(id=data["ticket"]).user.id
            if data.get("text") and (data["sender"] != user):
                data["text"] += signature

        data = super().to_internal_value(data)

        if not (data.get("text") or data.get("files")):
            raise ValidationError({"text": "Обязательное поле, если не задано поле 'files'."})

        return data


class CommonSupportTicketMessageFileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "ticket_message",
            "file",
        ]
