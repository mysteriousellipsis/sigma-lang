pip3 install -U PyInstaller

echo "purging ./dist/"
rm -rf dist/

python -m PyInstaller --onefile --name "sigma-$(arch)" main.py

echo "executable at dist/sigma-$(arch)"