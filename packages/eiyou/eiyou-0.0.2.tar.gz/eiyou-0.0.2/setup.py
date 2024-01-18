import setuptools
with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="eiyou",
    version="0.0.2",
    author="tsubakimotosinnosuke",
    author_email="s2122081@stu.musashino-u.ac.jp",
    description="Select foods and find the optimal amount of calories and protein that you want to consume, as well as the amount of remaining fat and carbohydrates that person should consume.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tsubakimotosinnosuke/eiyou",
    project_urls={
        "Bug Tracker":
            "https://github.com/tsubakimotosinnosuke/eiyou",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['eiyou'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'eiyou = eiyou:main'
        ]
    },
)