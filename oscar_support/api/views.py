from django.db.models import get_model

from rest_framework import viewsets

from oscar.core.compat import get_user_model

from . import serializers
from .mixins import UserFilterMixin

User = get_user_model()
Group = get_model('auth', 'Group')


class CustomerViewSet(UserFilterMixin, viewsets.ModelViewSet):
    model = User
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return self.filter_queryset(self.model.objects.all())


class AgentViewSet(UserFilterMixin, viewsets.ModelViewSet):
    model = User
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return self.filter_queryset(self.model.objects.filter(is_staff=True))


class GroupViewSet(viewsets.ModelViewSet):
    model = Group
