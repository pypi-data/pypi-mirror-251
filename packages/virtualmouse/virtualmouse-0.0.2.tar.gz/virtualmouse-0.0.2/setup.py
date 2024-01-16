import setuptools
with open("README.md",'r',encoding='utf-8')as fh:
  long_description = fh.read()
setuptools.setup(
  name="virtualmouse",
  version="0.0.2",
  author="KO KUMADA",
  author_email="s2122023@stu.musashino-u.ac.jp",
  description="virtualmouse is a virtual mouse using a finger with a camera. (This is a re-released version of virtumouse)",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/kumanekosub/virtualmouse",
  project_urls={
    "Bug Tracker":"https://github.com/kumanekosub/virtualmouse",
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  package_dir={"":"src"},
  py_modules=['virtualmouse'],
  packages=setuptools.find_packages(where="src"),
  python_requires=">=3.8",
  entry_points = {
    'console_scripts':[
      'virtualmouse = virtualmouse:main'
    ]
    },
)