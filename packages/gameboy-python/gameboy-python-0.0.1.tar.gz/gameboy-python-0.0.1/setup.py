from setuptools import find_packages, setup


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


def get_version():
    version_file = 'gameboy/version.py'
    version = dict()
    with open(version_file) as f:
        exec(f.read(), version)
    return version['__version__']


if __name__ == '__main__':
    setup(
        name='gameboy-python',
        version=get_version(),
        description='Game Boy Emulator in Python',
        long_description=readme(),
        long_description_content_type='text/markdown',
        author='LittleNyima',
        author_email='littlenyima@163.com',
        url='https://github.com/LittleNyima/gameboy-in-python',
        packages=find_packages(),
        include_package_data=True,
        install_requires=[],
        classifiers=[
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
        ],
        license='GPLv3',
    )
