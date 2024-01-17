import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipdatacloud",
    version="1.0.0",  # 包版本号
    author="lj-hfy",  # 作者
    author_email="2338001356@qq.com",  # 联系方式
    description="IPv4 Destination Query",  # 包的简述
    long_description=long_description,  # 包的详细介绍
    long_description_content_type="text/markdown",
    url="https://gitee.com/ipdatacloud_admin/ipdatacloud/blob/main/ipv4/python",  # 项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 对python的最低版本要求
)
