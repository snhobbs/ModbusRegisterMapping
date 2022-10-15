#!/usr/bin/env python3
import errno
import click
import copy
from jinja2 import Template, Environment, FileSystemLoader
import modbus_generator
import sys, os
import pandas as pd
import numpy as np
import math
import datetime
from os import path

def get_data_type_register_count(dtype, length):
    bytes = 0
    for bit_length in [8, 16, 32, 64]:
        if str(bit_length) in dtype:
            bytes = bit_length//8 * length
    if dtype == "string":
        bytes = length
    return int(math.ceil(bytes/2))

def clean_df(schema):
    schema.columns = schema.columns.str.strip()
    schema.address = [int(pt, base=16) for pt in schema.address if isinstance(pt, str)]
    schema["ctype"] = schema["data type"]
    schema.ctype.replace("string", "uint8", inplace=True)
    for pt in ["int8", "int16", "int32", "int64"]:
        for sign in ["", "u"]:
            schema["data type"].replace(sign+pt, sign+pt+"_t", inplace=True)
            schema["ctype"].replace(sign+pt, sign+pt+"_t", inplace=True)

    for entry_type in schema.type.unique():
        dt = schema[schema["type"] == entry_type]
        # fill register count
        for i, line in dt.iterrows():
            expected_length = get_data_type_register_count(line["data type"], line["length"])
            if line["register count"] == np.nan:
                line["register count"] = expected_length
            elif line["register count"] < expected_length:
                raise ValueError(f"Error in line {i}: Register Count set too low {line['register count']} expected {expected_length}")

        # fill addresses
        for i, line in dt.iterrows():
            highest_unused_address_line = dt[dt.address == max(dt.address)].first
            end_position = line["address"] + line["register count"] - 1
            if line["address"] == np.nan:
                line["address"] == highest_unused_address_line.address + highest_unused_address_line["register_count"]
            for j,  compare_line in dt.iterrows():
                position = compare_line.address
                if i == j:
                    continue # skip the same line case
                if line["address"] == position or end_position==position:
                    raise ValueError(f"Error in line {i}: Address equals that of line {j}")
                if line["address"] <= position and end_position > position:
                    raise ValueError(f"Error in line {i}: Address of line {j} is in data space")
    return schema



@click.command()
@click.option('--file', '-f', type=str, required=True, help='Single device description file')
@click.option('--cpp', '-c', is_flag=True, help='cpp list of objects')
@click.option('--python', '-p', is_flag=True, help='Python list of objects')
@click.option('--csv', is_flag=True, help='Output formated CSV')
@click.option('--md', is_flag=True, help='Markdown Documentation')
@click.option('--test_master', '-t', is_flag=True, help='Generate corresponding test files for the languages chosen')
def main(**kwargs):
    '''
    csv format:
        + name: tag of entry
        + type: function type one of "input register", "holding register"...
        + data type: type needed to print the value in a sensible way. [ctype, string, compound type...]
        + length: Length of array of data type [string is a list of chars]
        + address: Modbus address
        + register counts: number of Modbus registers (16 bit)
        + ctype: storage type [uint8_t, uint32_t, ...]
    '''

    fname = kwargs.pop("file")
    schema = pd.read_csv(fname, skipinitialspace = True)
    '''
    try:
        schema = clean_df(pd.read_csv(fname, skipinitialspace = True))
    except (FileNotFoundError):
        print("Schema file %s not found"%fname)
        return errno.ENOENT
    '''

    timestamp = datetime.datetime.now()

    if kwargs["python"]:
        template_name =  "ModbusEntryDict.py.j2"
        template = modbus_generator.get_template("", template_name)
        entries = [p for _, p in schema.iterrows()]
        rendering = template.render(entries=entries)
        with open("modbus_server_objects.py", 'w') as f:
            f.write(rendering)

    if kwargs["cpp"]:
        template = modbus_generator.get_template("cpp", "ModbusBasicServer.h.j2")
        for entry_type in schema.type.unique():
            lines = [pt for _, pt in list(schema[schema.type == entry_type].iterrows())]
            entry_type = entry_type.replace(" ", "_")
            lines = [pt for pt in lines if pt["name"] != "UNUSED"]
            rendering = template.render(entries=lines, name=entry_type, timestamp=timestamp)
            fname = f"modbus_basic_server_{entry_type}.h"
            with open(fname, 'w') as f:
                f.write(rendering)
            os.system("clang-format %s -i --style=Google"%fname)
        template_name =  "modbus_server_objects.h.j2"
        template = modbus_generator.get_template("cpp", template_name)
        fname = template_name.strip(".j2")
        entries = [p for _, p in schema.iterrows()]
        rendering = template.render(entries=entries, name=entry_type, timestamp=timestamp)
        with open(fname, 'w') as f:
            f.write(rendering)
        os.system("clang-format %s -i --style=Google"%fname)

    if kwargs["md"]:
        # "0x3%05x"
        template_name = "RegisterMap.md.j2"
        template = modbus_generator.get_template("", template_name)
        model = {}
        for entry_type in schema.type.unique():
            model[entry_type] = [pt for _, pt in list(schema[schema.type == entry_type].iterrows())]
        title="Modbus RTU Register Map"
        rendering = template.render(schema=model, timestamp=timestamp, title=title)
        with open(template_name.strip(".j2"), 'w') as f:
            f.write(rendering)

    if kwargs["csv"]:
        fname = "ModbusRegisterMap.csv"
        schema.to_csv(fname)

#@click.option('--test_master', '-t', is_flag=True, help='Generate corresponding test files for the languages chosen')

    return

if __name__ == "__main__":
    main()
