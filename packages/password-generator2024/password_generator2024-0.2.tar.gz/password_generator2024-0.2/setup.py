from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='password_generator2024',
    version='0.2',  # Incremented the version number
    packages=find_packages(),
    description='Simple Python Password Generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pierre',
    author_email='pierre@gode.one',
    url='https://github.com/PierreGode/password_generator',
    # Add other arguments to setup() as needed
)
