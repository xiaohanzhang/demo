# python3 django

```python
# commonsku_model.py
class CskuSoftDeleteModel(models.Model):
    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(active_only=False)

    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'User', on_delete=models.DO_NOTHING, related_name='+', db_column='created_by')

    class Meta:
        abstract = True

    def delete(self):
        self.active = False
        self.save()

    def hard_delete(self):
        super(SoftDeleteModel, self).delete()


# models.py
class Tenant(CskuSoftDeleteModel):
    class Meta:
        db_table = 'tenants'

    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36, db_column='tenant_id')
    tenant_name = models.CharField(max_length=255)
    primary_contact = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True)
    hidden = models.BooleanField(default=False)

# serializers.py
class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        exclude = ('active', 'date_created',)

    tenant_id = serializers.UUIDField(read_only=True, source='pk')
    primary_contact = ContactSerializer(many=False, read_only=True)
    jobs = JobSerializer(many=True, read_only=True)

# views.py
class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

# urls.py
router = routers.DefaultRouter()
router.register(r'tenants', TenantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# complex query
## relation join
query_set = (
    Tenant.objects
        .filter(tenant_name__icontains='vandelay')
        .filter(Q(jobs__orders__order_type='PRESENTATION') | Q(hidden=True))
)[:20]
## eager loading fk
Tenant.objects.all().select_related('primary_contact__address')
## eager loading one to many
Teannt.objects.all().prefetch_related('jobs__orders')
```


```php
// app/Models/Tenant.php
class Tenant extends Model
{
    protected $table = 'tenants';
    protected $primaryKey = 'tenant_id';
    protected $keyType = 'string';

    public function jobs()
    {
        return $this->hasMany('App\Models\Job');
    }

    public function primary_contact()
    {
        return $this->belongsTo('App\Models\Contact', 'primary_contact_id');
    }
}

// app/Http/Resources/TenantResource.php
class TenantResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->tenant_id,
            'tenant_name' => $this->tenant_name,
            'hide' => $this->hide,
            'primary_contact' => $this->whenLoaded('primary_contact'),
            'jobs' => $this->whenLoaded('jobs'),
        ];
    }
}

// app/Http/Controllers/TenantController.php
class TenantController extends BaseController
{
    public function index(Request $request) {
        return TenantResource::collection(Tenant::paginate());
    }

    public function show(string $id) {
        return new TenantResource(Tenant::find($id));
    }
}

// routes/api.php
Route::middleware('api')->group(function () {
    Route::apiResources([
        'tenants' => 'TenantController',
    ]);
});

// complex query, Eloquent can't handle complex query, need use query builder here
//// relation join
self::query()
    ->join('orders', 'jobs.job_id', '=', 'orders.job_id')
    ->where('tenants.tenant_name', '=', 'Vandelay Promotions')
    ->where('tenants.active', '=', true)
    ->where(function ($query) {
        $query->where('orders.order_type', '=', 'PRESENTATION')
            ->where('orders.active', '=', true)
            ->orWhere('tenants.hidden', '=', true)
        ;
    })
    ->limit(20)
    ->get()
;
```

# personal opinion 
## Auth, CRUD, validator, middleware, cache, log
django = laravel
## model
django: model field type defination, multiple type of model inheritance, flexable model manager
larvel: only has basic relation support
## query builder
python: django-orm / sqlalchemy both very good
php: eloquent only handles simple CRUD query, need use raw query builder for complex join/filter
## performance
php > python
## library / tools
django > laravel(laravel is growing)
Usually python lib are easier to use and more elegant. (pdf, debuger) 
## documentation
django: better text documentation
laravel: lots of videos
## django highlight
migration
class-based views
django-filter
admin