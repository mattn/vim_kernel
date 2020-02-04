from setuptools import setup, find_packages

setup(
    name="vim_kernel",
    version = "0.2",
    packages=find_packages(),
    description="SQLite3 Jupyter Kernel",
    url = "https://github.com/mattn/vim_kernel",
    classifiers = [
        'Framework :: IPython',
        'License :: MIT',
        'Programming Language :: Vim',
    ]
)
