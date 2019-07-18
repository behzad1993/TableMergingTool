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
            file_date = file[18:26]
            with open(path + file) as csv_File:
                csv_reader = csv.reader(csv_File, delimiter=';')
                header = next(csv_reader)
                id_mapper["header"] = [header, None]
                evaluate_lines(csv_reader, id_mapper, id_double, file_date)

        print("____________________\n")
        print("Merging all csv files")
        for entry in id_mapper:
            writer.writerow(id_mapper[entry][0])
        print("Created file: " + output_name)
        print("____________________\n")

    if len(sys.argv) == 4:
        remove_single_ids(id_double)
    elif len(sys.argv) == 5 and sys.argv[4] == "yes":
        print_double_id(path, id_double, header)
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


def evaluate_lines(csv_reader, id_mapper, id_double, file_date):
    for line in csv_reader:
        if not line:
            continue
        current_id = line[5] + line[6]
        if current_id not in id_mapper:
            id_mapper[current_id] = [line, file_date]
            id_double[current_id] = [line]
        elif current_id in id_mapper:
            id_double[current_id].append(line)
            time = id_mapper.get(current_id)[0][0]
            time_to_compare = line[0]
            file_date_to_compare = id_mapper.get(current_id)[1]
            if time < time_to_compare:
                id_mapper[current_id] = [line, file_date]
            elif file_date > file_date_to_compare and time == time_to_compare:
                id_mapper[current_id] = [line, file_date_to_compare]


def remove_single_ids(id_double):
    for id_to_check in list(id_double):
        if len(id_double[id_to_check]) < 2:
            id_double.pop(id_to_check, None)
    return id_double


def print_double_id(path, id_double, header):
    print("Create file with all duplicated ID's ... please wait")
    all_duplicate_ids = "all_duplicate_ids"
    with open(path + all_duplicate_ids, 'w', encoding='utf-8', newline='') as id_check:
        writer = csv.writer(id_check, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        for id in id_double:
            if len(id_double[id]) < 2:
                continue
            writer.writerow([id])
            writer.writerow(header)
            line_list = id_double[id]
            for line in line_list:
                writer.writerow(line)
            writer.writerow("")
            writer.writerow("")
            writer.writerow("")
    id_check.close()
    print("Created additional file where all duplicate id's are listed, named: 'all_duplicate_ids'")
    print("____________________\n")


if __name__ == '__main__':
    main()
