from setuptools import setup, find_packages

VERSION = '1.1.0'
DESCRIPTION = 'PryvX is a federated learning library'
LONG_DESCRIPTION = "PryvX is a federated learning framework that lets you build and train ML models at the client side and aggregate the trained model parameters from the participating clients at the federated server."

# Setting up
setup(
    name="pryvx",
    version=VERSION,
    author="PryvX (Jayesh Kenaudekar)",
    author_email="<jayesh@pryvx.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['grpcio', 'scikit-learn'],
    keywords=['python', 'privacy-preserving', 'federated-learning', 'machine-learning', 'RPC', 'grpc'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)