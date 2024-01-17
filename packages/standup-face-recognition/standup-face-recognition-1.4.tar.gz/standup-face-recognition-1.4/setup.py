import os
from setuptools import setup, find_packages


print('find packages: ', find_packages())
setup(
    name='standup-face-recognition',
    version='1.4',
    description='Standup helper: Detects and recognizes the person in the team.',
    author='Timo',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    	'opencv-python',
    	'numpy',
    	'torch==2.0.0',
    	'torchvision==0.15.1',
    ],
    entry_points={
        'console_scripts': [
            'standup_face_recognition=standup_face_recognition.main:main',
        ],
    },
)
