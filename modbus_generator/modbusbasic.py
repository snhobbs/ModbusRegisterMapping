from jinja2 import Template, Environment, FileSystemLoader

def MakeHeader(template_directory, entries, fname, namespace):
    env = Environment(loader=FileSystemLoader(template_directory))
    data_store_template = "MappedDataStore.h.j2"
    template = env.get_template(data_store_template)
    rendering = template.render(entries=entries, namespace=namespace, fname=fname, timestamp=datetime.datetime.now())
    with open(fname, 'w') as f:
        f.write(rendering)
    os.system("clang-format %s -i --style=Google"%fname)

def MakeMap(template_directory, entries, fname, title):
    env = Environment(loader=FileSystemLoader(template_directory))
    register_map_template = "RegisterMap.md.j2"
    template = env.get_template(register_map_template)
    rendering = template.render(entries=entries, title=title)
    with open(fname, 'w') as f:
        f.write(rendering)


