# installing python
this is a short guide on how to install python!

there are two methods to install python: [manual installation](INSTALLPYTHON.md#manual-installation) and [using pyenv](INSTALLPYTHON.md#using-pyenv)

# using pyenv
this method is better if you plan to use python in the future  
a little tougher but using multiple python versions is easier  

1. setting up pyenv
firstly, install [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)  

2. installing python
after setting up pyenv, you can install python by running the following command:

```
pyenv install 3.13
```

3. set your python version
```
pyenv global 3.13
```

now go to [this section](INSTALLPYTHON.md#after-installation)

# manual installation
this method is easier to do, but problems can arise in the future  
go to [python's website](https://www.python.org/downloads/) and install the latest version of python.  

now go to [this section](INSTALLPYTHON.md#after-installation)

# after installation
run the following command to check if python is installed correctly:

```
python --version
```
