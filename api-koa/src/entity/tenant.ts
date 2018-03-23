import {
    Entity, PrimaryGeneratedColumn, Column, ManyToOne, OneToMany, JoinTable, BaseEntity
} from 'typeorm';

@Entity('tenants')
export class Tenant extends BaseEntity {

    @PrimaryGeneratedColumn('uuid')
    tenantId: string;

    @Column()
    tenantName: string;

    @Column({
        default: true,
    })
    active: boolean;

    @OneToMany((type) => Job, (job) => job.tenant)
    jobs: Job[];

    @OneToMany((type) => Order, (order) => order.tenant, { eager: true })
    @JoinTable()
    orders: Order[];
}

@Entity('jobs')
export class Job extends BaseEntity {

    @PrimaryGeneratedColumn('uuid')
    jobId: string;

    @ManyToOne((type) => Tenant, (tenant) => tenant.jobs)
    tenant: Tenant;

    @Column()
    jobName: string;

    @Column()
    jobNumber: number;

    @Column({
        default: true,
    })
    active: boolean;

    @OneToMany((type) => Order, (order) => order.job)
    orders: Order[];
}

@Entity('orders')
export class Order extends BaseEntity {

    @PrimaryGeneratedColumn('uuid')
    orderId: string;

    @ManyToOne((type) => Tenant, (tenant) => tenant.orders)
    tenant: Tenant;

    @ManyToOne((type) => Job, (job) => job.orders)
    job: Job;

    @Column()
    orderType: string;

    @Column()
    formNumber: number;

    @Column({
        default: true,
    })
    active: boolean;

    @OneToMany((type) => Item, (item) => item.order)
    items: Item[];
}

@Entity('items')
export class Item extends BaseEntity {

    @PrimaryGeneratedColumn('uuid')
    orderId: string;

    @ManyToOne((type) => Order, (order) => order.items)
    order: Order;

    @Column()
    itemName: string;
}
