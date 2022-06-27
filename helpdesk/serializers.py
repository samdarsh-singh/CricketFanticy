from rest_framework import serializers
from .models import Ticket
import uuid


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['token', 'content']
        read_only_fields = ['token']

    def create(self, validated_data, **extra_fields):
        instance = self.Meta.model(**validated_data)
        ticket_str = str(uuid.uuid4()).split("-")[-1]
        instance.token = ticket_str
        instance.save()

        return instance
