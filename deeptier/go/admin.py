from django.contrib import admin
from .models import CustomUser, EmailTemplate, Voucher, ReferalInfo

def phone_number(obj):
    """
    Function to get phone number from custom user model
    """
    try:
        user = CustomUser.objects.get(uid=obj.uid)
        return user.phone_number
    except CustomUser.DoesNotExist:
        return None
    
@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ["purpose", "subject", "body"]

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = ["uid", "phone_number", "company_name", "is_superuser"]


@admin.register(ReferalInfo)
class ReferalInfoAdmin(admin.ModelAdmin):
    list_display = ["voucher", "referred_user", "referred_by", "created_at", "modified_at"]

    def phone_number(self, obj):
        return phone_number(obj)
    
@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ["code", "discount_amount", "is_redeemed", "created_at"]
    
# @admin.register(ReferralWallet)
# class ReferralWalletAdmin(admin.ModelAdmin):
#     list_display = ["user", "get_vouchers"]

#     def get_vouchers(self, obj):
#         return ", ".join([voucher.code for voucher in obj.vouchers.all()])
#     get_vouchers.short_description = 'Vouchers'
