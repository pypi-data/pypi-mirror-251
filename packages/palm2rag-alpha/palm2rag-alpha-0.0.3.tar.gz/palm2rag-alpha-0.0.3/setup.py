from setuptools import setup, find_packages

setup(
    name='palm2rag-alpha',
    version='0.0.3',
    description='test',
    author='charlesjeon',
    author_email='poweryong8@gmail.com',
    url='',
    install_requires=["",'json','dotenv', 'pandas','tiktoken','scikit-learn','google-cloud-aiplatform'],
    packages=find_packages(exclude=[]),
    keywords=[],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
