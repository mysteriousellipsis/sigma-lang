echo "this script will help you update python"
echo "note that brew (https://brew.sh) will be installed"
echo "xcode select developer tools will be installed"
echo "pyenv will be installed"
echo "python 3.13 will be installed"
echo "enter your password if prompted to"
echo "enter to continue"
read
echo "installing developer tools..."
xcode-select --install
echo "done"
echo ""
echo "installing brew..."
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
if ($0 -eq "zsh") then
    export PATH=/usr/local/bin:$PATH > ~/.zshrc
    source ~/.zshrc
else
    export PATH=/usr/local/bin:$PATH > ~/.bash_profile
    source ~/.bash_profile
fi
brew doctor
echo ""
echo "installing pyenv..."
brew install pyenv
echo ""
echo "installing python 3.13 (latest tested version)"
pyenv install 3.13 --ensure-pip
echo "setting default python version to 3.13"
pyenv global 3.13
echo ""
echo "installed pyenv with version 3.13"
echo "to revert changes, run 'brew uninstall pyenv && /bin/bash -c \$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)'"
