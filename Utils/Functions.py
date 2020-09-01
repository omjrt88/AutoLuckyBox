import inspect
import re

def getProperty(modelObj, key):
    try:
        if "." in key:
            keys = key.split(".")
            root = inspectMethod(modelObj)[keys[0]]
            del keys[0]
            keys = '.'.join(keys)
            return getProperty(root, keys)
        value = inspectMethod(modelObj)[key]
        return '' if value is None else value
    except KeyError:
        return None

def inspectMethod(root):
    if isinstance(root, dict):
        return root
    return dict(inspect.getmembers(root))

def removeWhiteSpaces(myString):
    return re.sub(' +',' ', myString.replace('\n', '').strip())

def stringClear(myString):
    return myString.lower().strip().replace("'", "")

def str2bool(myBool):
    if isinstance(myBool, bool):
        return myBool
    if isinstance(myBool, str):
        return eval(myBool)