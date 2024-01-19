#!/usr/bin/python3

import sys
import getopt
import io
import json
import javaobj
import os
from os.path import exists
from javaobj import JavaObjectUnmarshaller


def seek_size(f):
    pos = f.tell()
    f.seek(0, io.SEEK_END)
    size = f.tell()
    f.seek(pos)
    return size


def show_help():
    print("J2J.py -i <inputfile> [-o <outputfile>]")
    print("J2J.py -s <FileOrDirectory>")


def deserialize(inputFile, outputFile):
    with open(inputFile, "rb") as fin:
        i = 0
        t = None

        fileSize = seek_size(fin)
        tmpObject = None

        marshaller = JavaObjectUnmarshaller(fin)

        try:
            tmpObject = marshaller.readObject(ignore_remaining_data=False)
            objectType = tmpObject.__str__()

            if objectType == "<javaobj:java.util.Properties>":
                properties = {}
                while fin.tell() != fileSize:
                    key = marshaller.readObject(ignore_remaining_data=True)
                    value = marshaller.readObject(ignore_remaining_data=True)
                    properties[key] = value

                if outputFile != "":
                    with open(outputFile, "w") as f:
                        json.dump(properties, f)
                else:
                    print(json.dumps(properties, indent=4))
            else:
                items = []
                for obj in marshaller.references:
                    str = obj.__str__()
                    if str.startswith("[") and str.endswith("]"):
                        continue
                    items.append(str)
                if outputFile != "":
                    with open(outputFile, "w") as f:
                        json.dump(items, f)
                else:
                    print(json.dumps(items, indent=4))

        except Exception:
            raise

        if fin.tell() != fileSize:
            print("error!")


deserialize("/Users/jteuwen/images/checkerboard.qpdata", "o.json")
