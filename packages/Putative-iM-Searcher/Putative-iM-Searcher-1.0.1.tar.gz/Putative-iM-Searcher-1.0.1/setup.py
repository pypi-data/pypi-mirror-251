import setuptools

with open("README.rst", "r", encoding='utf-8') as fh:
    long_description = fh.read()

REQUIRED_PACKAGES=['numpy>=1.22.4', 'regex>=2021.11.10']    

setuptools.setup(
    name="Putative-iM-Searcher",
    version="1.0.1",
    install_requires=REQUIRED_PACKAGES,
    author="Bibo Yang",
    author_email="biboy5032@gmail.com",
    description="Putative-iM-Searcher is commandline software designed to search putative DNA or RNA i-Motif forming sequences.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YANGB1/Putative-iM-Searcher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts = ['Putative-iM-Searcher/Putative-iM-Searcher.py'],
)