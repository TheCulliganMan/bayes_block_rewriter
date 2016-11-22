#!/usr/bin/env python
from __future__ import print_function
import sys

def process_items(line_items):
    new_items = []
    current_slice_start = None
    current_index = 0
    prev_item = None

    while current_index < len(line_items):

        try:

            item = int(line_items[current_index])

            if not prev_item and not current_slice_start:

                current_slice_start = item
                prev_item = item

            else:

                if (prev_item + 1) == item:

                    prev_item = item

                else:
                    if current_slice_start == prev_item:
                        new_items.append(str(prev_item))

                    else:
                        new_items.append("{}-{}".format(current_slice_start,
                                                        prev_item))

                    prev_item = None
                    current_slice_start = None

        except ValueError:
            prev_item = None
            current_slice_start = None
            new_items.append(line_items[current_index].strip(" "))

        current_index += 1

    return new_items


def rewrite_line(line):
    header, to_rewrite = line.split("=")
    to_rewrite = to_rewrite.split(";")[0]
    to_rewrite = to_rewrite.split(", ")
    items = process_items(to_rewrite)
    new_line = "{}= {};\n".format(header, ", ".join(items))
    return new_line

def process_line(line):
    if 'charset Subset' in line:
        return rewrite_line(line)
    else:
        return line


def process_files():
    files = sys.argv[1:]
    for fi in files:
        with open("{}.rewritten".format(fi), 'w+') as output_handle:
            with open(fi) as input_handle:
                print('Started', fi)

                for line in input_handle:
                    new_line = process_line(line)
                    output_handle.write(new_line)

                print("Finished {} wrote to {}.rewritten".format(fi, fi))

def main():
    process_files()

main()
