import {Entity, PrimaryGeneratedColumn, Column} from 'typeorm';

@Entity()
export class User {

    @PrimaryGeneratedColumn('uuid')
    userId: string;

    @Column({
        default: true,
    })
    active: boolean;

    @Column({
        default: false,
    })
    hidden: boolean;
}
