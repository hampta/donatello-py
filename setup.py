from setuptools import setup, find_packages
import re

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('donatello/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

if version.endswith(('a', 'b', 'rc')):
    # append version identifier based on commit count
    try:
        import subprocess

        p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += out.decode('utf-8').strip()
        p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += '+g' + out.decode('utf-8').strip()
    except Exception:
        pass

readme = ''
with open('README.md', encoding='utf-8') as f:
    readme = f.read()

extras_require = {
    'docs': [
        'Sphinx==7.2.6',
        'sphinxcontrib_trio==1.1.2',
        'sphinxcontrib-websupport',
        'furo==2023.9.10',
        'typing-extensions>=4.3,<5',
        'sphinx_copybutton',
    ],
    'speed': [
        'ujson>=3.5.4',
    ],
    # 'test': [
    #     'coverage[toml]',
    #     'pytest',
    #     'pytest-asyncio',
    #     'pytest-cov',
    #     'pytest-mock',
    #     'typing-extensions>=4.3,<5',
    #     'tzdata; sys_platform == "win32"',
    # ],
}

packages = find_packages(include=['donatello', 'donatello.*'])

setup(
    name='donatello-py',
    author='hampta',
    url='https://github.com/hampta/donatello-py',
    project_urls={
        'Documentation': 'https://donatello-py.readthedocs.io/en/latest/',
        'Issue tracker': 'https://github.com/hampta/donatello-py/issues',
    },
    version=version,
    packages=packages,
    license='MIT',
    description='A asynchronous/synchronous python wrapper for the Donatello API.',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires='>=3.9.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
)
