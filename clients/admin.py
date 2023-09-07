from django.contrib import admin

from .models import Clients


class ClientsAdmin(admin.ModelAdmin):
    list_display = (
        "get_user_name",
        "get_user_full_name",
        "get_organization_name",
        "get_subsidiary_name",
        'organization_name',
        "phone_no",
    )

    def get_organization_name(self, obj):
        return obj.subsidiary.organization.name

    get_organization_name.short_description = "Organization Name"

    def get_user_name(self, obj):
        return obj.user.username

    get_user_name.short_description = "User Id"

    def get_user_full_name(self, obj):
        return obj.user.first_name +" "+ obj.user.last_name
    
    get_user_full_name.short_description = "Client Name"

    def get_subsidiary_name(self, obj):
        return obj.subsidiary.name

    get_subsidiary_name.short_description = "Subsidiary Name"


admin.site.register(Clients, ClientsAdmin)
