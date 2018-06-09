NOPYTHON = false
PYTHON = python
ifeq ($(shell which python3),)
	python_version_full := $(wordlist 2,4,$(subst ., ,$(shell python --version 2>&1)))
	python_version_major := $(word 1,${python_version_full})
	NOPYTHON = true
	ifeq ( $(python_version_major), 3 )
		NOPYTHON = false
		PYTHON = python
		PYTHON-PIP = pip
	endif
else
	PYTHON = python3
	PYTHON-PIP = pip3
endif

help:
	@echo "make prepare"
	@echo "    prepare development environment, use only once"
	@echo "make install"
	@echo "    install all python requirements, use only once"
	@echo "make start"
	@echo "    start the analysis"
	@echo "make start-and-save"
	@echo "    start the analysis and save some graphs"
	@echo "make start-and-save-all"
	@echo "    start the analysis and save all the graphs"

prepare:
	sudo apt-get install python3
	sudo apt-get install python3-tk
	sudo apt-get install python3-pip

install: check_version
	${PYTHON-PIP} install -r requirements.txt
	
check_version:
	@if [ ${NOPYTHON} = false ]; \
		then ${PYTHON} --version; \
		else \
			echo "Sorry :( THIS PROJECT NEEDS PYTHON3!"; \
			echo "Your current version: "; \
			${PYTHON} --version; \
			echo "> Running 'make prepare' to install python3, python3-tk and python3-pip for you!"; \
			make prepare; \
			make install; \
			echo "> Trying again . . ."; \
	fi

start: check_version
	${PYTHON} -W ignore main.py

start-and-plot: check_version
	${PYTHON} -W ignore main.py -vb

start-and-plot-all: check_version
	${PYTHON} -W ignore main.py -vvb

.PHONY : all
.DEFAULT: help
