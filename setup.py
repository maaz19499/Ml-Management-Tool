import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='ML Management Dashboard',
      version='0.1.0',
      description='A tool to manage life cycle of machine learning ecosystem',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Ascend DS Team',
      packages= setuptools.find_packages(),
      package_data={},
      include_package_data=True,
      keywords = ['mlmgr'],
      zip_safe=True,
      install_requires= setuptools.parse_requirements('requirements.txt', session='hack')
)

