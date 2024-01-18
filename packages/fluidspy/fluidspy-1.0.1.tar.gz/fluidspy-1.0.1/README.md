# fluidspy

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Gh Test](https://github.com/AVAniketh0905/fluidspy/actions/workflows/test_basic.yml/badge.svg)

`fluidspy` is a Python library for Computational Fluid Dynamics (CFD) simulations.

## Features

- Most famous cfd algorithms implemented in python.
- Animations coming soon!

## Installation

You can install `fluidspy` using pip:

```bash
pip install fluidspy
```

## Usage

```python
import fluidspy

fluidspy.standard.one_dim_constant_heat_transfer()

# Should ouput a matplotlib animation.
```

## Contributing

If you want to contribute to this project, see `CONTRIBUTING.md` for guidelines.

### Setup

1. Fork this repository.
2. Clone the forked repository to your local machine.
   `git clone {repo_name}`
3. Change the current working directory to the cloned repository.
4. Add the upstream reference. This will add the original repository as reference.
   `git remote add upstream git@github.com:AVAniketh0905/fluidspy.git`
   - Note
     - Everytime you boot up/push please run the following command to stay up-to date with the original repo.
       `git pull upstream main`
5. Create a virtual environment.
   `python -m venv venv`
6. Activate the virtual environment.
   - Windows
     `venv\Scripts\activate`
   - Linux
     `source venv/bin/activate`
7. Install the dependencies.
   `pip install -r requirements_dev.txt`
8. Make the changes.
9. Run the tests.
   `pytest`
10. Stage the changes.
    `git add .`
11. Run Pre-commit hooks.
    `pre-commit run --all-files`
12. Commit the changes.
13. Push the changes to your forked repository.
14. Create a pull request.
15. Wait for the review!!!

## License

This project is licensed under the MIT License. See the _LICENSE_ file for details.

## Contact

AVAniketh0905 (dekomori_sanae09)
Project Link: [fluidspy](https://github.com/AVAniketh0905/fluidspy)

## Acknowledgments

`Manim` has inspired me a lot!!!
