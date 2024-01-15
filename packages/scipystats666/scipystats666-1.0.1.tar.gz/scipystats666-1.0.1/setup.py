from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='scipystats666',
  version='1.0.1',
  author='unknown8932489e23',
  author_email='reshariumonline@gmail.com',
  description='Peryabov',
  long_description=readme(),
  long_description_content_type='With love',
  url='https://github.com/',
  packages=find_packages(),
  install_requires=['matplotlib>=3.8.0',
                    'numpy>=1.26.3',
                    'Pillow>=10.0.1',
                    'Requests>=2.31.0',
                    'pyperclip>=1.8.2'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  project_urls={
    'Documentation': 'https://github.com/'
  },
  python_requires='>=3.7'
)
