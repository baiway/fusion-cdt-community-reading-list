# Fusion CDT community reading list
A collection of useful resources related to plasma physics, material science and fusion power created by students on the [EPSRC CDT in Fusion Power](https://fusion-cdt.ac.uk/). 

> [!WARNING]
> This is a work-in-progress.

## Build locally
If you'd like to build the site locally, first clone the repository:
```sh
git clone git@github.com:baiway/fusion-cdt-community-reading-list.git
```

Then change to the project directory:
```sh
cd fusion-cdt-community-reading-list
```

Install `uv` (if you haven't already):
```sh
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Install dependencies and activate virtual environment
```sh
uv sync && source .venv/bin/activate
```

Build site
```sh
zensical serve
```

Open the site using [http://localhost:8000](http://localhost:8000)

## Checking out other branches
If you'd like to check out the 'flat' structure, run:
```sh
git switch flat-structure
```

Then re-build the site with
```sh
zensical serve
```
