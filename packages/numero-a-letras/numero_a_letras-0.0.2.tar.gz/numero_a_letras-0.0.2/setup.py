import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="numero_a_letras",
    version="0.0.2",
    author="Eugenio",
    author_email="coding_with@eugeniovazquez.com.ar",
    description="Convierte un numero a su representacion en letras",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lugezz/numero_a_letras_literal",
    project_urls={
        "Issues": "https://github.com/lugezz/numero_a_letras_literal/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8"
)
