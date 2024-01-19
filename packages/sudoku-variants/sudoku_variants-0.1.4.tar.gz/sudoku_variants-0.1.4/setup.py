from distutils.core import setup

setup(
    name="sudoku_variants",
    packages=["sudoku_variants", "sudoku_variants/func", "sudoku_variants/rule"],
    version="0.1.4",  # Need update
    license="MIT",
    description="Sudoku solver and generator that supports variant rules",
    author="Rapid Rabbit",
    author_email="rapid.rabbit.tech@gmail.com",
    url="https://github.com/KaFaiFai/sudoku_variants",
    download_url="https://github.com/KaFaiFai/sudoku_variants/archive/refs/tags/v_0_1_4.tar.gz",  # Need update
    keywords=["Sudoku", "Variants", "Generator", "Solver"],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
