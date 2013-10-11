from django.contrib import admin
from django.db.models import get_model


admin.site.register(get_model('oscar_support', 'Note'))
admin.site.register(get_model('oscar_support', 'Ticket'))
admin.site.register(get_model('oscar_support', 'Message'))
admin.site.register(get_model('oscar_support', 'TicketType'))
admin.site.register(get_model('oscar_support', 'TicketStatus'))
