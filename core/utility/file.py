import os
import shutil

def create_dir(dir: str, only_check: bool = True) -> None:
    """
    Create a directory at the specified path.

    If the directory already exists:
      - If `only_check` is True (default), the function does nothing.
      - If `only_check` is False, it removes the existing directory and its contents before creating a new one.

    Args
    ----
    `dir` : The path of the directory to create. This can be either a full path or a relative path.\n
    `only_check` : The flag to specify removing strategy when dir is already existed.
    """
    
    if os.path.exists(dir):
        if only_check:
            return
        else:
            shutil.rmtree(dir)    
    os.makedirs(dir)
