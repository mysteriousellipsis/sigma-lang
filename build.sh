pip3 install -U PyInstaller

echo "purging ./dist/"
rm -rf dist/
echo "purging ./build/"
rm -rf build/

python -m PyInstaller --onefile --name "sigma-$(arch)" main.py

echo "removing .spec file"
rm -rf "sigma-$(arch).spec"

echo "executable at dist/sigma-$(arch)"