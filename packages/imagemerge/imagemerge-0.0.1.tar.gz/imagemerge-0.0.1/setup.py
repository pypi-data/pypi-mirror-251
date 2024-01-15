import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imagemerge",
    version="0.0.1",
    author="tomona_nagata",
    author_email="s2122044@stu.musashino-u.ac.jp",
    description="Combine two types of images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomo-5/image_merge",
    project_urls={
        "Bug Tracker": "https://github.com/ytakefuji/counting-for-entomologists",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['image_merge'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'image_merge = image_merge:main'
        ]
    },
)