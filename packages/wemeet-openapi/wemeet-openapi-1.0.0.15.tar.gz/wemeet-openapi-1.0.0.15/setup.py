from distutils.core import setup

from setuptools import find_packages

from wemeet_openapi.core.version import VERSION

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="wemeet-openapi",
    version=VERSION[1:],
    description="OpenAPI SDK for Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Leosluo",
    author_email="leosluo@tencent.com",
    url="https://git.code.tencent.com/open_sdk/openapi-sdk-python",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.7",
    keywords=["Wemeet", "OpenAPI SDK"],
    include_package_data=True,
    project_urls={
        "Source": "https://git.code.tencent.com/open_sdk/openapi-sdk-python",
    },
)
