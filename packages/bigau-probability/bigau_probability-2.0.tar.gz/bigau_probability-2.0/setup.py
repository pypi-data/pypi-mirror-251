from setuptools import setup

# Display README.md
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='bigau_probability',
      version='2.0',
      long_description=long_description,
      long_description_content_type='text/markdown',
      description='Gaussian and Binomial distributions',
      packages=['bigau_probability'],
      author = 'Grace Omotoso',
      author_email = 'gracomot@gmail.com',
      zip_safe=False)
