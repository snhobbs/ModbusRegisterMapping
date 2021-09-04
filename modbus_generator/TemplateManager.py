import pkg_resources, jinja2
import os

def get_template(*args):
    template_bytes = pkg_resources.resource_string(__name__, os.path.join("../", "share", "modbus_generator", "templates", *args))
    template_str = template_bytes.decode("utf-8")
    return jinja2.Template(template_str)

