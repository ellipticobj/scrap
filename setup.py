from setuptools import setup, find_packages

setup(
    name="scrap",
    version="0.1.0",
    description="quick note taking app",
    author="luna rios",
    author_email="luna@hackclub.com",
    url="https://github.com/ellipticobj/scrap",
    packages=find_packages(),
    py_modules=['main', 'editor'],
    install_requires=[
        "prompt_toolkit"
    ],
    entry_points={
        "console_scripts": [
            "scrap = main:main"
        ]
    },
)
