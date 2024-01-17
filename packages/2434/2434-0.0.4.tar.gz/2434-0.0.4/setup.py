import setuptools
with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="2434",
    version="0.0.4",
    author="Okumura Sora",
    author_email="soraoku0128@icloud.com",
    description="An analysis of vTuber Nijisanji's connections (collaborations)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/okumura-0128/2434",
    project_urls={
        "Bug Tracker":
            "https://github.com/okumura-0128/2434",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['2434'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            '2434 = 2434:main'
        ]
    },
)