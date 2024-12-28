#!/bin/bash
set -euo pipefail


echo "INFO: Running '{{cookiecutter.project_slug}}' docker-entrypoint.sh..."

_doStart()
{
	exec python -u ./main.py || exit 2
	# exec uvicorn main:app --host=0.0.0.0 --port={% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_PORT:-8000} --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips='*' || exit 2
	exit 0
}


main()
{
	umask 0002 || exit 2
	sudo chown -Rc "${USER}:${GROUP}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}HOME_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DATA_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_LOGS_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_TMP_DIR}" || exit 2
	find "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DATA_DIR}" -type d -exec chmod 770 {} + || exit 2
	find "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DATA_DIR}" -type f -not -path "*/scripts/*" -not -path "*/main.py" -exec chmod 660 {} + || exit 2
	find "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DATA_DIR}" -type d -exec chmod ug+s {} + || exit 2
	find "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_LOGS_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_TMP_DIR}" -type d -exec chmod 775 {} + || exit 2
	find "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_LOGS_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_TMP_DIR}" -type f -exec chmod 664 {} + || exit 2
	find "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_LOGS_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_TMP_DIR}" -type d -exec chmod +s {} + || exit 2
	chmod ug+x "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DIR}/main.py" || exit 2
	# echo "${USER} ALL=(ALL) ALL" | sudo tee -a "/etc/sudoers.d/${USER}" > /dev/null || exit 2
	echo ""

	## Parsing input:
	case ${1:-} in
		"" | -s | --start | start | --run | run)
			_doStart;;
			# shift;;
		-b | --bash | bash | /bin/bash)
			shift
			if [ -z "${*:-}" ]; then
				echo "INFO: Starting bash..."
				/bin/bash
			else
				echo "INFO: Executing command -> ${*}"
				exec /bin/bash -c "${@}" || exit 2
			fi
			exit 0;;
		*)
			echo "ERROR: Failed to parsing input -> ${*}"
			echo "USAGE: ${0}  -s, --start, start | -b, --bash, bash, /bin/bash"
			exit 1;;
	esac
}

main "${@:-}"
