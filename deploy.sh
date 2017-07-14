#!/bin/bash

#deploy bless
ansible-playbook \
	-e ansible_python_interpreter=$(which python) \
	-c local \
	-i localhost, \
	build_bless.yml
