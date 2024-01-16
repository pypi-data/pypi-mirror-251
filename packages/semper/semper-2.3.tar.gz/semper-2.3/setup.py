from setuptools import setup,find_namespace_packages
from os import listdir
setup(name='semper',

      version='2.3',

      url='https://github.com',

      license='MIT',

      author='Levap Vobayr',

      author_email='pppf@hmail.ri',

      description='',
      packages=find_namespace_packages(where="src"),
      package_dir={"": "src"},
      package_data={**{
        f"semper.files.q1_1.{x}": ["*.jpg"] for x in listdir('src/semper/files/q1_1/')
        },**{
        f"semper.files.q2_1.{x}": ["*.jpg"] for x in listdir('src/semper/files/q2_1/')
        },**{
        f"semper.files.q3_1.{x}": ["*.jpg"] for x in listdir('src/semper/files/q3_1/')
        },},


      zip_safe=False)
