# Release Steps

1. Install prerequisites:

    python -m pip install --upgrade build twine

2. Squash merge dev into main:

    git checkout main
    git merge --squash dev

3. Update NEWS.md and bump the `__version__` value in `src/codebooks/__init__.py`

4. Build and validate the dist files:

    python -m build
    twine check dist/*

5. Upload dist files to the test PyPI instance:

    twine upload --repository testpypi dist/*

6. Install from test PyPI and test package:

    python -m venv testenv
    source testenv/bin/activate # or on Windows: \testenv\Scripts\Activate.ps1
    pip install --index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple codebooks
    python -c 'import codebooks; print(codebooks.__version__);'
    cd test
    pip install pyarrow
    python dataset.py
    codebooks --desc desc.csv dataset.csv
    codebooks --desc desc.csv --parquet dataset.parquet
    cd ..
    deactivate
    rm -rf testenv # or on Windows: del testenv

7. Upload final package to PyPI:

    twine upload dist/*

8. Commit and tag release:

    git commit -am "{VERSION}"
    git tag v{VERSION}
    git push
    git push --tags
    git checkout dev
    git merge main
    git push

