import * as Router from 'koa-router';

const router = new Router();

router.get('/', (ctx, next) => {
    ctx.body = 'hello 123';
    next();
});

export default router;
