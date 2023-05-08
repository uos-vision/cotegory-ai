import os
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