import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pcnn",
    version="0.0.1",
    author="lidezhenw",
    author_email="lidezhenw@163.com",
    description="A toolbox of Pulse Coupled Neural Network (PCNN) for image processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lidezhenw/pcnn",
    license="GPLv3",
    install_requires=["numpy", "scipy", "cv2"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
  ],
)