# setup.py
from setuptools import setup

setup(
    name="tinyra",
    version="0.2.0.post3",
    description="A minimalistic research assistant built with AutoGen.",
    py_modules=["tinyra"],
    install_requires=["textual", "tiktoken", "pyautogen"],
    entry_points={
        "console_scripts": [
            "tinyra = tinyra:run_tinyra",
        ],
    },
)
