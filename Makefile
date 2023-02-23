.PHONY: load upload preproc semantify help clean-kg clean-data clean-all install
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

load: ## load data (e.g. make load data=icews )
	mkdir -p data/$(data)
	python src/$(data).py --load_data --load_path=data/$(data)

upload: ## upload data, location tib, skynet (e.g. make upload data=icews )
	python src/$(data).py --upload_data

preproc: ## preprocess data (e.g. make preproc data=icews )
	python src/$(data).py --preproc_data

semantify: ## semantify data or create rdf KG ( e.g. make semantify data=icews )
	mkdir -p kgdata/${data}
	python src/$(data).py --config_file=configs/$(data).ini

clean-kg: ## delete sematified data ( e.g. make clean-kg data=icews )
	cd kgdata && rm -rf $(data)

clean-data: ## delete downloaded data ( e.g. make clean-data data=icews )
	cd data && rm -rf $(data)

clean-all: clean-kg clean-data ## deleted downloaded data and rdf data (e.g. make clean-all data=icews)

install: ## install required packages
	pip install -r requirements.txt
	







