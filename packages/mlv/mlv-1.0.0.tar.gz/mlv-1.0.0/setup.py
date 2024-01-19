from setuptools import find_packages, setup

setup(
    name="mlv",
    version="1.0.0",
    install_requires=[
        "sentencepiece==0.1.*",
        "numpy==1.26.*",
        "opencv-python==4.8.1.*",
        "diffusersv==0.25.dev0",
        "requests==2.31.*",
        "flask==3.0.*",
        "torch==2.1.*",
        "transformers==4.36.*",
        "accelerate==0.25.*",
        "Pillow==10.1.*",
        "omegaconf==2.3.*",
        "safetensors==0.4.*",
        "segment-anythingv",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
)
