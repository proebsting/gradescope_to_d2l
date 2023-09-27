import csv
import argparse
import pprint
import sys


def main():
    args = parse_args()
    gradescope = args.gradescope
    d2l_input = args.d2l_input
    d2l_output = args.d2l_output

    with open(gradescope, "r") as f:
        reader = csv.DictReader(f)
        gradescope_data = list(reader)

    gs_by_sid = get_by_sid(gradescope_data)

    gs_assignments = get_assignments(gradescope_data)

    with open(d2l_input, "r") as f:
        reader = csv.DictReader(f)
        d2l_data = list(reader)

    gs2d2l = {}
    d2l_row = d2l_data[0]
    for assign in gs_assignments:
        assert assign not in gs2d2l
        for d2l_key in d2l_row.keys():
            if d2l_key.startswith(assign):
                gs2d2l[assign] = d2l_key
                break
        if assign not in gs2d2l:
            print(f"Gradescope assignment {assign} not in D2L")
            sys.exit(1)

    for assign in gs_assignments:
        for row in d2l_data:
            # pprint.pprint(row)
            odid = row["OrgDefinedId"]
            assert odid[0] == "#"
            sid = odid[1:]
            if sid not in gs_by_sid:
                print(f"D2L SID {sid} not in Gradescope: {row['Username']}")
            grade = gs_by_sid[sid][assign]
            assert gs2d2l[assign] in row
            row[gs2d2l[assign]] = grade

    with open(d2l_output, "w") as f:
        writer = csv.DictWriter(f, fieldnames=d2l_row.keys())
        writer.writeheader()
        for row in d2l_data:
            writer.writerow(row)


def get_by_sid(gradescope_data):
    gs_by_sid = {}
    for row in gradescope_data:
        sid = row["SID"]
        if sid in gs_by_sid:
            x = gs_by_sid[sid]
            for k, v in x.items():
                if not v and row[k]:
                    x[k] = row[k]
            # pprint.pprint(x)
        else:
            gs_by_sid[sid] = row
    return gs_by_sid


def get_assignments(gradescope_data):
    ignore = [
        "Email",
        "First Name",
        "Last Name",
        "Lateness ",
        "- Max Points",
        "- Submission Time",
        "- Total Points",
        "Total Score",
        "SID",
    ]

    gs_assignments = []
    for key in gradescope_data[0].keys():
        if any([i in key for i in ignore]):
            continue
        gs_assignments.append(key)
    return gs_assignments


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload gradescope csv to d2l"
    )
    parser.add_argument(
        "--gradescope", type=str, required=True, help="Gradescope csv file"
    )
    parser.add_argument(
        "--d2l_input", type=str, required=True, help="D2L csv input file"
    )
    parser.add_argument(
        "--d2l_output", type=str, required=True, help="D2L csv output file"
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
