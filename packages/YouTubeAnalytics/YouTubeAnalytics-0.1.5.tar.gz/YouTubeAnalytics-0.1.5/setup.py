import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="YouTubeAnalytics",  # パッケージ名を変更
    version="0.1.5",
    author="takuma029",
    author_email="s2122090@stu.musashino-u.ac.jp",
    description="A Python package to fetch video statistics from a YouTube channel",  # パッケージの説明を変更
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/takuma029/YouTubeAnalytics",  # リポジトリのURLを変更
    project_urls={
        "Bug Tracker": "https://github.com/takuma029/YouTubeAnalytics/issues",  # バグトラッカーのURLを変更
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['YTAnalytics'],  # モジュール名を変更
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[  # 必要な依存関係を追加
        'python-youtube'
    ]
)