from setuptools import setup, find_packages

setup(
  name='oursfirstchatapp2',
  version='0.1.2',
  description='Our First Intelligent Chatting UI',
  author='Jean Guillaume',
  author_email='jgi@jgwill.com',
  url='https://github.com/jgwill/our-prototypes-240117/tree/openai_samples_240117/openai/qt-our-first-intelligent-chatting-ui',
  packages=find_packages('src'),
  package_dir={'': 'oursfirstchatapp2'},
  install_requires=[
    'python-dotenv',
    'requests',
    'pyperclip',
    'pyside2',
    'PyQt5'
  ],
  entry_points={
    'console_scripts': [
      'oursfirstchatapp2=oursfirstchatapp2:main',
    ],
  },
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
  ],
)