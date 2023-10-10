ARG BASE_IMAGE=debian:12.1-slim
ARG DEBIAN_FRONTEND=noninteractive

ARG FASTAPI_TEMPLATE_APP_DIR="/app/fastapi-template"
ARG FASTAPI_TEMPLATE_DATA_DIR="/var/lib/fastapi-template"
ARG FASTAPI_TEMPLATE_LOGS_DIR="/var/log/fastapi-template"


# Here is the builder image
# hadolint ignore=DL3006
FROM ${BASE_IMAGE} as builder

ARG DEBIAN_FRONTEND

# ARG USE_GPU=false
ARG PYTHON_VERSION=3.9.18

# Set the SHELL to bash with pipefail option
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# hadolint ignore=DL3008
RUN _BUILD_TARGET_ARCH=$(uname -m) && \
	echo "BUILDING TARGET ARCHITECTURE: ${_BUILD_TARGET_ARCH}" && \
	rm -rfv /var/lib/apt/lists/* /var/cache/apt/archives/* /tmp/* /root/.cache/* && \
	apt-get clean -y && \
	apt-get update --fix-missing -o Acquire::CompressionTypes::Order::=gz && \
	apt-get install -y --no-install-recommends \
		ca-certificates \
		build-essential \
		wget && \
	if [ "${_BUILD_TARGET_ARCH}" == "x86_64" ]; then \
		export _MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-py39_23.5.2-0-Linux-x86_64.sh; \
	elif [ "${_BUILD_TARGET_ARCH}" == "aarch64" ]; then \
		export _MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-py39_23.5.2-0-Linux-aarch64.sh; \
		# export _MINICONDA_URL=https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge-pypy3-Linux-aarch64.sh; \
	else \
		echo "Unsupported platform: ${_BUILD_TARGET_ARCH}" && \
		exit 1; \
	fi && \
	wget -nv --show-progress --progress=bar:force:noscroll "${_MINICONDA_URL}" -O /root/miniconda.sh && \
	/bin/bash /root/miniconda.sh -b -u -p /opt/conda && \
	/opt/conda/condabin/conda clean -y -av && \
	/opt/conda/condabin/conda update -y conda && \
	/opt/conda/condabin/conda install -y python=${PYTHON_VERSION} pip && \
	/opt/conda/bin/pip install --timeout 60 --no-cache-dir -U pip && \
	/opt/conda/bin/pip cache purge && \
	/opt/conda/condabin/conda clean -y -av

COPY ./requirements*.txt /
RUN	_BUILD_TARGET_ARCH=$(uname -m) && \
	# if [ "${_BUILD_TARGET_ARCH}" == "x86_64" ] && [ "${USE_GPU}" == "false" ]; then \
	# 	export _REQUIRE_FILENAME=requirements.amd64.txt; \
	# elif [ "${_BUILD_TARGET_ARCH}" == "x86_64" ] && [ "${USE_GPU}" == "true" ]; then \
	# 	export _REQUIRE_FILENAME=requirements.gpu.txt; \
	# elif [ "${_BUILD_TARGET_ARCH}" == "aarch64" ]; then \
	# 	export _REQUIRE_FILENAME=requirements.arm64.txt; \
	# fi && \
	# /opt/conda/bin/pip install --timeout 60 --no-cache-dir -r "./${_REQUIRE_FILENAME}" && \
	/opt/conda/bin/pip install --timeout 60 --no-cache-dir -r ./requirements.txt && \
	/opt/conda/bin/pip cache purge && \
	/opt/conda/condabin/conda clean -y -av


# Here is the base image
# hadolint ignore=DL3006
FROM ${BASE_IMAGE} as base

ARG DEBIAN_FRONTEND
ARG FASTAPI_TEMPLATE_APP_DIR
ARG FASTAPI_TEMPLATE_DATA_DIR
ARG FASTAPI_TEMPLATE_LOGS_DIR

# CHANGEME: Change hashed password:
ARG HASH_PASSWORD="\$1\$K4Iyj0KF\$SyXMbO1NTSeKzng1TBzHt."
ARG UID=1000
ARG GID=11000
ARG USER=ft-user
ARG GROUP=ft-group

ENV UID=${UID} \
	GID=${GID} \
	USER=${USER} \
	GROUP=${GROUP} \
	FASTAPI_TEMPLATE_APP_DIR=${FASTAPI_TEMPLATE_APP_DIR} \
	FASTAPI_TEMPLATE_DATA_DIR=${FASTAPI_TEMPLATE_DATA_DIR} \
	FASTAPI_TEMPLATE_LOGS_DIR=${FASTAPI_TEMPLATE_LOGS_DIR}

ENV	PYTHONIOENCODING=utf-8 \
	PATH=/opt/conda/bin:${PATH}

# Set the SHELL to bash with pipefail option
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Installing system dependencies
# hadolint ignore=DL3008
RUN rm -rfv /var/lib/apt/lists/* /var/cache/apt/archives/* /tmp/* /root/.cache/* && \
	apt-get clean -y && \
	apt-get update --fix-missing -o Acquire::CompressionTypes::Order::=gz && \
	apt-get install -y --no-install-recommends \
		sudo \
		locales \
		tzdata \
		procps \
		iputils-ping \
		net-tools \
		curl \
		nano && \
	apt-get clean -y && \
	sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
	sed -i -e 's/# en_AU.UTF-8 UTF-8/en_AU.UTF-8 UTF-8/' /etc/locale.gen && \
	dpkg-reconfigure --frontend=noninteractive locales && \
	update-locale LANG=en_US.UTF-8 && \
	echo "LANGUAGE=en_US.UTF-8" >> /etc/default/locale && \
	echo "LC_ALL=en_US.UTF-8" >> /etc/default/locale && \
	addgroup --gid ${GID} ${GROUP} && \
	useradd -l -m -d /home/${USER} -s /bin/bash -g ${GROUP} -G sudo -u ${UID} ${USER} && \
	echo "${USER} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${USER} && \
	chmod 0440 /etc/sudoers.d/${USER} && \
	echo -e "${USER}:${HASH_PASSWORD}" | chpasswd -e && \
	echo -e "\numask 0002" >> /home/${USER}/.bashrc && \
	echo "alias ls='ls -aF --group-directories-first --color=auto'" >> /home/${USER}/.bashrc && \
	echo -e "alias ll='ls -alhF --group-directories-first --color=auto'\n" >> /home/${USER}/.bashrc && \
	echo ". /opt/conda/etc/profile.d/conda.sh" >> /home/${USER}/.bashrc && \
	echo "conda activate base" >> /home/${USER}/.bashrc && \
	mkdir -pv ${FASTAPI_TEMPLATE_APP_DIR} ${FASTAPI_TEMPLATE_DATA_DIR} ${FASTAPI_TEMPLATE_LOGS_DIR} && \
	chown -Rc "${USER}:${GROUP}" ${FASTAPI_TEMPLATE_APP_DIR} ${FASTAPI_TEMPLATE_DATA_DIR} ${FASTAPI_TEMPLATE_LOGS_DIR} && \
	find ${FASTAPI_TEMPLATE_APP_DIR} ${FASTAPI_TEMPLATE_DATA_DIR} -type d -exec chmod -c 770 {} + && \
	find ${FASTAPI_TEMPLATE_APP_DIR} ${FASTAPI_TEMPLATE_DATA_DIR} -type d -exec chmod -c ug+s {} + && \
	find ${FASTAPI_TEMPLATE_LOGS_DIR} -type d -exec chmod -c 775 {} + && \
	find ${FASTAPI_TEMPLATE_LOGS_DIR} -type d -exec chmod -c +s {} + && \
	rm -rfv /var/lib/apt/lists/* /var/cache/apt/archives/* /tmp/* /root/.cache/* /home/${USER}/.cache/*

ENV LANG=en_US.UTF-8 \
	LANGUAGE=en_US.UTF-8 \
	LC_ALL=en_US.UTF-8

COPY --from=builder --chown=${UID}:${GID} /opt /opt


# Here is the production image
# hadolint ignore=DL3006
FROM base as app

WORKDIR ${FASTAPI_TEMPLATE_APP_DIR}
COPY --chown=${UID}:${GID} ./app ${FASTAPI_TEMPLATE_APP_DIR}
COPY --chown=${UID}:${GID} --chmod=770 ./scripts/docker/*.sh /usr/local/bin/

# VOLUME ${FASTAPI_TEMPLATE_DATA_DIR}

USER ${UID}:${GID}
ENTRYPOINT ["docker-entrypoint.sh"]
# CMD ["-b", "sleep 1 && uvicorn main:app --host=0.0.0.0 --port='${FASTAPI_TEMPLATE_PORT:-8000}' --no-server-header --proxy-headers --forwarded-allow-ips='*' --no-access-log"]
