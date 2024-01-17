import re
image_regex = re.compile(r"^(?:(?=[^:\/]{1,253})(?!-)[a-zA-Z0-9-]{1,63}(?<!-)(?:\.(?!-)[a-zA-Z0-9-]{1,63}(?<!-))*(?::[0-9]{1,5})?/)?((?![._-])(?:[a-z0-9._-]*)(?<![._-])(?:/(?![._-])[a-z0-9._-]*(?<![._-]))*)(?::(?![.-])[a-zA-Z0-9_.-]{1,128})?$")
path_regex = re.compile(r"^([\/]{1}[a-zA-Z0-9.]+)+(\/?){1}$|^([\/]{1})$")
env_name_regex = re.compile(r"^[-._a-zA-Z][-._a-zA-Z0-9]*$")
container_name_regex = re.compile(r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$")
label_regex = re.compile(r"^(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])?$")
# replace \p{Han} with \u4e00-\u9fff
description_regex = re.compile(r"^[a-zA-Z0-9_.,\-\/\u4e00-\u9fff，。 ]{3,253}$")
email_regex = re.compile(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")

def is_valid_description(text):
    return description_regex.search(text)

def is_valid_label(text):
    return label_regex.search(text)

def is_valid_env_name(name):
    return env_name_regex.search(name)

def is_valid_container_name(name):
    return container_name_regex.search(name)

def is_image_name(image_name) -> bool:
    return image_regex.search(image_name)

def is_valid_path(path:str) -> bool:
    return path_regex.search(path)

def is_valid_email(email:str) -> bool:
    return email_regex.search(email)
