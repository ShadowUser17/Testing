#!/usr/bin/env python3
import pathlib
import jinja2

data = [
    {
        "host": "127.0.0.1",
        "port": "5506"
    },
    {
        "host": "127.0.0.1",
        "port": "5507"
    },
    {
        "host": "127.0.0.1",
        "port": "5508"
    },
]


raw = pathlib.Path('template.j2')
example = jinja2.Template(raw.read_text())
print(example.render(data=data))
