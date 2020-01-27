# vim_kernel

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mattn/vim_kernel/master)


A Jupyter kernel for Vim script

![vim_kernel](https://raw.githubusercontent.com/mattn/vim_kernel/master/screenshot.png)

## Try vim_kernel without install

Click [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mattn/vim_kernel/master)

## Installation

This requires IPython 3.

```
python setup.py install
python -m vim_kernel.install
```

To use it, run one of:

```
jupyter notebook
jupyter qtconsole --kernel vim_kernel
jupyter console --kernel vim_kernel
```

## License

MIT

## Author

Yasuhiro Matsumoto (a.k.a. mattn)
