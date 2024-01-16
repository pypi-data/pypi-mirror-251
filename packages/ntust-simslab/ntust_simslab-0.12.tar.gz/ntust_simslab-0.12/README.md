# Build A Simple Python Package

This is a simple example of how to build your own Python package.

## Installation

Install towards current directory:
```javascript
pip install .

>>> Output:
>>> Processing /Users/hsiangjenli/Documents/github/tutorial-simple-pypkg
>>>   Installing build dependencies ... done
>>>   Getting requirements to build wheel ... done
>>>   Preparing metadata (pyproject.toml) ... done
>>> Requirement already satisfied: requests<3.0.0,>=2.28.2 in /Users/hsiangjenli/miniconda3/lib/python3.11/site-packages (from ntust-simslab-pkg==0.1) (2.31.0)
>>> Requirement already satisfied: charset-normalizer<4,>=2 in /Users/hsiangjenli/miniconda3/lib/python3.11/site-packages (from requests<3.0.0,>=2.28.2->ntust-simslab-pkg==0.1) (2.0.4)
>>> equirement already satisfied: idna<4,>=2.5 in /Users/hsiangjenli/miniconda3/lib/python3.11/site-packages (from requests<3.0.0,>=2.28.2->ntust-simslab-pkg==0.1) (3.4)
>>> Requirement already satisfied: urllib3<3,>=1.21.1 in /Users/hsiangjenli/miniconda3/lib/python3.11/site-packages (from requests<3.0.0,>=2.28.2->ntust-simslab-pkg==0.1) (1.26.16)
>>> Requirement already satisfied: certifi>=2017.4.17 in /Users/hsiangjenli/miniconda3/lib/python3.11/site-packages (from requests<3.0.0,>=2.28.2->ntust-simslab-pkg==0.1) (2023.7.22)
>>> Building wheels for collected packages: ntust-simslab-pkg
>>>   Building wheel for ntust-simslab-pkg (pyproject.toml) ... done
>>>   Created wheel for ntust-simslab-pkg: filename=ntust_simslab_pkg-0.1-py3-none-any.whl size=2196 sha256=37839596c2d37fc0e319662eb41833a005207697e8a9fe6d262f574434637202
>>>   Stored in directory: /Users/hsiangjenli/Library/Caches/pip/wheels/ea/62/01/cc30cb512e66bc464fdfaf3e5c85b38e238c829c084eb5f3d6
>>> Successfully built ntust-simslab-pkg
>>> Installing collected packages: ntust-simslab-pkg
>>> Successfully installed ntust-simslab-pkg-0.1
```



Install from GitHub:
```shell
pip install git+https://github.com/hsiangjenli/tutorial-simple-pypkg.git@package
```

## Pushing to PyPi

1. Build the package:
    ```javascript
    python setup.py sdist

    >>> Output:
    >>> running sdist
    >>> running egg_info
    >>> creating ntust_simslab.egg-info
    >>> writing ntust_simslab.egg-info/PKG-INFO
    >>> writing dependency_links to ntust_simslab.egg-info/dependency_links.txt
    >>> writing top-level names to ntust_simslab.egg-info/top_level.txt
    >>> writing manifest file 'ntust_simslab.egg-info/SOURCES.txt'
    >>> reading manifest file 'ntust_simslab.egg-info/SOURCES.txt'
    >>> writing manifest file 'ntust_simslab.egg-info/SOURCES.txt'
    >>> running check
    >>> creating ntust_simslab-0.1
    >>> creating ntust_simslab-0.1/ntust_simslab.egg-info
    >>> copying files to ntust_simslab-0.1...
    >>> copying README.md -> ntust_simslab-0.1
    >>> copying pyproject.toml -> ntust_simslab-0.1
    >>> copying setup.py -> ntust_simslab-0.1
    >>> copying ntust_simslab.egg-info/PKG-INFO -> ntust_simslab-0.1/ntust_simslab.egg-info
    >>> copying ntust_simslab.egg-info/SOURCES.txt -> ntust_simslab-0.1/ntust_simslab.egg-info
    >>> copying ntust_simslab.egg-info/dependency_links.txt -> ntust_simslab-0.1/ntust_simslab.egg-info
    >>> copying ntust_simslab.egg-info/top_level.txt -> ntust_simslab-0.1/ntust_simslab.egg-info
    >>> Writing ntust_simslab-0.1/setup.cfg
    >>> creating dist
    >>> Creating tar archive
    >>> removing 'ntust_simslab-0.1' (and everything under it)
    ```
1. Upload the package to PyPI(You need to have an account)
    ```shell
    pip install twine
    twine upload dist/*
    ```
    - https://pypi.org/help/#apitoken
    - ![Alt text](image.png)
1. Install the package from [PyPI](https://pypi.org/project/ntust-simslab/)
    ```shell
    pip install ntust-simslab==0.1
    ```

## Usage

Then you can simply import the package from anywhere:
```python
from ntust_simslab import lab

lab = lab.Lab(professor="楊龍龍")
lab.add_student("李貓貓")
```