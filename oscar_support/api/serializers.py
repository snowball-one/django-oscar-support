from rest_framework import serializers

from oscar.core.compat import get_user_model


class UserSerializer(serializers.ModelSerializer):
    display_text = serializers.SerializerMethodField('get_display_text')

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'display_text')

    def get_display_text(self, obj):
        if not obj:
            return ''
        full_name = obj.get_full_name()
        if full_name:
            return "{0} <{1}>".format(full_name, obj.email)
        return obj.email
