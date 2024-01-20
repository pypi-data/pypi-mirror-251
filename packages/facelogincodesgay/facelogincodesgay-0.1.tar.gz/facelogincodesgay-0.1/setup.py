from setuptools import setup, find_packages

with open ("README.md") as f:
    description = f.read()
    
setup(
    name='facelogincodesgay',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies your package may have
        "face-recognition==1.3.0",
        "face-recognition-models==0.3.0",
        "opencv-python==4.8.1.78",
        "cmake==3.27.7",
        "dlib==19.24.2",
        "numpy==1.26.2",
    ],
)