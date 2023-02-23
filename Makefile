.PHONY: load upload preproc semantify help clean
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
	mkdir -p data/$(data)
	python src/$(data).py --load_data 

upload: ## upload data and name of the dataset (e.g. make upload data=icews )
	python src/$(data).py --upload_data

preproc: ## preprocess data and name of the dataset (e.g. make preproc data=icews )
	python src/$(data).py --preproc_data

semantify: ## semantify data or create rdf KG and name of the dataset ( e.g. make semantify data=icews )
	mkdir -p kgdata/${data}
	python src/$(data).py --config_file=configs/$(data).ini

clean_kg: ## delete sematified data ( e.g. make clean_kg data=icews )
	rm -rf kgdata/$(data).nt

clean_data: ## delete downloaded data ( e.g. make clean_data data=icews )
	rm -rf data/$(data)







