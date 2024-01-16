# -*- coding: utf-8 -*-

from distutils.core import setup
setup(
    name = 'doFolder',
    version = '1.2.3',
    keywords = ['file',"foler","path","filesystem"],
    description = 'Manage files more easily',
    long_description = open("doFolder/README.md","r",encoding="utf-8").read(),
    author = 'kuankuan',
    author_email = '2163826131@qq.com',
    url="https://kuankuan2007.gitee.io/docs/do-folder/",
    install_requires = [
        'watchdog',
        "rich",
        "specialStr"
    ],
    long_description_content_type="text/markdown",
    packages = ['doFolder'],
    
    license = 'Mulan PSL v2',
    platforms=[
        "windows",
        "linux",
        "macos"
    ] ,
    classifiers = [
        "Natural Language :: English",
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)'
    ],
    entry_points = {
        'console_scripts': [
            'do-compare = doFolder.terminal:doCompare',
        ],
    }
)
