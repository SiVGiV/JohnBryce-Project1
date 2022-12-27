import os.path
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
            reader = csv.DictReader(csvfile)
            for row in reader:
                lines.append(row)
    except IOError as e:
        warnings.warn("Problem reading csv file:\n" + str(e))
        return []
    return lines


def arr_to_csv(arr: list[dict], fields: list, filepath: str):
    """
    Writes an array of dictionaries to a csv file.
    Skips existing IDs in the file and items with no "ID" value
    :param arr: array of row dictionaries to write to file
    :param fields: a list of all field names
    :param filepath: path to a csv file to write to
    :return: None
    """
    new_list = arr.copy()
    with open(filepath, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fields,
            quoting=csv.QUOTE_ALL
        )
        writer.writeheader()
        for row in new_list:
            writer.writerow(row)


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
