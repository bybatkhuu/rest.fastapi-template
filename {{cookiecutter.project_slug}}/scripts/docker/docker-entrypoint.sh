#!/bin/bash
set -euo pipefail


_doStart()
{
	sleep 1
	python -u main.py || exit 2
	# uvicorn main:app --host=0.0.0.0 --port='{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}APP_PORT:-8000}' --no-server-header --proxy-headers --forwarded-allow-ips='*' --no-access-log || exit 2
	exit 0
}


main()
{
	sudo chown -Rc "${USER}:${GROUP}" "${APP_DIR}" "${DATA_DIR}" "${LOGS_DIR}" || exit 2
	find "${APP_DIR}" "${DATA_DIR}" -type d -exec chmod 770 {} + || exit 2
	find "${APP_DIR}" "${DATA_DIR}" -type f -exec chmod 660 {} + || exit 2
	find "${APP_DIR}" "${DATA_DIR}" -type d -exec chmod ug+s {} + || exit 2
	find "${LOGS_DIR}" -type d -exec chmod 775 {} + || exit 2
	find "${LOGS_DIR}" -type f -exec chmod 664 {} + || exit 2
	find "${LOGS_DIR}" -type d -exec chmod +s {} + || exit 2
	chmod ug+x "${APP_DIR}/main.py" || exit 2
	echo "${USER} ALL=(ALL) ALL" | sudo tee -a "/etc/sudoers.d/${USER}" > /dev/null || exit 2
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
				/bin/bash -c "${@}" || exit 2
			fi
			exit 0;;
		*)
			echo "ERROR: Failed to parsing input -> ${*}"
			echo "USAGE: ${0} -s, --start, start | -b, --bash, bash, /bin/bash"
			exit 1;;
	esac
}

main "${@:-}"
