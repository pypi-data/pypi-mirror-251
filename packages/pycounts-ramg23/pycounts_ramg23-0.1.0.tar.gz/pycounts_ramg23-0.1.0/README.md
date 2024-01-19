# pycounts_ramg23

Calculate words counts in a text file!

## Installation

```bash
$ pip install pycounts_ramg23
```

## Usage

`pycounts_ramg23` can be used to count words in a text file and plot results as follows:

```python
from pycounts_ramg23.pycounts_ramg23 import count_words
from pycounts_ramg23.plotting import plot_words
import matplotlib.pyplot as plot

file_path = "test.txt"  # path to your file_path
counts = count_words(file_path)
fig = plot_words(counts,n=10)
plt.show()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pycounts_ramg23` was created by Rafael Montoya. It is licensed under the terms of the MIT license.

## Credits

`pycounts_ramg23` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
