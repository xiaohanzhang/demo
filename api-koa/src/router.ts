import * as Router from 'koa-router';
import { Brackets } from 'typeorm';

import { Tenant, Job, Order, Item } from './entity';

const router = new Router();

router.get('/jobs/', async (ctx, next) => {
  const jobs = await Job.createQueryBuilder()
    .innerJoinAndMapOne('Job.tenant', 'Tenant', 'Tenant')
    .innerJoinAndMapMany('Job.orders', 'Order', 'Order')
    .innerJoinAndMapMany('Order.items', 'Item', 'Item')
    .where('Tenant.tenant_name = :tenantName', { tenantName: 'Vandelay Promotions' })
    .where('Order.active = 1')
    .andWhere(new Brackets((qb) => {
      qb.where('Order.order_type = :orderType', { orderType: 'PRESENTATION' })
        .orWhere('Tenant.hidden = 1')
      ;
    }))
    .limit(20)
    .getMany()
  ;
  ctx.body = {
    jobs,
  };
});

export default router;
