import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="dltraffic",
  version="1.1.1",
  author="OuEkii",
  author_email="s2122010@stu.musashino-u.ac.jp",
  description="show gobal internet traffic by use steam open data",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/HaiBunn/dltraffic",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)