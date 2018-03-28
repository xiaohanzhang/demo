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


class Phone(SoftDeleteModel):
    class Meta:
        db_table = 'phones'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='phone_id')
    phone_number = models.CharField(max_length=20)
    phone_extension = models.CharField(max_length=10, default='')
    # TODO: fix enum field
    phone_type = models.CharField(
        max_length=63,
        default='WORK',
        choices=(
            ('WORK', 'WORK',),
            ('HOME', 'HOME',),
            ('CELL', 'CELL'),
            ('FAX', 'FAX'),
        )
    )
    # TODO: fix enum field
    parent_type = models.CharField(
        max_length=63,
        default='CONTACT',
        choices=(
            ('CONTACT', 'CONTACT',),
            ('SUPPLIER', 'SUPPLIER',),
            ('SUPPLIER-ACCOUNT', 'SUPPLIER-ACCOUNT',),
            ('CLIENT', 'CLIENT',),
            ('TENANT', 'TENANT',),
            ('TENANT-ACCOUNT', 'TENANT-ACCOUNT',),
        )
    )
    parent_id = models.CharField(max_length=36)


class File(models.Model):
    class Meta:
        db_table = 'files'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='file_id')


class Department(SoftDeleteModel):
    class Meta:
        db_table = 'departments'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='department_id')
    department_name = models.CharField(max_length=255)
    parent_type = models.CharField(
        max_length=63,
        default=None,
        choices=(
            ('SUPPLIER', 'SUPPLIER',),
            ('CLIENT', 'CLIENT',),
            ('TENANT', 'TENANT',),
        )
    )
    ordering = models.IntegerField(default=None)


class UserInvitation(models.Model):
    class Meta:
        db_table = 'user_invitations'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='user_invitation_id')


class Address(SoftDeleteModel):
    class Meta:
        db_table = 'addresses'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='address_id')
    address_name = models.CharField(max_length=100)
    address_company = models.CharField(max_length=100, default='')
    address_line_1 = models.CharField(max_length=100, default='')
    address_line_2 = models.CharField(max_length=100, default='')
    address_line_3 = models.CharField(max_length=100, default='')
    address_line_4 = models.CharField(max_length=100, default='')
    address_city = models.CharField(max_length=45)
    address_state = models.CharField(max_length=45)
    address_postal = models.CharField(max_length=45, default='')
    address_country = models.CharField(max_length=45)
    # TODO: fix enum field
    address_type = models.CharField(
        max_length=63,
        choices=(
            ('BILLING', 'BILLING',),
            ('SHIPPING', 'SHIPPING',),
            ('BOTH', 'BOTH'),
        )
    )
    address_default = models.CharField(
        max_length=63,
        choices=(
            ('BILLING', 'BILLING',),
            ('SHIPPING', 'SHIPPING',),
            ('BOTH', 'BOTH'),
            ('NONE', 'NONE'),
        )
    )
    parent_id = models.CharField(max_length=36)
    # TODO: fix enum field
    parent_type = models.CharField(
        max_length=63,
        default='CONTACT',
        choices=(
            ('CONTACT', 'CONTACT',),
            ('SUPPLIER', 'SUPPLIER',),
            ('SUPPLIER-ACCOUNT', 'SUPPLIER-ACCOUNT',),
            ('CLIENT', 'CLIENT',),
            ('TENANT', 'TENANT',),
            ('TENANT-ACCOUNT', 'TENANT-ACCOUNT',),
        )
    )


class Contact(SoftDeleteModel):
    class Meta:
        db_table = 'contacts'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='contact_id')
    contact_first_name = models.CharField(max_length=100, default='')
    contact_last_name = models.CharField(max_length=100, default='')
    contact_position = models.CharField(max_length=100, default='')
    contact_email = models.CharField(max_length=100, default='')
    contact_twitter = models.CharField(max_length=255, default='')
    contact_facebook = models.CharField(max_length=255, default='')
    contact_linkedin = models.CharField(max_length=255, default='')
    contact_skype = models.CharField(max_length=255, default='')
    contact_default_phone = models.ForeignKey('Phone', on_delete=models.SET_NULL, null=True)
    contact_default_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)
    contact_no_marketing = models.BooleanField(default=False)
    contact_image = models.ForeignKey('File', on_delete=models.SET_NULL, null=True)
    contact_tags = models.TextField(default='')
    contact_invitation = models.ForeignKey('UserInvitation', on_delete=models.DO_NOTHING, default='')
    contact_department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    parent_contact = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)


class JobTemplate(models.Model):
    class Meta:
        db_table = 'job_templates'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='job_template_id')


class Tenant(SoftDeleteModel):
    class Meta:
        db_table = 'tenants'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='tenant_id')
    tenant_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=100, null=True, default=None)
    tenant_domain_key = models.CharField(max_length=255)
    tenant_status = models.CharField(
        max_length=63,
        default='ACTIVE',
        choices=(
            ('ACTIVE', 'ACTIVE',),
            ('TRIAL', 'TRIAL',),
            ('PROSPECT', 'PROSPECT',),
            ('INACTIVE', 'INACTIVE',),
        )
    )
    tenant_fiscal_year_end_month = models.IntegerField(default=12)
    tenant_fiscal_year_end_day = models.IntegerField(default=31)
    tenant_terms_and_conditions = models.TextField()
    tenant_default_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)
    tenant_default_job_template = models.ForeignKey('JobTemplate', on_delete=models.SET_NULL, null=True)
    default_currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True, default='USD')
    hidden = models.BooleanField(default=False)

'''
  `price_type` enum('AUTOMATIC','FIXED') NOT NULL DEFAULT 'AUTOMATIC',
  `price_period` enum('ANNUAL','MONTHLY') NOT NULL DEFAULT 'ANNUAL',
  `default_user_monthly_price` decimal(10,4) NOT NULL DEFAULT '0.0000',
  `monthly_price` decimal(8,2) NOT NULL DEFAULT '0.00',
  `price_tax_id` varchar(100) NOT NULL DEFAULT '',
  `tenant_notes` text NOT NULL,
  `primary_contact_id` char(36) DEFAULT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `active` tinyint(1) DEFAULT '1',
  `tenant_activation_key` varchar(100) DEFAULT NULL,
  `background_image_id` char(36) DEFAULT NULL,
  `background_image_position` int(11) NOT NULL DEFAULT '0',
  `website` varchar(255) DEFAULT NULL,
  `size` varchar(255) NOT NULL DEFAULT '',
  `potential_size` int(11) NOT NULL DEFAULT '0',
  `sage_account` varchar(50) NOT NULL DEFAULT '',
  `sage_login` varchar(50) NOT NULL DEFAULT '',
  `sage_password` varchar(50) NOT NULL DEFAULT '',
  `esp_id` varchar(50) NOT NULL DEFAULT 'active',
  `esp_secret` varchar(50) NOT NULL DEFAULT '',
  `capture_addresses_from` timestamp NULL DEFAULT NULL,
  `capture_addresses_to` timestamp NULL DEFAULT NULL,
  `has_xero` tinyint(1) NOT NULL DEFAULT '0',
  `public` tinyint(1) NOT NULL DEFAULT '1',
  `total_revenue_category` varchar(7) DEFAULT NULL,
  `zos` varchar(15) DEFAULT NULL,
  `association_type` varchar(15) DEFAULT NULL,
  `default_header_id` varchar(36) NOT NULL DEFAULT '',
  `default_invoice_view` varchar(20) NOT NULL DEFAULT 'DETAIL',
  `show_cardconnect` tinyint(1) NOT NULL DEFAULT '0',
  `maximum_commission` int(11) NOT NULL DEFAULT '100',
  `feedback_text` varchar(255) DEFAULT NULL,
  `show_shopify` tinyint(1) DEFAULT '0',
  `collaborate_beta` tinyint(1) NOT NULL DEFAULT '0',
  `async_sage_push` tinyint(1) NOT NULL DEFAULT '0',
  `po_with_job_number` tinyint(4) NOT NULL DEFAULT '0',
  `stripe_customer_id` char(50) DEFAULT NULL,
  `stripe_unpaid` tinyint(4) DEFAULT '0',
  `suspended` tinyint(4) NOT NULL DEFAULT '0',
'''


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


class Industry(SoftDeleteModel):
    class Meta:
        db_table = 'industries'

    id = models.CharField(
        primary_key=True, default=uuid.uuid4, max_length=36, db_column='industry_id')
    tenant = models.ForeignKey('Tenant', related_name='industries',  on_delete=models.PROTECT)
    industry_name = models.CharField(max_length=100)


class Tax(SoftDeleteModel):
    class Meta:
        db_table = 'taxes'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='tax_id')
    tenant = models.ForeignKey('Tenant', related_name='taxes',  on_delete=models.PROTECT)
    label = models.CharField(max_length=10)
    description = models.TextField(default='')
    percent = models.DecimalField(max_digits=10, decimal_places=3, default=None, null=True)
    tenant_registration = models.CharField(max_length=100, default='')
    tax_exempt = models.BooleanField(default=False)
    editable = models.BooleanField(default=True)


class Terms(SoftDeleteModel):
    class Meta:
        db_table = 'terms'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='terms_id')
    terms_name = models.CharField(max_length=100)
    days_to_add = models.IntegerField(default=0)
    display_order = models.IntegerField(default=None, null=True)


class Currency(models.Model):
    class Meta:
        db_table = 'currencies'

    id = models.CharField(primary_key=True, max_length=4, db_column='currency_id')
    currency_country = models.CharField(max_length=100)
    currency_name = models.CharField(max_length=100)
    currency_symbol = models.CharField(max_length=8, default='$')


class Status(models.Model):
    class Meta:
        db_table = 'status'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='status_id')
    parent_type = models.CharField(max_length=20)
    status_name = models.CharField(max_length=25)
    flow_order = models.IntegerField(default=0)


class CommissionClientRate(models.Model):
    class Meta:
        db_table = 'commission_client_rates'

    id = models.CharField(
        primary_key=True, default=uuid.uuid4, max_length=36, db_column='commission_client_rate_id')
    company_id = models.CharField(max_length=36)
    client_rate_label = models.CharField(max_length=255, default='')
    multiplier = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)


class Client(SoftDeleteModel):
    class Meta:
        db_table = 'clients'

    id = models.CharField(
        primary_key=True, default=uuid.uuid4, max_length=36, db_column='client_id')
    tenant = models.ForeignKey('Tenant', related_name='clients',  on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='+')
    prospect = models.BooleanField(default=False)
    client_name = models.CharField(max_length=255)
    client_website = models.URLField(max_length=255, default='')
    client_facebook = models.URLField(max_length=255, default='')
    client_twitter = models.URLField(max_length=255, default='')
    client_tenant_account_number = models.CharField(max_length=255, default='')
    client_order_margin_minimum = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    sales_target = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # TODO: fix enum field
    priority = models.CharField(
        max_length=63,
        default='MEDIUM',
        choices=(
            ('LOW', 'LOW',),
            ('MEDIUM', 'MEDIUM',),
            ('HIGH', 'HIGH'),
        )
    )
    primary_contact = models.ForeignKey('Contact', on_delete=models.DO_NOTHING, related_name='+')
    secondary_contact = models.ForeignKey('Contact', on_delete=models.DO_NOTHING, related_name='+')
    tertiary_contact = models.ForeignKey('Contact', on_delete=models.DO_NOTHING, related_name='+')
    industry = models.ForeignKey('Industry', on_delete=models.DO_NOTHING)
    default_tax = models.ForeignKey('Tax', on_delete=models.DO_NOTHING)
    default_terms = models.ForeignKey('Terms', on_delete=models.DO_NOTHING)
    default_currency = models.ForeignKey('Currency', on_delete=models.DO_NOTHING)
    sales_rep = models.ForeignKey('User', on_delete=models.DO_NOTHING, related_name='+')
    client_tags = models.CharField(max_length=200, default='')
    client_profile = models.TextField(default='')
    account_status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True)
    commission_client_rate = models.ForeignKey('CommissionClientRate', on_delete=models.SET_NULL, null=True)
    parent_client = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='+')
    quickbooks_id = models.CharField(max_length=100, default='')
    date_quickbooks = models.DateTimeField(default='0000-00-00 00:00:00')
    latest_use = models.DateTimeField(auto_now=True)
    xero_contact_id = models.CharField(max_length=36, default=None, null=True)
    qbo_customer_ref = models.IntegerField(default=None, null=True)
    date_merged = models.DateTimeField(default='0000-00-00 00:00:00')
    merged_by = models.CharField(max_length=36, default=None, null=True)
