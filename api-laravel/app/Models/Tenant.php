<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Tenant extends Model
{
    protected $table = 'tenants';
    protected $primaryKey = 'tenant_id';
    protected $keyType = 'string';

    public function jobs()
    {
        return $this->hasMany('App\Models\Job');
    }

    public function industry()
    {
        return $this->belongsTo('App\Industry', 'tenant_id');
    }

    public function tenant_account()
    {
        return $this->belongsTo('App\Tenant_Account', 'tenant_id', 'tenant_id');
    }

    public function tenant_user()
    {
        return $this->belongsTo('App\Tenant_User', 'tenant_id', 'tenant_id');
    }

    public function toArray()
    {
        return [
            'id' => $this->tenant_id,
            'name' => $this->tenant_name,
        ];
    }
}
