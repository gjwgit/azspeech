########################################################################
#
# Makefile for pre-built ML model
#
# Copyright (c) Graham.Williams@togaware.com
#
# License: Creative Commons Attribution-ShareAlike 4.0 International.
#
########################################################################

# App version numbers
#   Major release
#   Minor update
#   Trivial update or bug fix

APP=azspeech
DATE=$(shell date +%Y-%m-%d)

########################################################################
# Supported modules.

INC_BASE    = $(HOME)/.local/share/make
INC_PANDOC  = $(INC_BASE)/pandoc.mk
INC_GIT     = $(INC_BASE)/git.mk
INC_MLHUB   = $(INC_BASE)/mlhub.mk
INC_CLEAN   = $(INC_BASE)/clean.mk

ifneq ("$(wildcard $(INC_PANDOC))","")
  include $(INC_PANDOC)
endif
ifneq ("$(wildcard $(INC_GIT))","")
  include $(INC_GIT)
endif
ifneq ("$(wildcard $(INC_MLHUB))","")
  include $(INC_MLHUB)
endif
ifneq ("$(wildcard $(INC_CLEAN))","")
  include $(INC_CLEAN)
endif

define HELP
$(APP):

  install	Install locally over package install in ~/.mlhub/$(APP)
  private	Install private.json to ~/.mlhub/$(APP)

endef
export HELP

help::
	@echo "$$HELP"

install:
	install demo.py transcribe.py synthesize.py translate.py recognise.py $(HOME)/.mlhub/$(APP)/

private:
	install private.json $(HOME)/.mlhub/$(APP)/
