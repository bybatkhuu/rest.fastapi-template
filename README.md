# FastAPI template

This is a template repo for a FastAPI project.

## Features

- FastAPI
- REST API
- Web service
- Microservice
- Template
- CI/CD
- Docker and docker-compose

---

## Getting started

### Prerequisites

For **standalone** environment:

- Install **Python (>= v3.9)**:
    - **[RECOMMENDED] Miniconda (v3)** - <https://docs.conda.io/en/latest/miniconda.html>
    - *[OPTIONAL] venv* - <https://docs.python.org/3/library/venv.html>

For **docker** environment:

- Install **docker** and **docker-compose** - <https://docs.docker.com/engine/install>

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

**2.2.** Follow one of the below options **[A]** or **[B]**:

**A.** Download source code from releases page:

- Releases - <https://github.com/[REPO_OWNER]/rest.fastapi_template/releases>

```sh
# Set to downloaded version:
export _VERSION=[VERSION]
# For example:
export _VERSION=1.0.0

mv -v ~/Downloads/rest.fastapi_template-${_VERSION}.zip . && \
    unzip rest.fastapi_template-${_VERSION}.zip && \
    rm -v rest.fastapi_template-${_VERSION}.zip && \
    mv -v rest.fastapi_template-${_VERSION} rest.fastapi_template && \
    cd rest.fastapi_template
```

**B.** Or clone the repository (for development: git + ssh key):

```sh
git clone git@github.com:${_REPO_OWNER}/rest.fastapi_template.git && cd rest.fastapi_template
```

### 3. Install python dependencies

<!-- #### 3.1. Install base/common dependencies -->

```bash
< ./requirements.txt grep -v '^#' | xargs -t -L 1 pip install --timeout 60 --no-cache-dir
```

<!-- #### 3.2. Install hardware specific dependencies

Follow the one of below instructions based on your environment (A is recommended for most cases):

**A.** For Intel/AMD **x86_64** CPU:

```bash
< ./requirements.amd64.txt grep -v '^#' | xargs -t -L 1 pip install --timeout 60 --no-cache-dir
```

**B.** For **arm64/aarch64** CPU:

```bash
< ./requirements.arm64.txt grep -v '^#' | xargs -t -L 1 pip install --timeout 60 --no-cache-dir
```

**C.** For **NVIDIA GPU** and **x86_64** CPU:

```bash
< ./requirements.gpu.txt grep -v '^#' | xargs -t -L 1 pip install --timeout 60 --no-cache-dir
``` -->

### 4. Configure environment variables

**TIP:** Skip this step, if you've already configured environment.

**IMPORTANT:** Please, check **[environment variables](#environment-variables)**!

```sh
# Copy .env.example file into .env file:
cp -v .env.example app/.env

# Edit environment variables to fit in your environment:
nano ./app/.env

# Enter into app directory:
cd app
```

### 5. Run the server

Follow the one of below instructions based on your environment **[A, B, C, D, E]**:

**A.** Run server directly:

```bash
# Run python server:
python main.py
```

**B.** Or run server with **uvicorn**:

```bash
# Run uvicorn server:
uvicorn main:app --host=[BIND_HOST] --port=[PORT] --no-access-log
# For example:
uvicorn main:app --host=0.0.0.0 --port=8000 --no-access-log
# For development:
uvicorn main:app --host=0.0.0.0 --port=8000 --no-access-log --reload --reload-include="*.yml"
```

**C.** Or run server with **gunicorn**:

```bash
# Or run gunicorn server:
gunicorn -w=[WORKER] -k=uvicorn.workers.UvicornWorker main:app -b=[BIND_HOST]:[PORT]
# For example:
gunicorn -w=4 -k=uvicorn.workers.UvicornWorker main:app -b=0.0.0.0:8000
# For development:
gunicorn -w=4 -k=uvicorn.workers.UvicornWorker main:app -b=0.0.0.0:8000 --reload
```

**D.** **[RECOMMENDED]** Or run with **PM2**:

```bash
cd ..

# Copy example PM2 configuration file:
cp -v pm2-process.json.example pm2-process.json

# Start PM2 process:
pm2 start ./pm2-process.json && \
    pm2 logs --lines 50

# Stop PM2 process:
pm2 stop ./pm2-process.json && \
    pm2 delete ./pm2-process.json
```

**E.** **[RECOMMENDED]** Or run with **Docker Compose**:

```bash
cd ..

# Copy .env.example file to .env:
cp -v .env.example .env
# Edit environment variables:
nano .env

# Run docker-compose:
docker-compose up -d && \
    docker-compose logs -f --tail 100

# Stop docker-compose:
docker-compose down
```

:thumbsup: :sparkles:

---

## Environment Variables

You can use the following environment variables to configure:

[**`.env.example`**](.env.example)

```sh
## Docker image namespace:
IMG_NAMESCAPE=username

## FastAPI port:
FASTAPI_PORT=8000
```

## Documentation

- [Build docker image](docs/docker-build.md)

## Roadmap

...

---

## References

- FastAPI - <https://fastapi.tiangolo.com>
