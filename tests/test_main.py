import os
import sys
sys.path.append(os.sep.join([os.path.dirname(os.path.realpath(__file__)),
                             '..',
                             'src'
                             ]))
import main # noqa

main.import_settings()
main.main()
