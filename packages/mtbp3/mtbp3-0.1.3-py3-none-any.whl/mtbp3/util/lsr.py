
#  Copyright (C) 2023 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>


import os
import json
import pandas as pd

def lsr_tree(path: str = "", outfmt: str = "list",  nopre: bool = False):
    """
    Recursively lists the directory tree structure starting from the given path.

    Args:
        path (str, optional): The path to start listing from. Defaults to current directory.
        outfmt (str, optional): The output format. Can be 'list', 'json', 'dataframe', or 'string'. Defaults to 'list'.
        nopre (bool, optional): Flag to disable prefixes. Defaults to False.

    Returns:
        list or str or json: The directory tree structure in the specified output format.

    Example:
        >>> lsr_tree(".")
        ['mtbp3/__init__.py', 'mtbp3/main.py']

    """

    if not os.path.exists(path):
        print(f"Path '{path}' does not exist.")
        return

    if nopre == True:
        pre0 = " "
        pre1 = " "

    assert outfmt in ["list", "json", "string","dataframe"], "Invalid output format. Must be one of 'list', 'json', 'string', or 'dataframe'."

    if outfmt == "json":
        data = {}
        idx = 0
        for s0, d0, f0 in os.walk(path):
            s0 = s0.replace(path, "")
            n0 = s0.count(os.sep)
            data[idx] = {"path": s0, "level": n0, "folders": d0, "files": f0}
            idx = idx+1
        return json.dumps(data)
    elif outfmt == "list": 
        files = []
        for s0, d0, f0 in os.walk(path):
            s0 = s0.replace(path, "")
            for f1 in f0:
                files.append(os.path.join(s0, f1))
            if len(f0) == 0 and len(d0) == 0:
                files.append(s0+"/(((empty folder)))")
        return files
    elif outfmt == "dataframe":
        data = []
        for s0, d0, f0 in os.walk(path):
            s1 = s0.replace(path, "")
            level = s1.count(os.sep) 
            if len(f0) > 0:
                type = "file"
                for f1 in f0:
                    data.append((s1, level+1, type, f1))
            elif len(d0) == 0:
                type = "folder"
                data.append((s1, level, "folder", "(((empty folder)))"))

        df = pd.DataFrame(data, columns=["path", "level", "type", "file"])
        return df 
    else:
        out0 = []
        for s0, d0, f0 in os.walk(path):
            s1 = s0.replace(path, "")
            level = s1.count(os.sep)
            if level == 0:
                s1 = s0
            indent = "... " * (level)
            out0.append(f"{indent}{os.path.basename(s1)}/")
            subindent = "... " * (level + 1)
            for f1 in f0:
                out0.append(f"{subindent}{f1}")
            if len(f0) == 0 and len(d0) == 0:
                out0.append(f"{subindent}(((empty folder)))") 

        return "\n".join(out0)


