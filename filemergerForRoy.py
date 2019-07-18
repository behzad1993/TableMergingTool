import os
import csv
import sys


def main():
    check_params()
    arguments = sys.argv
    path = arguments[1] + '/'
    output_name = arguments[2]

    print("Choosen path: " + path)
    print("Choosen filename: " + output_name)

    files = check_path(path)

    if os.path.exists(path + output_name):
        print("Remove existing merge file named: " + output_name + "\n")
        os.remove(path + output_name)
        files.remove(path + output_name)

    all_duplicate_ids = "all_duplicate_ids"
    if os.path.exists(path + all_duplicate_ids):
        print("Remove existing file named: " + all_duplicate_ids + "\n")
        os.remove(path + all_duplicate_ids)
        files.remove(path + all_duplicate_ids)

    print("____________________\n")
    print("Start searching for duplicate ID's ... \n")
    evaluate_files(path, output_name, files)


def check_params():
    if len(sys.argv) < 3:
        sys.exit("No path AND output filename found. Please retry")


def check_path(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))

    print("____________________\n")
    print("Files found: \n")
    for file in files:
        print(file)
    print("____________________\n")
    return files


def evaluate_files(path, output_name, files):
    id_mapper = {}
    id_double = {}
    with open(path + output_name, 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        files = remove_unnecessary_files(files, path, output_name)
        for file in files:
            print("Reading file: " + file + " ...")
            with open(path + file, encoding='utf-8-sig') as csv_File:
                csv_reader = csv.reader(csv_File, delimiter=';')
                evaluate_lines(csv_reader, id_mapper, id_double, file)

        print("____________________\n")
        print("Merging all csv files")
        for entry in id_mapper:
            writer.writerow(id_mapper[entry][0])
        print("Created file: " + output_name)
        print("____________________\n")

    if len(sys.argv) == 5 and sys.argv[4] == "yes":
        print_double_id(path, id_double)
    print("Found " + (str)(len(id_double)) + " ID duplicates")
    csv_File.close()
    out.close()
    print("Executed successfully.")


def remove_unnecessary_files(files, path, output_name):
    print("Check for unnecessary files...")
    checked_file_list = []
    for file in files:
        file = file.replace(path, "")
        if not file.startswith('.') and file != output_name:
            checked_file_list.append(file)
    print("____________________\n")
    return checked_file_list


def evaluate_lines(csv_reader, id_mapper, id_double, file):
    for line in csv_reader:
        if not line:
            continue
        current_id = line[0]
        if current_id not in id_mapper:
            id_mapper[current_id] = [line]
            id_double[current_id] = [line]
        elif current_id in id_mapper:
            id_double[current_id].append(line)


def remove_single_ids(id_double):
    for id_to_check in list(id_double):
        if len(id_double[id_to_check]) < 2:
            id_double.pop(id_to_check, None)
    return id_double


def print_double_id(path, id_double):
    remove_single_ids(id_double)
    print("Create file with all duplicated ID's ... please wait")
    all_duplicate_ids = "all_duplicate_ids"
    with open(path + all_duplicate_ids, 'w', encoding='utf-8', newline='') as id_check:
        writer = csv.writer(id_check, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        for id in id_double:
            writer.writerow([id])
    id_check.close()
    print("Created additional file where all duplicate id's are listed, named: 'all_duplicate_ids'")
    print("____________________\n")


if __name__ == '__main__':
    main()
