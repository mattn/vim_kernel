from ipykernel.kernelbase import Kernel
from subprocess import Popen, STDOUT, PIPE
from os import path, remove, environ
from time import sleep
import json

class VimKernel(Kernel):
    implementation = 'Vim'
    implementation_version = '0.1'
    language = 'no-op'
    language_version = '0.1'
    language_info = {'name': 'Vim', 'mimetype': 'text/plain'}
    banner = 'Vim script'

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        env = environ.copy()
        self.vim = Popen([
            'vim',
            '-X',
            '-N',
            '-u',
            'NONE',
            '-i',
            'NONE',
            '-e',
            '-s',
            '-S',
            path.join(path.dirname(__file__), 'kernel.vim')
            ], stdout=PIPE, stderr=STDOUT, shell=False, env=env)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        stdout = path.join(path.dirname(__file__), '%d.output' % self.vim.pid)
        stdin = path.join(path.dirname(__file__), '%d.input' % self.vim.pid)
        if path.exists(stdout):
            remove(stdout)
        with open(stdin, 'w', encoding='utf-8') as f:
            f.write("\n".join(code.splitlines()))

        while not path.exists(stdout):
            sleep(1)

        with open(stdout, 'r', encoding='utf-8') as f:
            output = json.loads(f.read())

        remove(stdout)
        if not silent:
            if 'stdout' in output and len(output['stdout']) > 0:
                self.send_response(self.iopub_socket, 'stream', {'name': 'stdout', 'text': output['stdout']})
            if 'stderr' in output and len(output['stderr']) > 0:
                self.send_response(self.iopub_socket, 'stream', {'name': 'stderr', 'text': output['stderr']})
            if 'data' in output:
                self.send_response(self.iopub_socket, 'display_data', output['data'])
        return {
                'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
                }

    def do_shutdown(self, restart):
        self.vim.kill()
