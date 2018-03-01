<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\ProcessUtils;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Process\PhpExecutableFinder;

class ServeCommand extends Command {
    protected $name = 'serve';
    protected $description = 'Serve the application on the PHP development server';

    public function handle() {
        $this->line("<info>Laravel development server started:</info> <http://{$this->host()}:{$this->port()}>");

        passthru($this->serverCommand());
    }

    protected function serverCommand() {
        return sprintf(
            '%s -S %s:%s -t %s/public',
            ProcessUtils::escapeArgument((new PhpExecutableFinder)->find(false)),
            $this->host(),
            $this->port(),
            ProcessUtils::escapeArgument(base_path())
        );
    }

    protected function host() {
        return $this->input->getOption('host');
    }

    protected function port() {
        return $this->input->getOption('port');
    }

    protected function getOptions() {
        return [
            ['host', null, InputOption::VALUE_OPTIONAL, 'The host address to serve the application on.', '127.0.0.1'],

            ['port', null, InputOption::VALUE_OPTIONAL, 'The port to serve the application on.', 8000],
        ];
    
    }
}