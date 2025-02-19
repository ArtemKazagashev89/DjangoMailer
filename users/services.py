from django.core.cache import cache

from config.settings import CACHE_ENABLED

from .models import CustomUser

CACHE_TIMEOUT = 60


class CustomUserService:

    @staticmethod
    def get_all_users():
        if not CACHE_ENABLED:
            return CustomUser.objects.all()
        key = "all_users"
        users = cache.get(key)
        if users is not None:
            return users
        users = CustomUser.objects.all()
        cache.set(key, users, CACHE_TIMEOUT)
        return users
