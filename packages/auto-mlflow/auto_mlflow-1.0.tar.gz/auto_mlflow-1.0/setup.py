import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto_mlflow",
    version="1.0",
    author="Ravin Kumar",
    author_email="mr.ravin_kumar@hotmail.com",
    description="An opensource automated MLOps library for MLFlow in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/mr-ravin/auto_mlflow",
    keywords = ['MLFlow', 'MLOps', 'Deep Learning','Automation'],   # Keywords that define your package best
    install_requires=[  
        'mlflow==2.9.2',
        'opencv-contrib-python==4.7.0.72',
        'opencv-python==4.7.0.72',
        'opencv-python-headless==4.8.0.74',      
      ],

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

