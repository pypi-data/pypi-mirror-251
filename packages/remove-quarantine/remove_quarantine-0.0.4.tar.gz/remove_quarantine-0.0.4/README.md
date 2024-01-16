# remove_quarantine pypi package

A package that on install removes quarantine bit from Indigo installed Plugins


Usage:  Should be used behind the scenes to remove quarantine plugin related issues

The package consists of very little, but on pip3 install remove_quarantine will run a script to remove quarantine bit from Indigo plugin packages
This removes issues with binaries being include

## Installation

To install the package, run:

```python
pip3 remove_quarantine
```

## Usage

Here's how you can use the package:


Add in requirements.txt

remove_quarantine==2023.2

No import in code needed.
No further code needed.
Version number == Indigo version number

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
