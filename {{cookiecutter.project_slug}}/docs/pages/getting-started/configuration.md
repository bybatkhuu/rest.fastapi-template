# ⚙️ Configuration

## 🌎 Environment Variables

[**`.env.example`**](https://github.com/{{cookiecutter.repo_owner}}/{{cookiecutter.repo_name}}/blob/main/.env.example):

```sh
## --- Environment variable --- ##
ENV=LOCAL
DEBUG=false
# TZ={{cookiecutter.timezone}}


## -- API configs -- ##
{{cookiecutter.env_prefix}}API_PORT=8000
{{cookiecutter.env_prefix}}API_LOGS_DIR="/var/log/{{cookiecutter.project_slug}}"
{{cookiecutter.env_prefix}}API_DATA_DIR="/var/lib/{{cookiecutter.project_slug}}"

# {{cookiecutter.env_prefix}}API_VERSION="1"
# {{cookiecutter.env_prefix}}API_PREFIX="/api/v{api_version}"
# {{cookiecutter.env_prefix}}API_DOCS_ENABLED=true
# {{cookiecutter.env_prefix}}API_DOCS_OPENAPI_URL="{api_prefix}/openapi.json"
# {{cookiecutter.env_prefix}}API_DOCS_DOCS_URL="{api_prefix}/docs"
# {{cookiecutter.env_prefix}}API_DOCS_REDOC_URL="{api_prefix}/redoc"



## -- Docker build args -- ##
# HASH_PASSWORD="\$5\$UN1S7dZEa/qDoijJ\$hJ5o.Wpp5aP2kp.46Y7lWgcsRE8/oRLVswU6Swi13fB"
# IMG_ARGS="--build-arg HASH_PASSWORD=${HASH_PASSWORD}"
```

## 🔧 Command arguments

You can customize the command arguments to debug or run the service with different commands.

[**`compose.override.yml`**](https://github.com/{{cookiecutter.repo_owner}}/{{cookiecutter.repo_name}}/blob/main/templates/compose/compose.override.dev.yml):

```yml
    command: ["/bin/bash"]
    command: ["-b", "pwd && ls -al && /bin/bash"]
    command: ["-b", "python -u -m api"]
    command: ["-b", "uvicorn main:app --host=0.0.0.0 --port={% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_PORT:-8000} --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips='*'"]
```
