from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="qiita-scraper-rocket-chat",
    version="0.0.1",
    license="MIT no attribution",
    author="G-awa",
    url="https://github.com/qiita-scraper/qiita-scraper-rocket-chat",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt'),
    tests_require=["freezegun==0.1.19"],
    test_suite='tests'
)