<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;
use App\Http\Resources\OrderResource;

class JobResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return [
            'job_id' => $this->job_id,
            'tenant' => $this->tenant,
            'orders' => OrderResource::collection($this->whenLoaded('orders')),
        ];
    }
}
