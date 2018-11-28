# Public API Docs

This hosts the Xerpa public API docs.

# Data structures

Use the following script to update the data structure section:

```
$ mkdir $HOME/pyenv
$ python3 -m venv $HOME/pyenv/xerpa
$ $HOME/pyenv/xerpa/bin/pip install requests
$ env lukla_api_token=LUKLA_API_TOKEN bin_python=$HOME/pyenv/xerpa/bin/python ext/bin/add-data-structures
```

Where `LUKLA_API_TOKEN` is the Lukla Public API Token for any company in [Sandbox](https://sandbox.xerpa.com.br).

To introspect your local server, say, at `http://localhost:4000`, use:

```bash
$ env lukla_api_token=LUKLA_API_TOKEN lukla_url=http://localhost:4000 bin_python=$HOME/pyenv/xerpa/bin/python ext/bin/add-data-structures
```

If `lukla_url` is not given, `https://sandbox.xerpa.com.br` will be used.

# Local testing

To test locally, install the [Apiary Client](https://github.com/apiaryio/apiary-client) gem:

```bash
$ gem install apiaryio
$ apiary preview --server --watch
```

This will start a server on `localhost:8080` by default.

To select another port:

```bash
$ apiary preview --server --watch --port 9090
```
