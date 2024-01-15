# SciBib

A Python package to collect scientific bibliographical data.


## Installation

This package can be installed with pip.

```
$ pip install scibib
```

Furthermore, you will need to edit a configuration file to pass your orcid_token.
This can be done interactively running
```
python -m scibib.data_query
```
You will be prompted to give your Orcid /read-public API token:
```
Please provide the value for orcid_token in your config file.
▯
```

If you prefer to edit the file directly, cancel with Ctrl+C. The message in
an ImportError will tell you which file to edit *e.g.*
```
[...]
ImportError: Please edit your module configuration file /home/gael/.config/scibib/scibib_config.py to define the orcid_token variable.This token is needed to use orcid's /read-public API.
```


## Usage
A basic demo is provided as test/demo.py on the GitHub repository.


A complete documentation of the package is provided in pdf 
[here](https://github.com/completementgaga/SciBib/blob/master/package_manual.pdf),
 the html version is served on 
[GitHub Pages](https://completementgaga.github.io/SciBib/).