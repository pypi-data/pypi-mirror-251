"""
Use this guide:
https://packaging.python.org/tutorials/packaging-projects/

py -m build && twine upload dist/*
linux: python -m build && python -m twine upload dist/*

git add . && git commit -m"updates" && git push
sudo pip install -e ./
"""
import setuptools
with open("src/unitgrade/version.py", "r", encoding="utf-8") as fh:
    __version__ = fh.read().split("=")[1].strip()[1:-1]
# long_description = fh.read()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="unitgrade",
    version=__version__,
    author="Tue Herlau",
    author_email="tuhe@dtu.dk",
    description="A student homework/exam evaluation framework build on pythons unittest framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://lab.compute.dtu.dk/tuhe/unitgrade',
    project_urls={
        "Bug Tracker": "https://lab.compute.dtu.dk/tuhe/unitgrade/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    license="MIT",
    install_requires=['numpy', 'tabulate', "pyfiglet<1.0.0", "coverage", "colorama", 'tqdm', 'importnb', 'requests', "pandas",
                      'watchdog', 'flask_socketio', 'flask', 'Werkzeug>=2.3.0', 'diskcache', # These are for the dashboard.
                      ],
    include_package_data=True,
    package_data={'': ['dashboard/static/*', 'dashboard/templates/*'],},  # so far no Manifest.in.
    entry_points={
        'console_scripts': ['unitgrade=unitgrade.dashboard.dashboard_cli:main'],
    }
)
