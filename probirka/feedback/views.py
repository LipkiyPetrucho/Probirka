from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.none()  # посторонние не могут смотреть список
    serializer_class = ContactMessageSerializer
    permission_classes = [
        AllowAny
    ]  # доступен всем ﻿:contentReference[oaicite:3]{index=3}
