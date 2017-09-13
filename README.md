# Public API Docs

This hosts the Xerpa public API docs.

## Usage

### Prerequisites
- node
- graphdoc (`npm install -g @2fd/graphdoc`)

### To build the docs run:

    graphdoc -x "xerpa-token: $XERPA_TOKEN" -c xerpa_public_api.json -f

`XERPA_TOKEN` is a variable with a production public api token
