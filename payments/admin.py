from django.contrib import admin
from django import forms  
import uuid;
from authapp.models import User
from .models import Invoice, Item,PaymentHistory

class ItemInlineForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'  

class ItemInline(admin.StackedInline):  
    model = Item
    form = ItemInlineForm
    extra = 1  
    

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'user', 'amount', 'is_paid', 'due_date', 'payment_method')
    list_filter = ('is_paid', 'due_date')
    search_fields = ('invoice_number', 'user__username', 'user__email')
    inlines = [ItemInline]
    ordering = ['invoice_number']  
    list_filter = ('is_paid','payment_method') 
   
    readonly_fields = ('invoice_number',)  # Make the invoice_number field readonly
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":           
            kwargs["queryset"] = User.objects.filter(is_client=True).all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def save_model(self, request, obj, form, change):        
        if not obj.invoice_number:
            unique_id = uuid.uuid4().hex[:8]  
            obj.invoice_number = f"DYR-{unique_id}"
        obj.save()


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Item)


class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_date', 'payment_method', 'payment_status')
    list_filter = ('payment_status', 'payment_date')
    search_fields = ('user__username', 'transaction_id','invoice__invoice_number')
    readonly_fields = ('payment_date',) 
    list_per_page = 20  
       
    # def get_queryset(self, request):        
    #     user_ids = [user.uid for user in PaymentHistory.objects.filter(user__is_client=True).select_related('user').only('user')]
    #     queryset = super().get_queryset(request).filter(user_id__in=user_ids)
    #     return queryset    

    def user_full_name(self, obj):        
        return f'{obj.user.first_name} {obj.user.last_name}'
    user_full_name.short_description = 'User'     
    ordering = ('-payment_date',)

admin.site.register(PaymentHistory, PaymentHistoryAdmin)

# Working