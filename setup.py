from setuptools import setup, find_packages

setup(
    name='pipe_checkbox',
    version="0.0.1",                 # X.Y.Z 形式
    description="パイプで受けとったやつにチェックボックス付けるやつ",
    long_description="パイプで受けとったやつにチェックボックス付けるやつ",
    author='MasaruKobayashi',
    install_requires=["prompt_toolkit"],
    entry_points={
        "console_scripts": [
            "checkbox=checkbox.main:run"
        ]
    },
)
