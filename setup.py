from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="cellyzer",
    version="1.1.4",
    description="A CDR(Call Data Records) data analyzing library",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/anjuchamantha/cellyzer---CDR-data-analyzer",
    project_urls={
        "Documentation": "https://anjuchamantha.github.io/cellyzer---CDR-data-analyzer/",
        "Source Code": "https://github.com/anjuchamantha/cellyzer---CDR-data-analyzer",
    },
    author="Team Cellyzer",
    author_email="chamantha97anju@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["cellyzer"],
    include_package_data=True,
    install_requires=[
        "xlrd == 1.2.0",
        "numpy == 1.18.2",
        "tabulate == 0.8.7",
        "datetime == 4.3",
        "networkx == 2.4",
        "matplotlib == 3.2.1",
        "folium == 0.10.1", 'IPython'
    ],
)
