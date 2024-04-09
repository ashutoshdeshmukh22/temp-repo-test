from django.contrib import admin
from django.contrib import auth
from .models import ClientProfile, app_configs, Transactions, SquredOffTransactions, Scripts

admin.site.unregister(auth.models.Group)

try:
    from rest_framework.authtoken.models import TokenProxy as DRFToken
except ImportError:
    from rest_framework.authtoken.models import Token as DRFToken

admin.site.unregister(DRFToken)

# Register your models here.
admin.site.register(ClientProfile)
admin.site.register(app_configs)
admin.site.register(Transactions)
admin.site.register(SquredOffTransactions)
admin.site.register(Scripts)