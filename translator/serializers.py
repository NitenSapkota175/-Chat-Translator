from rest_framework import serializers
from .models import TranslationHistory


class TranslationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationHistory
        fields = "__all__"


class TranslationRequestSerializers(serializers.Serializer):
    source_text = serializers.CharField()
    source_language = serializers.CharField(max_length=10)
    target_language = serializers.CharField(max_length=10)
