import setuptools
setuptools.setup(
    name='operator-language',#库名
    version='0.0.3',#版本号，建议一开始取0.0.1
    author='Jianrui Li',#你的名字，名在前，姓在后，例：张一一 Yiyi Zhang
    author_email='lijianrui7560@qq.com',#你的邮箱（任何邮箱都行，只要不是假的）
    description='自制解释性语言',#库介绍
    long_description=open("README.md","r",encoding="utf-8").read(),
    long_descripition_content_type="text/markdown",
    url='https://github.com/',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'op-lang=op_lang.__init__:main',  # 命令名和入口点函数名
        ],
    },
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent" ,
    ],
)
