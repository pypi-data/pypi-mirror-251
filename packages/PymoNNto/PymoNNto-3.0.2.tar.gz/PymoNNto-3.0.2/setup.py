import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PymoNNto",
    version="3.0.2",
    author="Marius Vieth",
    author_email="mv15go@gmail.com",
    description="Python Modular Neural Network Toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trieschlab/PymoNNto",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'PyQt5', 'pyqtgraph', 'matplotlib', 'scipy', 'scikit-learn', 'imageio', 'pillow', 'paramiko', 'scp', 'pandas'],
    entry_points={
        'console_scripts': [
            'Behaviour_UI=PymoNNto.UI.CLI:Behaviour_UI',
            'Evolution_UI=PymoNNto.UI.CLI:Evolution_UI',
            'Plot_UI=PymoNNto.UI.CLI:Execute_UI',
            'Plot_Overview_UI=PymoNNto.UI.CLI:Overview_UI',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)