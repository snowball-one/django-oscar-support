from django.contrib import admin
from django.db.models import get_model


admin.site.register(get_model('oscar_support', 'TicketType'))
admin.site.register(get_model('oscar_support', 'TicketStatus'))
admin.site.register(get_model('oscar_support', 'Ticket'))
admin.site.register(get_model('oscar_support', 'Priority'))
admin.site.register(get_model('oscar_support', 'Message'))
admin.site.register(get_model('oscar_support', 'RelatedOrder'))
admin.site.register(get_model('oscar_support', 'RelatedOrderLine'))
admin.site.register(get_model('oscar_support', 'RelatedProduct'))
admin.site.register(get_model('oscar_support', 'Attachment'))
