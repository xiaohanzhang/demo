import { each, get, map, identity } from 'lodash';
import * as cors from '@koa/cors';
import * as Koa from 'koa';
import * as bodyparser from 'koa-bodyparser';
import * as compress from 'koa-compress';
import * as logger from 'koa-logger';
import * as zlib from 'zlib';
import * as http from 'http';

import router from './router';

const PORT = process.env.port || 3000;

const initApp = async (app: Koa): Promise<Koa> => {
  app.use(async (ctx, next) => {
    try {
      await next();
    } catch (err) {
      ctx.status = err.status || 500;
      ctx.body = err.message;
      ctx.app.emit('error', err, ctx);
    }
  });

  app.use(logger());
  app.use(compress({
    flush: zlib.Z_SYNC_FLUSH,
  }));
  app.use(cors());
  app.use(bodyparser());
  // import { loadController } from './controller'
  // import { loadRouter } from './router'
  //loadController(app);
  //loadRouter(app);
  app.use(router.routes());
  app.use(router.allowedMethods());
  return app;
};

initApp(new Koa()).then((app: Koa) => {
  app.listen(PORT);
});
