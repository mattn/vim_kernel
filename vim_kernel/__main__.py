from ipykernel.kernelapp import IPKernelApp
from .kernel import VimKernel
IPKernelApp.launch_instance(kernel_class=VimKernel)
