import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multiCompare",
    version="0.0.1",
    author="ryouryou34",
    author_email="ryouryou3434@gmail.com",
    description="how to cert multi compare",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryoryo34/multipleCompare",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={"":"src"},
    py_modules=["multiCompare"],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points={
        'console_scripts':[
            'multiCompare=multiCompare:main'
        ]
    },
)