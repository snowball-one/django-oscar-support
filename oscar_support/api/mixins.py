from django.db.models import Q


class UserFilterMixin(object):

    def filter_on_email(self, qs, search_term):
        return qs.filter(email__icontains=search_term)

    def filter_on_all(self, qs, search_term):
        return qs.filter(
            Q(first_name__istartswith=search_term) |
            Q(last_name__istartswith=search_term) |
            Q(email__istartswith=search_term)
        )

    def filter_queryset(self, qs):
        search_term = self.request.GET.get('filter')
        if not search_term:
            return qs
        if '@' in search_term:
            return self.filter_on_email(qs, search_term)
        return self.filter_on_all(qs, search_term)
