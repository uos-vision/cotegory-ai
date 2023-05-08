import os
from enum import Enum
class StrEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
def call_pre_path(dir,file_name, src = None):
    link_path = os.path.join(dir,file_name)

    if src is not None:
        if os.path.islink(link_path):
            os.unlink(link_path)
        path = os.path.join(dir,src)
        os.symlink(path, link_path)

    try:
        ret_path = os.readlink(link_path)
    except:
        ret_path = None

    return ret_path