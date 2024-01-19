import configparser

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def intfloatstr(x):
    try:
        return int(x)
    except ValueError:
        return float(x)
    except ValueError:
        return str(x)
    
converters = {
    'list': lambda x: x if " " not in x else [i.strip() for i in x.split(' ')],
    'strint': lambda x: int(x) if x.isdigit() else x,
    'strfloat': lambda x: float(x) if is_number(x) else x,
    'intfloatstr': intfloatstr,
}
# usage:
# config = configparser.ConfigParser(converters=converters)

def parse_section_as_dict(section, method: str="intfloatstr"):
    """
    method can be one of 'strint' (mix of string and integers) or "list"
    if lists are also in the section
    TODO: check out pydantic for interactions with config files (.cfg, .json) 
          with classes
    """
    getter = getattr(section, f"get{method}")
    return {k:getter(k) for k in section.keys()}