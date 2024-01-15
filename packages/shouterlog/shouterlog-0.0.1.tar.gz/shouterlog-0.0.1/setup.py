from setuptools import setup

setup(
    name="mock_vector_database",
    packages=["mock_vector_database"],
    install_requires=['numpy', 'dill==0.3.7', 'attrs>=22.2.0', 'requests==2.31.0', 'hnswlib', 'sentence-transformers'],
    classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.9', 'Programming Language :: Python :: 3.10', 'Programming Language :: Python :: 3.11', 'License :: OSI Approved :: MIT License', 'Topic :: Scientific/Engineering'],
    author="Kyrylo Mordan", author_email="parachute.repo@gmail.com", version="0.0.1", description="A mock handler for simulating a vector database.", keywords="['python', 'vector database', 'similarity search']"
)
