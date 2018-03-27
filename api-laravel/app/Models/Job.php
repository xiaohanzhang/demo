<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\DB;

class Job extends Model
{
    protected $table = 'jobs';
    protected $primaryKey = 'job_id';
    protected $keyType = 'string';

    public function tenant()
    {
        return $this->belongsTo('App\Models\Tenant');
    }

    static function complex_example() 
    {
        // return raw data instead of active record, hard to take advantage from JobResource
        return self::query()
            ->join('tenants', 'jobs.tenant_id', '=', 'tenants.tenant_id')
            ->join('orders', 'jobs.job_id', '=', 'orders.job_id')
            ->where('tenants.tenant_name', '=', 'Vandelay Promotions')
            ->where(function ($query) {
                $query->where('orders.order_type', '=', 'PRESENTATION')
                    ->orWhere('tenants.hidden', '=', true)
                ;
            })
            ->limit(20)
            ->get()
        ;

    }
}
