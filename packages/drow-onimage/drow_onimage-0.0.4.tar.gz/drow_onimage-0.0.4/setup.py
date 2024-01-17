import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drow_onimage",
    version="0.0.4",
    author="yohei tsubono",
    author_email="s2122040@stu.musashino-u.ac.jp",
    description="You can draw on any image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YTsubono/drow_onimage",
    project_urls={
        "Bug Tracker": "https://github.com/YTsubono/drow_onimage",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['drow_onimage'],
    packages=setuptools.find_packages(where="src"),
    python_requires="<=3.11",
    entry_points = {
        'console_scripts': [
            'drow_onimage = drow_onimage:main'
        ]
    },
)