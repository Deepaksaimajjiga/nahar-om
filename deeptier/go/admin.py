from django.contrib import admin
from .models import *
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
    list_display = ["uid", "phone_number", "refered_by", "created_at"]

    def phone_number(self, obj):
        return phone_number(obj)