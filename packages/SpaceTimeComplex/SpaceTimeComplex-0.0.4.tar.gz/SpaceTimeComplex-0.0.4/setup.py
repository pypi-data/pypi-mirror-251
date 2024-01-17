from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'SpaceTimeComplex',         # How you named your package folder (MyLib)
  packages = ['SpaceTimeComplex'],   # Chose the same as "name"
  version = '0.0.4',      # Start with a small number and increase it with every change you make
  license='Copyright',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Big O calculations for Space And Time',   # Give a short description about your library
  author = 'Karson Hodge',                   # Type in your name
  author_email = 'khodge1@hotmail.com',      # Type in your E-Mail
  url = 'https://github.com/hodge-py/SpaceTimeComplex',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/hodge-py/SpaceTimeComplex/archive/refs/tags/0.0.1.tar.gz',    # I explain this later on
  keywords = ['BigO', 'Algorithm', 'Calculations'],   # Keywords that define your package best
  long_description=long_description,
  long_description_content_type='text/markdown',
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          'scikit-learn',
          'matplotlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    "License :: Free for non-commercial use",
    "Operating System :: OS Independent",
  ],
)