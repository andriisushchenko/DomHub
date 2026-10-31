PREMIUM_GROUP = 'Premium'


def is_premium(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name=PREMIUM_GROUP).exists()


def premium_context(request):
    return {'is_premium': is_premium(request.user)}
