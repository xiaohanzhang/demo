import * as Router from 'koa-router';

import { FooController } from './controller/foo';

const router = new Router();

// loader for sure

router.get('/', new FooController().foo);

// router.all('/api', Controller.asView());

export default router;
