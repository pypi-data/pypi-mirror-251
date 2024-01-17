# https://packaging.python.org/en/latest/tutorials/packaging-projects/

python3 -m pip install --upgrade build --break-system-packages

# Delete _build directory
rm -rf _build

# Delete dist directory
rm -rf dist

# Delete egg-info
rm -rf *.egg-info

# Delete all cache
rm -rf .cache



# Purge pip cache
pip cache purge




python3 -m build
python3 -m pip install --upgrade twine --break-system-packages
python3 -m twine upload --repository testpypi dist/*

# to install: python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ my_clippings