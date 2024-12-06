.PHONY: help validate start stop compose clean get-version test bump-version build docs changelog

help:
	@echo "make help         -- show this help"
	@echo "make validate     -- validate docker compose file"
	@echo "make start        -- start all services"
	@echo "make stop         -- stop all services"
	@echo "make compose      -- run docker-compose commands"
	@echo "make clean        -- clean all"
	@echo "make get-version  -- get current version"
	@echo "make test         -- run tests"
	@echo "make bump-version -- bump version"
	@echo "make build        -- build docker image"
	@echo "make docs         -- build documentation"
	@echo "make changelog    -- update changelog"

validate:
	./compose.sh validate

start:
	./compose.sh start -l

stop:
	./compose.sh down

compose:
	./compose.sh $(MAKEFLAGS)

clean:
	./scripts/clean.sh -a

get-version:
	./scripts/get-version.sh

test:
	./scripts/test.sh $(MAKEFLAGS)

bump-version:
	./scripts/bump-version.sh $(MAKEFLAGS)

build:
	./scripts/build.sh $(MAKEFLAGS)

docs:
	./scripts/docs.sh $(MAKEFLAGS)

changelog:
	./scripts/changelog.sh $(MAKEFLAGS)
