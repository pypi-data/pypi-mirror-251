import os
import warnings
import numpy as np

def prepend_zeros_to_filename(path, sep="_", n=5):
    """
    helper function for numeric file names which need to be filled with zeros for
    sorting

    path    path to be edited, can also be a filename only
    n       number of characters of filename after editing

    Examples:

    # get a list of images
    files = glob.glob("test/*.jpg")
    temp_sorted = [prepend_zeros_to_filename(f, n=3) for f in files]
    files_sorted = [i for _, i in sorted(zip(temp_sorted, files))]

    """
    directory, file = os.path.split(path)
    filename, ext = os.path.splitext(file)

    parts = filename.split(sep)
    parts_new = []
    for p in parts:
        try:
            p_int = int(p)
            # test if n is large enough for the changed integer
            if p_int == 0:
                base_n = 0
            else:
                base_n = np.log10(p_int)
            if base_n >= n:
                min_n = int(np.floor(base_n) + 1)
                raise warnings.warn(f"set n >= {min_n} to prepend zeros to {p_int}")
            else:
                p_new = p.zfill(n)
        except:
            p_new = p

        parts_new.append(p_new)
        file_new = "".join([sep.join(parts_new), ext])

    return os.path.join(directory, file_new)