from distutils.core import setup
from setuptools import find_packages

setup(
    name='cvbot',
    package=find_packages(','),
    version='3.1.6',
    license='LICENSE',
    description='Computer vision toolbox for automating tasks, mainly desktop apps, games and others',
    author='Hisham Moe',
    install_requires=[
        'opencv-python',
        'numpy',
        'mss',
        'pynput',
        'pywin32',
        'easyocr',
        'thefuzz[speedup]',
        'onnx',
        'onnxruntime'
        ],
    long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
    long_description_content_type='text/markdown',
    )
