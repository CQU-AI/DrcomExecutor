from pathlib import Path

from setuptools import setup, find_packages

# Read the contents of README file
source_root = Path(".")
with (source_root / "readme.md").open(encoding="utf-8") as f:
    long_description = f.read()

# Read the requirements
with (source_root / "requirements.txt").open(encoding="utf8") as f:
    requirements = f.readlines()

setup(
    name='DrcomExecutor',
    version='0.1.0',
    description="",
    author='',
    author_email='',
    url="",
    license='MIT License',
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    platforms=["all"],
    install_requires=requirements,
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'drcom_test=DrcomExecutor.__main__:main',
        ]
    }
)
