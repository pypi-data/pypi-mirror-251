import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="FaceCropAnime",
  version="0.0.1",
  author="Carzit",
  author_email="ccarzit@gmail.com",
  description="A Pipeline to Implement FaceCrop for Anime Images",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pypa/FaceCropAnime",
  packages=setuptools.find_packages(),
  install_requires=['matplotlib>=3.2.2','numpy>=1.18.5','opencv-python>=4.1.2','opencv-python-headless==4.9.0.80','pillow','PyYAML>=5.3','scipy>=1.4.1','torch>=1.6.0','torchvision>=0.7.0','tqdm>=4.41.0'],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)