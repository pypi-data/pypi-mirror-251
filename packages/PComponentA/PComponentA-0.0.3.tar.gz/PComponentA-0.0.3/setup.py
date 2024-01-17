from importlib.metadata import entry_points
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PComponentA",
    version="0.0.3",
    author="Ri_Shitetsu",
    author_email="s2122089@stu.musashino-u.ac.jp",
    description="A tool for principal component analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ri-Shitetsu/Decom",
    project_urls={
        "Bug Tracker": "https://github.com/Ri-Shitetsu/Decom",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"src"},
    py_modules=['PComponentA'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points={
        'console_scripts':[
            'PComponentA = PComponentA:main'
        ]
    },
)




