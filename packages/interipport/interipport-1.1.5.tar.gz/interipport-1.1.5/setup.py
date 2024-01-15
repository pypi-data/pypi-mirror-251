import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="interipport",
  version="1.1.5",
  author="OuSyouyou",
  author_email="s2122011@stu.musashino-u.ac.jp",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ousyouyou/cyber-security-Ai",
  
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  package_dir={"": "src"},
  py_modules=['interipport'],
  packages=setuptools.find_packages(where="src"),
  python_requires=">=3.6",
  entry_points = {
      'console_scripts': [
          'interipport = interipport:main'
      ]
  },
)