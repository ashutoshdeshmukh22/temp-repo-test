from rest_framework import serializers
from playground.models import ClientProfile, app_configs, Transactions, SquredOffTransactions, token_log, Scripts
from django.utils import timezone
import pytz

class ISTDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        # Convert datetime to IST timezone
        tz = pytz.timezone('Asia/Kolkata')
        value = timezone.localtime(value, tz)
        return super().to_representation(value)
    
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = '__all__'


class AppConfigSerializer(serializers.ModelSerializer):
    created_at = ISTDateTimeField()
    updated_at = ISTDateTimeField()
    class Meta:
        model = app_configs
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):

    created_at = ISTDateTimeField()
    updated_at = ISTDateTimeField()
    class Meta:
        model = Transactions
        fields = "__all__"

class SquaredOffTransactionSerializer(serializers.ModelSerializer):
    created_at = ISTDateTimeField()
    updated_at = ISTDateTimeField()
    class Meta:
        model = SquredOffTransactions
        fields = "__all__"

class TokenLogSerializers(serializers.ModelSerializer):
    created_at = ISTDateTimeField()
    class Meta:
        model = token_log
        fields = "__all__"

class ScriptsSerializers(serializers.ModelSerializer):
    created_at = ISTDateTimeField()
    updated_at = ISTDateTimeField()
    class Meta:
        model = Scripts
        fields = "__all__"
