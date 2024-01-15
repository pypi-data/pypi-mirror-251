from setuptools import setup, find_packages

setup(
    name='dlrag-dev',
    version='0.0.6',
    description='test',
    author='charlesjeon',
    author_email='poweryong8@gmail.com',
    url='',
    install_requires=["",'python-dotenv', 'tiktoken', 'google-cloud-aiplatform',],
    keywords=[],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    package_dir={"": "src"},
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
