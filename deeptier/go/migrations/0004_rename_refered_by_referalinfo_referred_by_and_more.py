# Generated by Django 4.2.11 on 2024-05-24 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('go', '0003_remove_voucher_user_delete_referral'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referalinfo',
            old_name='refered_by',
            new_name='referred_by',
        ),
        migrations.RenameField(
            model_name='referalinfo',
            old_name='uid',
            new_name='referred_user',
        ),
        migrations.AddField(
            model_name='referalinfo',
            name='voucher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='go.voucher'),
        ),
        migrations.DeleteModel(
            name='ReferralWallet',
        ),
    ]