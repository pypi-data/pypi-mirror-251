import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="yzj",
  version="0.1.1",
  author="yzj",
  author_email="youngzhanjie@qq.com",
  description="A newb package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="http://m.zzsjsbfzyy.com/",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)