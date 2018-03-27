import {
    Entity, PrimaryGeneratedColumn, Column, ManyToOne, OneToMany, JoinTable, BaseEntity, JoinColumn
} from 'typeorm';

@Entity('tenants')
export class Tenant extends BaseEntity {

    @PrimaryGeneratedColumn('uuid', { name: 'tenant_id' })
    tenantId: string;

    @Column('varchar', { name: 'tenant_name' })
    tenantName: string;

    @Column('tinyint', {
        default: true,
    })
    active: boolean;

    @OneToMany((type) => Job, (job) => job.tenant)
    jobs: Job[];

    @OneToMany((type) => Order, (order) => order.tenant)
    orders: Order[];
}

@Entity('jobs')
export class Job extends BaseEntity {

    @PrimaryGeneratedColumn('uuid', { name: 'job_id' })
    jobId: string;

    @ManyToOne((type) => Tenant, (tenant) => tenant.jobs, { eager: true })
    @JoinColumn({ name: 'tenant_id' })
    tenant: Tenant;

    @Column('varchar', { name: 'job_name' })
    jobName: string;

    @Column('int', { name: 'job_number' })
    jobNumber: number;

    @Column('tinyint', {
        default: true,
    })
    active: boolean;

    @OneToMany((type) => Order, (order) => order.job)
    orders: Order[];
}

@Entity('orders')
export class Order extends BaseEntity {

    @PrimaryGeneratedColumn('uuid', { name: 'order_id' })
    orderId: string;

    @ManyToOne((type) => Tenant, (tenant) => tenant.orders)
    @JoinColumn({ name: 'tenant_id' })
    tenant: Tenant;

    @ManyToOne((type) => Job, (job) => job.orders)
    @JoinColumn({ name: 'job_id' })
    job: Job;

    @Column('varchar', { name: 'order_type' })
    orderType: string;

    @Column('int', { name: 'form_number' })
    formNumber: number;

    @Column('tinyint', {
        default: true,
    })
    active: boolean;

    @OneToMany((type) => Item, (item) => item.order)
    items: Item[];
}

@Entity('items')
export class Item extends BaseEntity {

    @PrimaryGeneratedColumn('uuid', { name: 'order_id' })
    orderId: string;

    @ManyToOne((type) => Order, (order) => order.items)
    @JoinColumn({ name: 'order_id' })
    order: Order;

    @Column('varchar', { name: 'item_name' })
    itemName: string;
}
