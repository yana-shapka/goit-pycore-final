from setuptools import setup, find_packages # type: ignore

setup(
    name="personal-assistant",
    version="1.0.0",
    description="CLI Personal Assistant for managing contacts and notes",
    author="Yana Shapka",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "assistant = personal_assistant.main:main",
        ],
    },
    python_requires=">=3.10",
)