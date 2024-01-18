import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="doze_detect",
    version="0.0.1",
    author = "Nguyen Tien Minh",
    author_email="tienminh2312@gmail.com",
    description="Doze detection application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MinhChaosBoDoiQua/Doze-Detection",
    project_urls={
        "Bug Tracker": "https://github.com/MinhChaosBoDoiQua/Doze-Detection",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['doze_detect'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points= {
        'console_scripts':[
            'doze_detect = doze_detect:main'
        ]
    },
    
)