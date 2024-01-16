# remove_quarantine pypi package

A package that on install removes quarantine bit from Indigo installed Plugins, from both Plugins and Plugins (Disabled) folders

Usage:  Should be used behind the scenes to remove quarantine plugin related issues by plugin authors.

The package consists of very little, but on pip3 install remove_quarantine will run a script to remove quarantine bit from Indigo plugin packages

Simply having this in the requirements.txt file means with pip3 install of this library all current indigoPlugin bundles within Plugin and Plugin (Disabled) folders are unquarantined.  This includes the current folder which is having libraries install into it.
In my test this completely resolves the binary quarantine issue.

It is hard coded to Indigo version through lack of any possible other approach.  Hence will need new releases with Major Indigo version changes.

## Installation

To install the package, run:

```python
pip3 install remove_quarantine==2023.2.*
```
With version here equally the Indigo version you wish to apply to.  Note the last star updating to latest minor/patch version.

## Usage

Here's how you can use the package:

Add it to requirements.txt

requirements.txt contents:
`remove_quarantine==2023.2.*`
* added to always update to any minor version/patch changes

No import in code needed.   No further code needed.
Version number == Indigo version number

## Potential issues

If pip has cached the package and version then the unquarantine command will not be executed with import alone.
This can be overcome by using the --no-cache-dir with pip3 install
eg.
```python
pip3 install --no-cache-dir remove_quarantine==2023.2.*
```
If this option is not available, then the below aspects can be used early in import process.

eg. plugin.py, remove_quarantine==2023.2.* in requirements
```python
from remove_quarantine import remove_quarantine, show_logging
remove_quarantine()
import logging
import indigo 
```

## Other usage

Below is not needed, simply have this in the requirements.txt file means with every pip3 install of this library all current indigoPlugin bundles within Plugin and Plugin (Disabled) folders are unquarantined.  This includes the current folder which is having libraries install into it.
In my test this completely resolves the binary quarantine issue.

```python
from remove_quarantine import remove_quarantine, show_logging
print(show_logging()) ## Will display logging of installation removal of quarantine bits

results_remove = remove_quarantine()
print(results_remove)
## Will re-run the quarantine removal process and print the results from this.
```


```python
pip3 remove_quarantine
```

## License

This project is licensed under the MIT License - see the LICENSE file for details

MIT License

Copyright (c) [2023]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
