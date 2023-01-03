import os
import warnings
import csv


def csv_to_arr(filepath: str):
    """
    Reads a csv file and returns a list of row dictionaries
    :param filepath: The CSV file to read
    :return: A list of row dictionaries
    """
    lines = []
    try:
        with open(filepath, mode='r', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, quoting=csv.QUOTE_ALL)
            for row in reader:
                lines.append(row)
        return lines
    except IOError as e:
        warnings.warn("Problem reading csv file:\n" + str(e))
        return []


def arr_to_csv(arr: list[dict], fields: list, filepath: str):
    """
    Writes an array of dictionaries to a csv file.
    :param arr: array of row dictionaries to write to file
    :param fields: a list of all field names
    :param filepath: path to a csv file to write to
    :return: None
    """
    verify_path(filepath)
    try:
        with open(filepath, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=fields,
                quoting=csv.QUOTE_ALL
            )
            writer.writeheader()
            for row in arr:
                writer.writerow(row)
    except IOError as e:
        warnings.warn("Couldn't write array to file: " + str(e))


def append_csv(item: dict, filepath: str):
    """
    Appends dictionary to csv file
    :param item: Item to append (dict)
    :param filepath: CSV file to append to (str)
    :return: None
    """
    write_headers = False
    if not os.path.exists(filepath):
        write_headers = True
    verify_path(filepath)
    with open(filepath, mode='a', newline='') as csvfile:
        fieldnames = item.keys()
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL
        )
        if write_headers:
            writer.writeheader()
        writer.writerow(item)


def verify_path(pathstr: str):
    """
    Takes a path to folder/file and makes sure the path to that a folder exists (creates one if it doesn't)
    :param pathstr: path string to file/folder
    :return: folder path string
    """
    dirpath = os.path.dirname(pathstr)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    return str(dirpath)
