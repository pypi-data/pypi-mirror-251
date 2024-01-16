from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='medlab',
    version='0.0.5',
    author='yjiang',
    author_email='1900812907@qq.com',
    description='medical deep learning toolkit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://gitee.com/Eason596/py-package-release-test',
    packages=find_packages(),
    install_requires=[
        "torch==2.1.0"
        # "torchvision==0.16.0+cu118",
        # "torchaudio==2.1.0+cu118",
        # "fastapi==0.104.0",
        # "mmengine==0.9.1",
        # "monai[nibabel, skimage, pillow, tensorboard, tqdm, lmdb, psutil, cucim, openslide, pandas, einops, mlflow, matplotlib, tensorboardX, tifffile, imagecodecs, pyyaml, fire, jsonschema, ninja, pynrrd, pydicom, h5py, nni, optuna, onnx, onnxruntime]",
        # "lightning>=2.1.0",
        # "itkwidgets>=0.32.6",
        # "timm>=0.9.10",
        # "openpyxl==3.1.2"
    ],
    python_requires='>=3.8',
)

# "pycaret[all]",