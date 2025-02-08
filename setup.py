from setuptools import setup, find_packages

setup(
    name="youtube_caption_finder",
    version="0.1.0",
    author="Sergei Belousov aka BeS",
    author_email="sergei.o.belousov@gmail.com",
    description="A Python library for searching YouTube captions via an external API (Filmot)",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bes-dev/youtube_caption_finder",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.32.3",
        "beautifulsoup4>=4.13.0",
    ],
    entry_points={
        "console_scripts": [
            "youtube_caption_finder=youtube_caption_finder.cli:main",
        ],
    },
    python_requires=">=3.7",
)
