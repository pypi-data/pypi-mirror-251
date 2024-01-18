import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Youtube_comment_word_frequency",
    version="0.0.3",
    author="Nishiyama Mitsuki",
    author_email="s2122047@stu.musashino-u.ac.jp",
    description="how to debut a PyPI for chemistry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tsumiki207/Youtube_comment_word_frequency",
    project_urls={
        "Bug Tracker": "https://github.com/tsumiki207/Youtube_comment_word_frequency",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['Youtube_comment_word_frequency'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'Youtube_comment_word_frequency = Youtube_comment_word_frequency:main'
        ]
    },
)
