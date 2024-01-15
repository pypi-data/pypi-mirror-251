# Webshell Generator

Webshell Generator is a Python library for generating processed webshell instances.

## Installation

```bash
pip install webshell_generator
```

## Usage

```python
from webshell_generator import get_godzilla_jsp_shell

webshell = get_godzilla_jsp_shell()
print(webshell.tool)
# godzilla
print(webshell.type)
# jsp
print(webshell.mode)
# java_aes_base64
print(webshell.pas)
# pass
print(webshell.key)
# key
print(webshell.raw_content)
# [raw godzilla jsp webshell]
print(webshell.content)
# [unicode-encoding godzilla jsp webshell]
```
