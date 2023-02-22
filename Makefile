.PHONY: load upload preproc semantify help
.DEFAULT_GOAL := help


define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help: ## dataset availabe for make icews, lei, country
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

load: ## load data and name of the dataset (e.g. make load data=icews )
	python src/$(data)_data.py --load_data 

upload: ## upload data and name of the dataset (e.g. make upload data=icews )
	python src/$(data)_data.py --upload_data

preproc: ## preprocess data and name of the dataset (e.g. make preproc data=icews )
	python src/$(data)_data.py --preproc_data

semantify: ## semantify data or create rdf KG and name of the dataset ( e.g. make semantify data=icews )
	python src/$(data)_data.py --config_file=configs/config.ini
	# python src/$(data)_data.py --config_file=configs/$(data)_config.ini







