
# Publish new Version
```
python setup.py sdist 

twine upload dist/*
```

# Unitests

### Run test with coverage in terminal
```
pytest --cov=fastapi_dream_core
```


### Generate HTML with coverage
```
pytest --cov=fastapi_dream_core --cov-report=html
```