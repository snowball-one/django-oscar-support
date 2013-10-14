import mock

from django.utils import unittest
from django.contrib.auth.models import User

from oscar_support.api.mixins import UserFilterMixin
from oscar_support.api.serializers import UserSerializer


class TestUserFilterMixin(unittest.TestCase):

    def setUp(self):
        super(TestUserFilterMixin, self).setUp()
        self.queryset = mock.Mock()
        self.queryset.filter = mock.Mock()

    def _get_mocked_request(self, value):
        request = mock.Mock()
        request.GET = mock.Mock()
        request.GET.get = mock.Mock(return_value=value)
        return request

    def test_can_filter_only_on_email(self):
        user_filter = UserFilterMixin()
        user_filter.request = self._get_mocked_request(value='b@some')

        user_filter.filter_queryset(self.queryset)
        self.queryset.filter.assert_called_once_with(email__icontains='b@some')

    def test_can_filter_on_all_fields(self):
        search_term = 'Pet'
        user_filter = UserFilterMixin()
        user_filter.request = self._get_mocked_request(value=search_term)

        user_filter.filter_queryset(self.queryset)
        self.assertTrue(self.queryset.filter.called)

        Q_object = self.queryset.filter.call_args[0][0]
        self.assertSequenceEqual(
            [(k, v) for k, v in Q_object.children],
            [
                ('first_name__istartswith', search_term),
                ('last_name__istartswith', search_term),
                ('email__istartswith', search_term),
            ]
        )


class TestUserSerializer(unittest.TestCase):

    def setUp(self):
        super(TestUserSerializer, self).setUp()
        self.serializer = UserSerializer()

    def test_display_text_is_empty_for_invalid_object(self):
        self.assertEquals(self.serializer.get_display_text(obj=None), '')

    def test_display_text_including_full_name(self):
        user = User(
            email='test@email.com',
            first_name='Peter',
            last_name="Griffin"
        )
        self.assertEquals(
            self.serializer.get_display_text(user),
            'Peter Griffin <test@email.com>'
        )

    def test_display_text_including_email_only(self):
        user = User(email='test@email.com')
        self.assertEquals(
            self.serializer.get_display_text(user),
            'test@email.com'
        )
