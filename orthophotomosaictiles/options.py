#!/usr/bin/env python3

################################################################################
#### Options ###################################################################
################################################################################

options = None

class OptionsError(Exception):
    pass

class OptionMismatch(Exception):
    pass

def checkOptions():
    global options
    if options is None:
        options = Options()
    return options
    
def getOptions():
    global options
    return options

class Options:
    _default_outfolder = None
    _default_suffix = 'png'

    def __init__(self):
        self.sources = []
        self.overwrite = False
        self.outfolder = None
        self.suffix = None

        self.scale = None
        self.length = None
        self.height = None

        self.stdout = True
        self.debug = False
        self.logfile = None
        self.logfiledebug = None
        self.timestamp = False
       
        self.show = False

        self.read()
        self.validate()

    def getOutput(self):
        return self.data[0]

    def getVersion(self):
        from .version import __version__
        return __version__

    def showVersion(self):
        from sys import exit
        print('Version: {}'.format(self.getVersion()))
        exit()

    def usage(self, unknown = None):
        from os.path import basename
        from sys import argv, exit
        if unknown:
            print(('Unknown option ' + unknown))
        print(('''Usage for %(cmdname)s
 %(cmdname)s [options]
- Options ------\ 
  -o            | Overwrite
  -d folder     | Output folder, default folder of filename
                |____________________________________________________________
  --scale fac   | Shrink image by scale fac
  --scalel px   | Fit longest side into length px
  --scaleh px   | Fit height into length px
                |____________________________________________________________
  --show        | Show temp labelled image (and skip saving)
  --log  file   | Log to file
  --logd file   | Log to file and enforce debugging on this log handler
  -v            | Verbose, show messages on stdout
  -q            | Quiet
  --debug       | Log debugging messages
  --version     | Show library version: %(version)s
  -h            | Display help
                \____________________________________________________________''' % { 
            'cmdname': basename(argv[0]),
            'default_suffix': self._default_suffix,
            'version': self.getVersion()
        }))
        exit()

    def read(self):
        from sys import argv
        from os.path import exists
        args = argv[1:]
        while (len(args) > 0):
            argument = args.pop(0).rstrip()
            if   (argument == '-h'):  self.usage()
            elif (argument == '--version'):  self.showVersion()
            # Logging
            elif (argument == '-v'):  self.stdout = True
            elif (argument == '-q'):  self.stdout = False
            elif (argument == '--debug'):  self.debug = True
            elif (argument == '--log'):  self.logfile = args.pop(0).rstrip()
            elif (argument == '--logd'): self.logfiledebug = args.pop(0).rstrip()
            # Show
            elif (argument == '--show'):  self.show = True
            # Scaling
            elif (argument == '--scale'):  self.scale = float(args.pop(0).rstrip())
            elif (argument == '--scalel'): self.length = int(args.pop(0).rstrip())
            elif (argument == '--scaleh'): self.height = int(args.pop(0).rstrip())
            # Specifics
            elif (argument == '-o'):  self.overwrite = True
            elif (argument == '-d'):  self.outfolder = args.pop(0).rstrip()
            # Other / unknown
            elif (argument.startswith('-')): self.usage(unknown = argument)
            else:
                self.sources.append(argument)

        if len(self.sources) == 0:
            raise OptionsError('No files provided')

    def validate(self):
        """ Check the provided options are valid """
        if len(self.data) == 0:
            raise OptionsError('No data file provided')
        return True

        



