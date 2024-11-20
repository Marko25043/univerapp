from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Korisnik,Upisi,Uloga
admin.site.register(Upisi)
class KorisnikAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_superuser','email','role', 'status')}),
    )

admin.site.register(Korisnik,KorisnikAdmin)
admin.site.register(Uloga)
#tp12345678
#iv1234678
# 
