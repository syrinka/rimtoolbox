import sys
from rimtoolbox.parser import Workspace, Path

if __name__ == '__main__':
    w = Workspace()
    for i in sys.argv[1:-1]:
        w.digest_dir(i)
    w.solve_inherit()
    w.inject_langdata(ignore_extra=True)
    w.clean()
    w.dump(sys.argv[-1], indent=4)