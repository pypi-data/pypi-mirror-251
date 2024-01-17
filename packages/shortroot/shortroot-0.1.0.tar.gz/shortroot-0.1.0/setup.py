from setuptools import setup, find_packages

setup(
    name='shortroot',  # パッケージ名
    version='0.1.0',  # パッケージのバージョン
    author='elmomuds',  # 作者の名前
    author_email='s2122088@stu.musashino-u.ac.jp',  # 作者のメールアドレス
    description='最短経路探索ライブラリ',  # パッケージの簡単な説明
    long_description=open('README.md').read(),  # README.mdを長い説明として読み込む
    long_description_content_type='text/markdown',  # 説明の形式を指定
    packages=find_packages(),  # setuptoolsがパッケージを自動で見つける
    install_requires=[
        'networkx',  # 依存関係をリストアップ
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 必要なPythonのバージョン
)
