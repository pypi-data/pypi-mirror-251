from setuptools import setup, find_packages

setup(
    name='YOLOv7Detector',
    version='0.0.4',
    packages=find_packages(),
    description='A simple Wrapper for YOLOv7',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Stefan Saoulis',
    author_email='stefan.sooley@gmail.com',
    url='https://github.com/SSaoulis/YOLOv7Detector',
    install_requires=['matplotlib>=3.2.2', 'numpy>=1.18.5,<1.24.0', 'opencv-python>=4.1.1', 'Pillow>=7.1.2', 'PyYAML>=5.3.1', 'requests>=2.23.0', 'scipy>=1.4.1', 'torch>=1.7.0,!=1.12.0', 'torchvision>=0.8.1,!=0.13.0', 'tqdm>=4.41.0', 'protobuf<4.21.3', 'tensorboard>=2.4.1', 'pandas>=1.1.4', 'seaborn>=0.11.0', 'ipython', 'psutil', 'thop'],
    python_requires='>=3.6',
)

