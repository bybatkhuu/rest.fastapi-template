# FastAPI Template (Cookiecutter)

This is a cookiecutter template for FastAPI projects.

## Features

- Cookiecutter
- FastAPI
- REST API
- Web service
- Microservice
- Template
- CI/CD
- Docker and docker compose

---

## Getting started

### 1. Prerequisites

- Install **Python (>= v3.9)**:
    - **[RECOMMENDED] Miniconda (v3)** - <https://docs.conda.io/projects/miniconda/en/latest/index.html>
    - *[arm64/aarch64] Miniforge (v3)* - <https://github.com/conda-forge/miniforge>
    - *[OPTIONAL] venv* - <https://docs.python.org/3/library/venv.html>
- Install **docker** and **docker compose** - <https://docs.docker.com/engine/install>

For **development** environment:

- Install **git** - <https://git-scm.com/downloads>
- Setup an **SSH key** - <https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh>

### 2. Download or clone the repository

**2.1.** Prepare projects directory (if not exists):

```sh
# Create projects directory:
mkdir -pv ~/workspaces/projects

# Enter into projects directory:
cd ~/workspaces/projects

# Set repository owner:
export _REPO_OWNER=[REPO_OWNER]
# For example:
export _REPO_OWNER=username
```

**2.2.** Follow one of the below options **[A]**, **[B]** or **[C]**:

**A.** Clone the repository (for **public**: git + https):

```sh
git clone https://github.com/${_REPO_OWNER}/rest.fastapi-template.git && \
    cd rest.fastapi-template && \
    git checkout cookiecutter
```

**B.** Clone the repository (for **development**: git + ssh key):

```sh
git clone git@github.com:${_REPO_OWNER}/rest.fastapi-template.git && \
    cd rest.fastapi-template && \
    git checkout cookiecutter
```

**C.** Or download source code.

### 3. Install cookiecutter

```bash
# Install cookiecutter:
pip install -U cookiecutter
# Or:
pip install -r ./requirements.txt
```

### 4. Generate project with cookiecutter

```bash
# Generate project (project name, project slug, repo owner, version, etc.):
cookiecutter -f .
# Or:
./scripts/generate.sh
```

### 5. Start the project

```bash
cd [PROJECT_NAME]
# For example:
cd fastapi-template

# Start:
./compose.sh start -l

# Stop:
./compose.sh stop
```

:thumbsup: :sparkles:

## References

- Cookiecutter (GitHub) - <https://github.com/cookiecutter/cookiecutter>
- Cookiecutter (Docs) - <https://cookiecutter.readthedocs.io/en/stable>
- FastAPI - <https://fastapi.tiangolo.com>
