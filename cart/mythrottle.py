from collections import Counter

from rest_framework.throttling import SimpleRateThrottle
from .models import User


class UserLoginRateThrottle(SimpleRateThrottle):
    scope = 'getwheeeldetail'

    def get_cache_key(self, request, view):
        print(request.user.id, request.user.pk)

        user = User.objects.get(id=request.path_info.split('/')[-2])
        ident = user.id if user else self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }



# from rest_framework.throttling import UserRateThrottle
#
#
# class MyThrottle(UserRateThrottle):
#     rate = '1/day'
#     cache_format = 'throttle_%(scope)s_%(ident)s_%(detail)s'
#
#
#     scope = 'user'
#
#     def get_cache_key(self, request, view):
#         if request.user.is_authenticated:
#             ident = request.user.id
#         else:
#             ident = self.get_ident(request)
#
#         return self.cache_format % {
#             'scope': self.scope,
#             'ident': ident,
#             'detail': view.kwargs.get("id")
#         }