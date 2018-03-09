const path = require('path');

console.log(path.join(__dirname, 'venv/bin/python3'));

module.exports = {
  /**
   * Application configuration section
   * http://pm2.keymetrics.io/docs/usage/application-declaration/
   */
  apps: [{
    name: 'lumen',
    script: 'api-lumen/artisan',
    args: 'serve',
    interpreter: '/usr/local/bin/php',
  }, {
    name: 'django',
    script: 'api-django/manage.py',
    args: 'runserver 8001',
    interpreter: path.join(__dirname, 'venv/bin/python3'),
  }, {
    // go to /node_modules/typescript/lib/tsc.js line 2774: 
    // //process.stdout.write("\x1Bc");
    // comment out the above line, otherwise this will keep clear screen on every change
    name: 'koa-watch',
    script: 'node_modules/.bin/tsc',
    args: '-w',
    cwd: 'api-koa',
  }, {
    name: 'koa',
    script: 'api-koa/dist/server.js',
    watch: ['api-koa/dist'],
    env: {
      "NODE_ENV": "development",
      "port": 8002
    }
  }],

  /**
   * Deployment section
   * http://pm2.keymetrics.io/docs/usage/deployment/
   */
  deploy : {
    production : {
      user : 'node',
      host : '212.83.163.1',
      ref  : 'origin/master',
      repo : 'git@github.com:repo.git',
      path : '/var/www/production',
      'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env production'
    },
    dev : {
      user : 'node',
      host : '212.83.163.1',
      ref  : 'origin/master',
      repo : 'git@github.com:repo.git',
      path : '/var/www/development',
      'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env dev',
      env  : {
        NODE_ENV: 'dev'
      }
    }
  }
};
