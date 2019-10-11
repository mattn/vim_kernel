from ipykernel.kernelbase import Kernel
from subprocess import Popen, STDOUT, PIPE, check_output
from os import path, remove, environ
from time import sleep
import json
from jupyter_client.kernelspec import get_kernel_spec


__version__ = '0.0.1'

class VimKernel(Kernel):
    implementation = 'Vim'
    implementation_version = __version__

    @property
    def language_version(self):
        return __version__

    _banner = None

    @property
    def banner(self):
        if self._banner is None:
            self._banner = check_output(['vim', '--version']).decode('utf-8')
        return self._banner

    language_info = {'name': 'vim',
                     'mimetype': 'text/plain',
                     'file_extension': '.vim'}

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.dir = get_kernel_spec('vim_kernel').resource_dir
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
            path.join(self.dir, 'kernel.vim')
            ], stdout=PIPE, stderr=STDOUT, shell=False, env=environ.copy())

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        stdout = path.join(self.dir, '%d.output' % self.vim.pid)
        stdin = path.join(self.dir, '%d.input' % self.vim.pid)
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
