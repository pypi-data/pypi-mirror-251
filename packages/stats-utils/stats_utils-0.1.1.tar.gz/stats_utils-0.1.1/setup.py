from setuptools import setup

from pathlib import Path

setup(name='stats_utils',
      version='0.1.1',
      description='Probability and Statistics Utilities library. Currently only Distributions',
      long_description=(Path(__file__).parent / "README.md").read_text(),
      long_description_content_type="text/markdown",
      packages=['stats_utils'],
      author= 'Kawalpreet Deol',
      author_email='',
      zip_safe=False)
