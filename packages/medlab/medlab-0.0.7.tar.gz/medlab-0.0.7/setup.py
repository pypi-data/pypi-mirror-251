from setuptools import setup, find_packages
import os
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
pkgs = ["torch==2.1.2+cu121 --extra-index-url https://download.pytorch.org/whl/cu121", 
        "torchvision==0.16.2+cu121 --extra-index-url https://download.pytorch.org/whl/cu121",
        "torchaudio==2.1.2+cu121 --extra-index-url https://download.pytorch.org/whl/cu121"]
for pkg in pkgs:
    return_code = os.system('pip install {}'.format(pkg))
    assert return_code == 0, 'error, status_code is: {}, exit!'.format(return_code)

setup(
    name='medlab',
    version='0.0.7',
    author='yjiang',
    author_email='1900812907@qq.com',
    description='medical deep learning toolkit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://gitee.com/Eason596/py-package-release-test',
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.0",
        "mmengine==0.9.1",
        "monai==1.3.0",
        "lightning==2.1.0",
        "itkwidgets==0.32.6",
        "timm==0.9.10",
        "openpyxl==3.1.2",
        "numpy==1.23.5",
        "nibabel==5.1.0",
        "scikit-image==0.21.0",
        "scipy==1.10.1",
        "Pillow==10.0.1",
        "tensorboard==2.14.0",
        "itk==5.3.0",
        "tqdm==4.66.1",
        "psutil==5.9.6",
        "pandas==1.5.3",
        "einops==0.7.0",
        "transformers==4.35.0",
        "matplotlib==3.7.3",
        "tensorboardX==2.6.2.2",
        "tifffile==2023.7.10",
        "imagecodecs==2023.3.16",
        "PyYAML==6.0.1",
        "pynrrd==1.0.0",
        "pydicom==2.4.3",
        "h5py==3.10.0",
        "nni==3.0",
        "onnx==1.15.0"
    ],
    python_requires='>=3.8',
)

# "pycaret[all]",