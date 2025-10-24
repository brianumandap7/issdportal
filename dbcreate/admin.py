from django.contrib import admin
from .models import Ticket_tbl, IR_tbl, Roles, Responder_tbl, Classification_tbl, Severity_tbl, TLP_tbl, Status_tbl, Genders
# Register your models here.


admin.site.register(Ticket_tbl)
admin.site.register(IR_tbl)
admin.site.register(Roles)
admin.site.register(Responder_tbl)
admin.site.register(Classification_tbl)
admin.site.register(Severity_tbl)
admin.site.register(TLP_tbl)
admin.site.register(Status_tbl)
admin.site.register(Genders)