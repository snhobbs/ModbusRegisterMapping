from . import get_template
import datetime

def generate_flatbuffers_schema(schema, namespace=None):
    if namespace is None:
        namespace = ""

    template_name = "flatbuffers.fbs.j2"
    template = get_template(template_name)
    fname = template_name.strip(".j2")

    rendering = template.render(schema=schema, namespace=namespace, fname=fname, timestamp=datetime.datetime.now())
    with open(fname, 'w') as f:
        f.write(rendering)
