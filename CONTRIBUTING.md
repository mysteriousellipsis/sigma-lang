# contributing to sigma
please follow the [code of conduct](CODE_OF_CONDUCT.md)!!!!!!  
we accept any contributions!!  
feel free to refactor, propose/make new features or improve documentation  
please include a **clear description** of your changes in your pr or commit history  

# note
all required packages for you should be listed in [devrequirements.txt](devrequirements.txt)  
run `pip install -r devrequirements.txt` to install all required packages  
if you are doing a big big refactor or feature, please create an issue first and discuss it with us 

we use **[mypy](https://mypy.readthedocs.io/)** to ensure static typing.  
please ensure `mypy main.py` returns `Success: no issues found in 1 source file` before submitting a pull request  
if you have any trouble you can submit a pull request with your changes and ask for help and we'll try to help you fix it  
(install mypy using `pip install mypy` or `pip3 install mypy` depending on your system)  
  
we use **[black](https://black.readthedocs.io/)** to ensure consistent formatting.  
please use black before submitting a pr!!  
(install black using `pip install black` or `pip3 install black` depending on your system)
