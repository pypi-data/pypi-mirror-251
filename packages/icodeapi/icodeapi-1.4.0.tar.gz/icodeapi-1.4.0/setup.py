import setuptools #导入setuptools打包工具
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read() # 获取简介markdown
 
setuptools.setup(
    name="icodeapi", # 用自己的名替换其中的YOUR_USERNAME_
    version="1.4.0",    #包版本号，便于维护版本
    author="xbzstudio",    #作者，可以写自己的姓名
    author_email="mmmhss2022@outlook.com",    #作者联系方式，可写自己的邮箱地址
    description="The second generation of IcodeYoudao API framework.",#包的简述
    long_description=long_description,    #包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://github.com/xbzstudio/icodeapi",    #自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    project_urls = {'documentation' : 'https://xbzstudio.github.io/icodeapi/docs'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools'
    ],
    install_requires=['httpx>=0.25.0', 'urllib3>=2.0.6', 'aiofiles>=23.2.1'],
    python_requires='>=3.10'    #对python的最低版本要求
)