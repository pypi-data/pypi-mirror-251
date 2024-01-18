
# qdpxlib

This is `qdpxlib`, a Python API for easy handling (importing and exporting) of QDPX (MAXQDA) files.

## Installation

You can install `qdpxlib` using pip:

```bash
pip install qdpxlib
```

## Usage

Here's a simple example of how to use `qdpxlib`:

```python
import json
from qdpxlib import QDPXFile

qdpx_file = 'path/to/qdpxfile.qdpx'
output_json = 'output.json'
output_qdpx = 'new_qdpx.qdpx'

qdpx = QDPXFile(qdpx_file)

# Export them as JSON
with open(output_json, 'w') as f:
    json.dump(qdpx.codings, f, indent=4)

# Export new qdpx file
qdpx.export_qdpx(qdpx_file, output_qdpx)
```

## Contributing

Contributions are welcome! Please reach out to oyonay12@tamu.edu or make a pull request to contribute. We will post more detailed contribution guidelines soon.

## License

This project is licensed under the MIT license.