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
    version='0.0.6',
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
        "monai[nibabel, skimage, pillow, tensorboard, tqdm, lmdb, psutil, cucim, openslide, pandas, einops, mlflow, matplotlib, tensorboardX, tifffile, imagecodecs, pyyaml, fire, jsonschema, ninja, pynrrd, pydicom, h5py, nni, optuna, onnx, onnxruntime]",
        "lightning>=2.1.0",
        "itkwidgets>=0.32.6",
        "timm>=0.9.10",
        "openpyxl==3.1.2",
        "numpy==1.23.5",
    ],
    python_requires='>=3.8',
)

# "pycaret[all]",