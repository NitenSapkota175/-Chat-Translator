from rest_framework import serializers
from .models import TranslationHistory


class TranslationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationHistory
        fields = "__all__"


class TranslationRequestSerializers(serializers.Serializer):
    source_text = serializers.TextField()
    target_text = serializers.TextField()
    source_language = serializers.CharField(max_length=10)
