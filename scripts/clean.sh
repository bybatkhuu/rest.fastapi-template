#!/bin/bash
set -euo pipefail

## --- Base --- ##
# Getting path of this script file:
_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
_PROJECT_DIR="$(cd "${_SCRIPT_DIR}/.." >/dev/null 2>&1 && pwd)"
cd "${_PROJECT_DIR}" || exit 2

# Loading base script:
# shellcheck disable=SC1091
source "${_SCRIPT_DIR}/base.sh"

# Loading .env file:
if [ -f ".env" ]; then
	# shellcheck disable=SC1091
	source .env
fi
## --- Base --- ##


## --- Main --- ##
main()
{
	echoInfo "Cleaning 'rest.fastapi'..."
	if docker compose ps | grep 'Up' > /dev/null 2>&1; then
		echoError "FastAPI is running. Please stop it before cleaning."
		exit 1
	fi

	rm -rfv ./volumes/storage/fastapi/data/* ./volumes/storage/fastapi/logs/* || exit 2
	echoOk "Done."
}

main "${@:-}"
## --- Main --- ##
