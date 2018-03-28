# Public API Docs

This hosts the Xerpa public API docs.

# Data structures

use the following script to update the data structure section:

```
$ mkdir $HOME/pyenv
$ python3 -m venv $HOME/pyenv/xerpa
$ $HOME/pyenv/xerpa/bin/pip install requests
$ env lukla_api_token=LUKLA_API_TOKEN bin_python=$HOME/pyenv/xerpa/bin/python ext/bin/add-data-structures
```
