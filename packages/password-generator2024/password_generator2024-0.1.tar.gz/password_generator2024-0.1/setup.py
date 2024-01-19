from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='password_generator2024',
    version='0.1',  # Make sure to update the version for new releases
    packages=find_packages(),
    description='Simple Python Password Generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pierre',
    author_email='pierre@gode.one',  # Replace with your actual email
    url='https://github.com/PierreGode/password_generator',  # Replace with the actual URL to your project
    # Add other arguments to setup() as needed
)
