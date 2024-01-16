from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_support_tiket_model():
    """
    Возвращает модель SupportTicket для текущего проекта.
    """
    try:
        return django_apps.get_model(settings.SUPPORT_TIKET_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "SUPPORT_TIKET_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "SUPPORT_TIKET_MODEL refers to model '%s' that has not been installed"
            % settings.AUTH_USER_MODEL
        )


def get_support_tiket_model():
    """
    Возвращает модель SupportTicket для текущего проекта.
    """
    try:
        return django_apps.get_model(settings.SUPPORT_TIKET_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "SUPPORT_TIKET_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "SUPPORT_TIKET_MODEL refers to model '%s' that has not been installed"
            % settings.AUTH_USER_MODEL
        )
