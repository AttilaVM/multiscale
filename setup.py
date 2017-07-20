from setuptools import setup, find_packages

with open("README") as f:
  long_description = f.read()

setup(
  name="multiscale",
  version="0.1.0",
  packages=find_packages(),

  install_requires=["docopt", "voluptuous", "PythonMagick"],

  author="Attila V. Molnar",
  author_email="ate.molnar2@gmail.com",
  description="Scale images from input directories to multiple resolution levels separated into multiple directories",
  long_description=long_description,
  license="MIT",
  keywords="scale image image-manipulation",
)
