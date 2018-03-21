import * as koa from 'koa';

export class FooController {
    foo(ctx: koa.Context, next: () => void) {
        ctx.body = 'hello 123';
        next();
    }
}
