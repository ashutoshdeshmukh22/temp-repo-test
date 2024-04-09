from rest_framework import serializers
from playground.models import Scripts, Transactions

class ScriptsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Scripts
        fields = "__all__"

class TransactionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = "__all__"