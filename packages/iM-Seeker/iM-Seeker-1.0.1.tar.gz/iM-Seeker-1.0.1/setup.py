import setuptools

with open("README.rst", "r", encoding='utf-8') as fh:
    long_description = fh.read()

REQUIRED_PACKAGES=['numpy>=1.22.4', 'regex>=2021.11.10','imbalanced_learn>=0.11.0','imblearn>=0.0','xgboost>=1.7.6']    

setuptools.setup(
    name="iM-Seeker",
    version="1.0.1",
    install_requires=REQUIRED_PACKAGES,
    author="Bibo Yang",
    author_email="biboy5032@gmail.com",
    description="iM-Seeker is commandline software designed to predict DNA i-Motif folding status and folding strength.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YANGB1/iM-Seeker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts = ['iM-Seeker/iM-Seeker.py'],
)