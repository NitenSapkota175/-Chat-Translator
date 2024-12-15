from django.shortcuts import render
import requests
from .serializers import TranslationHistorySerializer, TranslationRequestSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TranslationHistory
from rest_framework import status


class TranslateTextView(APIView):

    def get(self, request, *args, **kwargs):
        # Render an empty form initially
        return render(request, "translator/translate.html", {"translated_text": None})

    def post(self, request, *args, **kwargs):
        serializer = TranslationRequestSerializers(data=request.data)
        if serializer.is_valid():
            source_text = serializer.validated_data["source_text"]
            source_language = serializer.validated_data["source_language"]
            target_language = serializer.validated_data["target_language"]

            url = "https://libretranslate.com/translate"
            payload = {
                "q": source_text,
                "source": source_language,
                "target": target_language,
            }
            headers = {"Content-Type": "application/json"}

            try:
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    translated_text = response.json.get("translatedText")
                    history = TranslationHistory.objects.create(
                        source_text=source_text,
                        targer_text=translated_text,
                        source_language=source_language,
                        target_language=target_language,
                    )
                    history_serializer = TranslationHistorySerializer(history)
                    # return Response(history_serializer.data, status=status.HTTP_200_OK)

                    return render(
                        request,
                        "translator/translate.html",
                        {
                            "source_text": source_text,
                            "translated_text": translated_text,
                            "source_language": source_language,
                            "target_language": target_language,
                        },
                    )

                else:
                    return render(
                        request,
                        "translator/translate.html",
                        {"error": "Translation failed"},
                    )
                # return Response(
                #     {"error": "Translation_faild"}, status=response.status_code
                # )
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
