
import csv
import os
from typing import Any, Iterable


def groups_save_to_file(group_data: Iterable[Iterable[Any]], file_name: str = "groups_output.csv"):
    def next_non_exists(f):
        fnew = f
        root, ext = os.path.splitext(f)
        i = 0
        while os.path.exists(fnew):
            i += 1
            fnew = '%s_%i%s' % (root, i, ext)
        return fnew

    with open(next_non_exists(file_name), 'w', encoding="utf-8-sig", newline='') as file:
        # create the csv writer
        writer = csv.writer(file)

        # write header.
        # writer.writerow("[name", "option", "members", "posts", "members_int"])

        # write data.
        writer.writerows(group_data)
