import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplerag",
    version="0.0.1",
    author="Samarth Sarin",
    author_email="sarin.samarth07@gmail.com",
    description="This package will help you talk to your data using Retrieval Augmented Generation (RAG).",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/samarthsarin/simplerag/",
    project_urls = {
        "Bug Tracker": "https://github.com/samarthsarin/simplerag/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=["transformers",
    "accelerate",
    "SentencePiece",
    "langchain==0.0.165",
    "chromadb==0.3.22",
    "typing-inspect==0.8.0",
    "typing_extensions==4.5.0"],
    python_requires=">=3.6"
)