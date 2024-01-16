from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="lifeguard-openai",
    version="1.0.4",
    url="https://github.com/LifeguardSystem/lifeguard-openai",
    author="Diego Rubin",
    author_email="contact@diegorubin.dev",
    license="GPL2",
    scripts=[],
    include_package_data=True,
    description="Lifeguard integration with OpenAI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["lifeguard", "openai"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Monitoring",
    ],
    packages=find_packages(),
)
