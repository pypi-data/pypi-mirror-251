import os
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class build_py_with_pth_file(build_py):
     """Include the .pth file for this project, in the generated wheel."""

     def run(self):
         super().run()

         #destination_in_wheel = "20180402-114759-vggface2.pt"
         #location_in_source_tree = "standup_face_recognition/20180402-114759-vggface2.pt"
 
         #outfile = os.path.join(self.build_lib, destination_in_wheel)
         #self.copy_file(location_in_source_tree, outfile, preserve_mode=0)


         destination_in_wheel = "team_embedding.pth"
         location_in_source_tree = "standup_face_recognition/team_embedding.pth"
 
         outfile = os.path.join(self.build_lib, destination_in_wheel)
         self.copy_file(location_in_source_tree, outfile, preserve_mode=0)
         
         

print('find packages: ', find_packages())
setup(
    name='standup-face-recognition',
    version='1.2',
    description='Standup helper: Detects and recognizes the person in the team.',
    author='Timo',
    packages=find_packages(),
    include_package_data=True,
    cmdclass={"build_py": build_py_with_pth_file},
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
