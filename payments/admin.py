from django.contrib import admin
from django import forms  # Import forms from here
import uuid;
from .models import Invoice, Item,PaymentHistory

class ItemInlineForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'  

class ItemInline(admin.TabularInline):  
    model = Item
    form = ItemInlineForm
    extra = 1  

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            # Filter the User queryset to show only clients (is_client=True and is_employee=False)
            kwargs["queryset"] = User.objects.filter(is_client=True, is_employee=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'user', 'amount', 'is_paid', 'due_date', 'payment_method')
    list_filter = ('is_paid', 'due_date')
    search_fields = ('invoice_number', 'user__username', 'user__email')
    inlines = [ItemInline]
    
    readonly_fields = ('invoice_number',)  # Make the invoice_number field readonly

    def save_model(self, request, obj, form, change):
        # Generate invoice number if it's empty
        if not obj.invoice_number:
            unique_id = uuid.uuid4().hex[:8]  # Generate a unique ID
            obj.invoice_number = f"DYR-{unique_id}"
        obj.save()

# Register the admin class and form
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Item)
# admin.site.register(Address)

class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_date', 'payment_method', 'payment_status')
    list_filter = ('payment_status', 'payment_date')
    search_fields = ('user__username', 'transaction_id','invoice__invoice_number')
    readonly_fields = ('payment_date',)  # Make payment_date readonly
    list_per_page = 20  # Number of items displayed per page

       
    def get_queryset(self, request):
        # Filter users with is_client set to True
        user_ids = [user.id for user in PaymentHistory.objects.filter(user__is_client=True).select_related('user').only('user')]
        # Get PaymentHistory records related to those users
        queryset = super().get_queryset(request).filter(user_id__in=user_ids)
        return queryset
    

    def user_full_name(self, obj):
        # Display the user's full name in the admin list
        return f'{obj.user.first_name} {obj.user.last_name}'
    user_full_name.short_description = 'User'  # Custom column header

    # Customize the ordering of the list
    ordering = ('-payment_date',)

# Register the PaymentHistory model with the custom admin class
admin.site.register(PaymentHistory, PaymentHistoryAdmin)