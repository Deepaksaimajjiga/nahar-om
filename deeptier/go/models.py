from django.db import models
from django.contrib.auth.models import AbstractUser
import random, string
from .user_manager import UserManager
import os
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class CustomUser(AbstractUser):
    """
    A custom user model. Every user of this project is defined by this model. It may be seller, or admin
    """

    username = None
    uid = models.CharField(max_length=10, primary_key=True)
    phone_number = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    company_name = models.CharField(max_length=200, default="No company name")
    entity_type = models.CharField(max_length=150, default="No entity type")
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["password"]
    objects = UserManager()

    def unique_id_generator(self):
        """This function generates a unique 10 digit id for every user. In this complete project this id is called UId"""
        # Generate a random 6-character string
        random_string = "".join(random.choices(string.ascii_uppercase, k=6))

        # Generate a random 4-digit number
        random_number = "".join(random.choices(string.digits, k=4))

        # Combine the two to form a 10-character unique ID
        generated_id = f"{random_string}{random_number}"

        # Check if the generated ID already exists in the table
        while CustomUser.objects.filter(uid=generated_id).exists():
            generated_id = self.unique_id_generator()  # Regenerate if it already exists

        return generated_id

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = self.unique_id_generator()

        super().save(*args, **kwargs)

    def _str_(self):
        return f"{self.uid}"

    def get_full_name(self):
        """
        Return the full name of the user.
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.uid

class Voucher(models.Model):
    # referral = models.ForeignKey(ReferalInfo, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_redeemed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class ReferalInfo(models.Model):
    """
    This model helps to store the referral information.
    Sellers can refer a new seller and based on that they may gets some benefits
    """
    voucher = models.ForeignKey(Voucher,null=True,blank = True, on_delete=models.CASCADE)

    referred_user = models.OneToOneField(
        CustomUser,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="refered_to_user",
    )
    referred_by = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="refered_by_user"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"{self.uid}"   

# class ReferralWallet(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     vouchers = models.ForeignKey(Voucher,)

#     def __str__(self):
#         return f"{self.user}'s Referral Wallet"
    
#     @staticmethod
#     def pre_delete_referral_wallet(sender, instance, **kwargs):
#         # Delete vouchers associated with the referral wallet
#         instance.vouchers.clear()

# Connect pre_delete_referral_wallet method to pre_delete signal of ReferralWallet
# models.signals.pre_delete.connect(ReferralWallet.pre_delete_referral_wallet, sender=ReferralWallet)
    
class EmailTemplate(models.Model):
    purpose = models.CharField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"{self.purpose}"