from django.contrib import admin
from django.db.models import get_model


admin.site.register(get_model('ticketing', 'Note'))
admin.site.register(get_model('ticketing', 'Ticket'))
admin.site.register(get_model('ticketing', 'Message'))
admin.site.register(get_model('ticketing', 'TicketType'))
admin.site.register(get_model('ticketing', 'TicketStatus'))
