.PHONY: docs test pypi_package install all

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Create and update the documentation
docs:
	cd docsrc/ && make github

## Execute unit tests
test:
	pytest tests/

## Upload package to pypi
pypi_package:
	make install
	check-manifest
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload --skip-existing dist/*

## Run black linting
lint:
	pre-commit run --all-files

## Install visions locally
install:
	pip install -e .

## Install spark (for tests)
install-spark-ci:
	sudo apt-get update
	sudo apt-get -y install openjdk-8-jdk
	curl https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
	--output ${SPARK_DIRECTORY}/spark.tgz
	cd ${SPARK_DIRECTORY} && tar -xvzf spark.tgz && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} spark

## Plots
plots:
	cd src/visions/visualisation/
	python plot_circular_packing.py
	python plot_summary.py
	python plot_typesets.py

## lint, type check, install, rebuild docs, and finally test
all:
	make lint
	make install
	make plots
	make docs
	make test

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
