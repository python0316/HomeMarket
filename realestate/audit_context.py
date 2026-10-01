from contextvars import ContextVar


_current_user = ContextVar(
    'current_user',
    default=None,
)

_current_ip = ContextVar(
    'current_ip',
    default=None,
)


def set_current_user(user):
    """
    Joriy request foydalanuvchisini saqlaydi.
    """
    _current_user.set(user)


def get_current_user():
    """
    Joriy request foydalanuvchisini qaytaradi.
    """
    return _current_user.get()


def set_current_ip(ip_address):
    """
    Joriy request IP manzilini saqlaydi.
    """
    _current_ip.set(ip_address)


def get_current_ip():
    """
    Joriy request IP manzilini qaytaradi.
    """
    return _current_ip.get()


def clear_audit_context():
    """
    Request tugagandan keyin contextni tozalaydi.
    """
    _current_user.set(None)
    _current_ip.set(None)