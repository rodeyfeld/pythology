`/usr/bin/python3.11 -m venv venv_dreamflow`
`source venv_dreamflow/bin/activate`
`python -m pip install pip-tools`
`pip-sync`


## compile settings
`pip-compile --constraint=requirements.txt --extra=dev --output-file=dev-requirements.txt`

`pip-compile --output-file=requirements.txt pyproject.toml`
