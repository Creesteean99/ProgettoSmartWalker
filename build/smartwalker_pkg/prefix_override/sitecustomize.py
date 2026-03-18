import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/crist/smartwalker_ws/install/smartwalker_pkg'
