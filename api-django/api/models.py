import uuid
from django.db import models
from .base import SoftDeleteModel


class Login(SoftDeleteModel):
    class Meta:
        db_table = 'logins'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='login_id')
    login_name = models.CharField(max_length=255)


class User(SoftDeleteModel):
    class Meta:
        db_table = 'users'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='user_id')
    login = models.ForeignKey('Login', on_delete=models.SET_NULL, null=True)


class Tenant(SoftDeleteModel):
    class Meta:
        db_table = 'tenants'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='tenant_id')
    tenant_name = models.CharField(max_length=255)
    hidden = models.BooleanField()


class Job(SoftDeleteModel):
    class Meta:
        db_table = 'jobs'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='job_id')
    tenant = models.ForeignKey('Tenant', on_delete=models.SET_NULL, null=True)
    client_rep = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    job_name = models.CharField(max_length=255)
    job_number = models.IntegerField()


class Order(SoftDeleteModel):
    class Meta:
        db_table = 'orders'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='order_id')
    tenant = models.ForeignKey('Tenant', on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey('Job', related_name='orders',  on_delete=models.SET_NULL, null=True)
    form_number = models.IntegerField()
    order_type = models.CharField(max_length=50)


class Item(models.Model):
    class Meta:
        db_table = 'items'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='item_id')
    order = models.ForeignKey('Order', related_name='items',  on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=255)

