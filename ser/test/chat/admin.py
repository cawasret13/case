from django.contrib import admin

from chat.models import item, cases, HistoryCase, Users


admin.site.register(item)
admin.site.register(cases)
admin.site.register(HistoryCase)
admin.site.register(Users)
