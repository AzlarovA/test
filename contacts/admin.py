from django.contrib import admin
from .models import Contact, Social, FAQ, ContactPageForm
# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ("company", "address", 'telephone_1')
    list_display_links = ("company", "address", 'telephone_1')


class SocialAdmin(admin.ModelAdmin):
    list_display = ("soci", "text")
    list_display_links = ("soci", "text")


admin.site.register(Contact, ContactAdmin)
admin.site.register(Social, SocialAdmin)
admin.site.register(FAQ)
admin.site.register(ContactPageForm)

