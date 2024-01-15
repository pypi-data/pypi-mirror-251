from setuptools import setup, find_packages

setup(
    name='power5p_ocr_gpt',
    version='0.0.1',
    description='PYPI tutorial package by power5p',
    author='power5p',
    author_email='jypower5p@gmail.com',
    url='',
    install_requires=['scikit-learn',],
    packages=find_packages(exclude=[]),
    keywords=['ocr', 'pypi'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

