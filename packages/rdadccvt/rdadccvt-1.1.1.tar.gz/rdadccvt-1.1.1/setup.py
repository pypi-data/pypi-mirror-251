from setuptools import setup, find_packages

setup(
    name="rdadccvt",
    version="1.1.1",
    description="Balzer's algorithm (DCCVT) to find a maximally population compact map",
    url="https://github.com/rdatools/rdadccvt",
    author="alecramsay",
    author_email="a73cram5ay@gmail.com",
    license="MIT",
    packages=[
        "rdadccvt",
    ],
    install_requires=["rdabase", "scipy"],
    zip_safe=False,
)
