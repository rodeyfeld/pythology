
`sudo apt-get install graphviz`

`/usr/bin/python3.11 -m venv venv_dreamflow`
`source venv_dreamflow/bin/activate`
`python -m pip install pip-tools`
`pip-sync`


## compile settings
This project uses a constraints file. 
`pip-compile --output-file=requirements.txt pyproject.toml --constraint constraints.tx`
