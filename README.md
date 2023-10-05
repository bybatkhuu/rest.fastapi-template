# FastAPI template

This is a template repo for a FastAPI project.

## Features

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

For **docker** environment:

- Install **docker** and **docker compose** - <https://docs.docker.com/engine/install>

For **standalone** environment:

- Install **Python (>= v3.9)**:
    - **[RECOMMENDED] Miniconda (v3)** - <https://docs.conda.io/en/latest/miniconda.html>
    - *[OPTIONAL] venv* - <https://docs.python.org/3/library/venv.html>

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

**A.** Or clone the repository (for development: git + ssh key):

```sh
git clone git@github.com:${_REPO_OWNER}/rest.fastapi-template.git && cd rest.fastapi-template
```

**B.** Download source code.

### 3. Install python dependencies

**TIP:** Skip this step, if you're going to use **docker** environment.

<!-- #### 3.1. Install base/common dependencies -->

```bash
pip install -r ./requirements.txt
```

<!-- #### 3.2. Install hardware specific dependencies

Follow the one of below instructions based on your environment (A is recommended for most cases):

**A.** For Intel/AMD **x86_64** CPU:

```bash
pip install -r ./requirements.amd64.txt
```

**B.** For **arm64/aarch64** CPU:

```bash
pip install -r ./requirements.arm64.txt
```

**C.** For **NVIDIA GPU** and **x86_64** CPU:

```bash
pip install -r ./requirements.gpu.txt
``` -->

### 4. Configure environment variables

**TIP:** Skip this step, if you've already configured environment.

**IMPORTANT:** Please, check **[environment variables](#environment-variables)**!

#### **A.** **[RECOMMENDED]** For **docker** environment **[5.A]**

```sh
# Copy `.env.example` file to `.env`:
cp -v .env.example .env

# Edit environment variables to fit in your environment:
nano .env
```

#### **B.** For **standalone** environment **[5.B ~ 5.F]**

```sh
# Copy `.env.example file` into `.env` file:
cp -v .env.example fastapi_template/.env

# Edit environment variables to fit in your environment:
nano ./fastapi_template/.env

# Enter into app directory:
cd fastapi_template
```

### 5. Run the server

Follow the one of below instructions based on your environment **[A, B, C, D, E, F]**:

#### Docker environment

**A.** **[RECOMMENDED]** Run with **Docker Compose**:

**IMPORTANT:** Please, check **[arguments](#arguments)**!

```bash
## 1. Configure `docker-compose.override.yml` file.
# TIP: Skip this step, if you've already configured.

# Set environment:
export _ENV=[ENV]
# For example for development environment:
export _ENV=dev

# Copy docker-compose.override.[ENV].yml into `docker-compose.override.yml` file:
cp -v ./templates/docker-compose/docker-compose.override.${_ENV}.yml docker-compose.override.yml

# Edit `docker-compose.override.yml` file to fit in your environment:
nano docker-compose.override.yml


## 2. Check docker compose configuration is valid:
./compose.sh validate
# Or:
docker compose config


## 3. Start docker compose:
./compose.sh start -l
# Or:
docker compose up -d && \
    docker compose logs -f --tail 100


## 3. Stop docker compose:
./compose.sh stop
# Or:
docker compose down
```

#### Standalone environment (Process Manager)

**B.** Or run with **PM2**:

Before running, need to install **PM2**: <https://pm2.keymetrics.io/docs/usage/quick-start>

```bash
## 1. Configure PM2 configuration file.
# TIP: Skip this step, if you've already configured.

# Copy example PM2 configuration file:
cp -v pm2-process.json.example pm2-process.json

# Edit PM2 configuration file to fit in your environment:
nano pm2-process.json


## 2. Start PM2 process:
pm2 start ./pm2-process.json && \
    pm2 logs --lines 50 fastapi-template


## 3. Stop PM2 process:
pm2 stop ./pm2-process.json && \
    pm2 flush && \
    pm2 delete ./pm2-process.json
```

#### Standalone environment (Python)

**C.** Or run server as **Python module**:

```bash
# Run server as python module:
python -u -m fastapi_template
```

**D.** Or run server as **Python script**:

```bash
# Enter into project directory:
cd fastapi_template

# Run server as python script:
python -u main.py
```

**E.** Run with **uvicorn**:

```bash
# Run uvicorn server:
uvicorn fastapi_template.main:app --host=[BIND_HOST] --port=[PORT] --no-server-header --forwarded-allow-ips="*" --no-access-log

# For example:
uvicorn fastapi_template.main:app --host=0.0.0.0 --port=8000 --no-server-header --forwarded-allow-ips="*" --no-access-log

# For development:
# Enter into project directory:
cd fastapi_template
uvicorn main:app --host=0.0.0.0 --port=8000 --no-server-header --forwarded-allow-ips="*" --no-access-log --reload --reload-include="*.yml" --reload-include="*.yaml" --reload-include="*.json"
```

**F.** Or run with **gunicorn**:

```bash
# Or run gunicorn server:
gunicorn -k=uvicorn.workers.UvicornWorker fastapi_template.main:app -b=[BIND_HOST]:[PORT] --proxy-protocol --forwarded-allow-ips="*" --proxy-allow-from="*"

# For example:
gunicorn -k=uvicorn.workers.UvicornWorker fastapi_template.main:app -b=0.0.0.0:8000 --proxy-protocol --forwarded-allow-ips="*" --proxy-allow-from="*"

# For development:
# Enter into project directory:
cd fastapi_template
gunicorn -k=uvicorn.workers.UvicornWorker main:app -b=0.0.0.0:8000 --proxy-protocol --forwarded-allow-ips="*" --proxy-allow-from="*" --reload
```

:thumbsup: :sparkles:

---

## Environment Variables

You can use the following environment variables to configure:

[**`.env.example`**](.env.example)

```sh
ENV=local
DEBUG=false

# CHANGEME: Change project name with env variables prefix:
## FastAPI template settings:
FASTAPI_TEMPLATE_APP__PORT=8000
FASTAPI_TEMPLATE_LOGGER__FILE__LOGS_DIR="/var/log/{app_name}"

## Docker image namespace:
IMG_NAMESCAPE=username # CHANGEME: Change docker image namespace (dockerhub username, or registry hostname)

## Docker build arguments:
# HASH_PASSWORD="\$1\$K4Iyj0KF\$SyXMbO1NTSeKzng1TBzHt."
# IMG_ARGS="--build-arg HASH_PASSWORD=${HASH_PASSWORD}"


## Project variables:
PROJECT_NAME=fastapi-template # CHANGEME: Change project name
PROJECT_DIR_NAME=fastapi_template # CHANGEME: Change project directory name
```

## Arguments

You can use the following arguments to configure:

```txt
-b, --bash, bash, /bin/bash
    Run only bash shell.
```

For example as in [**`docker-compose.override.yml`**](templates/docker-compose/docker-compose.override.dev.gpu.yml) file:

```yml
    command: ["/bin/bash"]
    command: ["-b", "pwd && ls -al && /bin/bash"]
    command: ["-b", "sleep 1 && uvicorn main:app --host=0.0.0.0 --port=${FASTAPI_TEMPLATE_APP__PORT:-8000} --no-server-header --proxy-headers --forwarded-allow-ips='*' --no-access-log"]
```

## Documentation

- [Build docker image](docs/docker-build.md)

## Roadmap

...

---

## References

- FastAPI - <https://fastapi.tiangolo.com>
