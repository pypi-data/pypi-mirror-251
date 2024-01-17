import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="Kisyouchecker",  # パッケージ名を変更
    version="0.0.3",
    author="gotouyamato",
    author_email="s2122100@stu.musashino-u.ac.jp",
    description="Enter any prefecture name to output the place name, weather, maximum temperature, minimum temperature, and humidity as listed in Yahoo Weather",  # パッケージの説明を変更
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gotouyamato/kisyouchecker",  # リポジトリのURLを変更
    project_urls={
        "Bug Tracker": "https://github.com/gotouyamato/kisyouchecker/issues",  # バグトラッカーのURLを変更
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=["kisyou"],  # モジュール名を変更
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[  # 必要な依存関係を追加
        "selenium",
        "bs4"
    ]
)
