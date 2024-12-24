---
hide:
  - navigation
#   - toc
---

# Introduction

{{cookiecutter.project_description}}

## ✨ Features

- FastAPI
- REST API
- Web service
- Microservice
- Template
- CI/CD
- Docker and docker compose

## 🧩 Template

- You can use this template repository as reference to create a new repository with the same structure or clone the repository to start a new project. It will help you to organize your project structure and files. It works out of the box for most REST API service projects.
- You can customize (remove, modify or add) the files and directories as needed to meet your project requirements.
- If you want to use the template repository directly, just click the **[Use this template](https://github.com/new?template_name={{cookiecutter.repo_name}}&template_owner={{cookiecutter.repo_owner}})** button and follow the instructions.
- You can use **cookiecutter** to generate a new project from **[cookiecutter](https://github.com/{{cookiecutter.repo_owner}}/{{cookiecutter.repo_name}}/tree/cookiecutter)** branch:

    ```sh
    # Clone the cookiecutter branch:
    git clone -b cookiecutter https://github.com/{{cookiecutter.repo_owner}}/{{cookiecutter.repo_name}}.git

    # Install cookiecutter:
    pip install cookiecutter

    # Generate a new project from the cookiecutter template:
    cookiecutter -f .
    ```
