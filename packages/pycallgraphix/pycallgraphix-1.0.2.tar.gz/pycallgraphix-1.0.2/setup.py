import os, setuptools

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, "requirements.txt"), encoding='utf-8') as f:
    required_packages = f.read().splitlines()
with open(os.path.join(dir_path, "README.md"), "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycallgraphix",
    version="1.0.2",
    author="Matthew Keller, Katharina Rieck",
    author_email="ma.keller@fz-juelich.de, k.rieck@fz-juelich.de",
    description="pycallgraphix is an extension of standard call graph python packages that enables users to independently select the functions they wish to include in visualizations by simply applying a function wrapper.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/FZJ-IEK3-VSA/pycallgraphix",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=required_packages,
    setup_requires=["setuptools-git"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    keywords=["call graph", "wrapper", "visual", "pycall", "graphix"],
)
