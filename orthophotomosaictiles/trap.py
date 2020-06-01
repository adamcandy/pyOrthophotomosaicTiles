#!/usr/bin/env python3

from .log import getLogger
log = getLogger()

################################################################################
#### Global variables ##########################################################
################################################################################

trapped = False

################################################################################
#### General routines ##########################################################
################################################################################

def signal_handler(signal, frame):
    from sys import exit
    global trapped
    if not trapped:
        trapped = True
        log.info('Ouch!')
    else:
        exit(1)

def isTrapped():
    global trapped
    return trapped

