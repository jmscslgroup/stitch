import setuptools


def get_version():
    exec(open("stitch/version.py").read(), locals())
    return locals()["__version__"]


def get_requirements():
    with open("requirements.txt") as f:
        lines = f.read().strip().split("\n")
    return lines


name = "stitch"

version = get_version()

description = "Stitch videos of the same drive."

python_requires = ">=3.8"

packages = ["stitch"]

install_requires = get_requirements()

setuptools.setup(
    name=name,
    version=version,
    description=description,
    python_requires=python_requires,
    packages=packages,
    install_requires=install_requires,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "stitch = stitch.__main__:main",
        ],
    },
)
