from realestate.audit_context import (
    set_current_user,
    set_current_ip,
    clear_audit_context,
)


class AuditContextMiddleware:
    """
    Har bir request uchun foydalanuvchi va IP manzilni
    Audit Log tizimiga yetkazib beradi.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)

        if user is not None and user.is_authenticated:
            set_current_user(user)
        else:
            set_current_user(None)

        set_current_ip(self.get_client_ip(request))

        try:
            response = self.get_response(request)
            return response

        finally:
            clear_audit_context()

    @staticmethod
    def get_client_ip(request):
        """
        Foydalanuvchining IP manzilini aniqlaydi.
        """

        forwarded_for = request.META.get(
            'HTTP_X_FORWARDED_FOR'
        )

        if forwarded_for:
            return forwarded_for.split(',')[0].strip()

        return request.META.get(
            'REMOTE_ADDR'
        )