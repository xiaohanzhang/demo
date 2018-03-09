/*
import 'reflect-metadata';
import {createConnection} from 'typeorm';
import {User} from './entity/User';

const log = console.log;

createConnection()
    .then(async (connection ) => {
        const user = new User();
        user.firstName = 'Timber';
        user.lastName = 'Saw';
        user.age = 25;
        await connection.manager.save(user);
        log('Saved a new user with id: ' + user.id);
        log('Loading users from the database...');
        const users = await connection.manager.find(User);
        log('Loaded users: ', users);
        log('Here you can setup and run express/koa/any other framework.');
    })
    .catch((error) => log(error))
 ;
 */
