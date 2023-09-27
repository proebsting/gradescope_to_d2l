## gradescope_to_d2l

To import grades from Gradescope to D2L using this script, the names of the corresponding
assignments must "match".  A Gradescope name matches a D2L name if the Gradescope name is
a prefix of the D2L name.

There are four steps:

1. Download CSV of all assignment grades from Gradescope (Assignments>Download Grades)
2. "Export" CSV of all grades from D2L.  (Grades>Enter Grades>Export>Export to CSV, selecting all assignments)
3. Run the program, creating a new D2L CSV file.
4. "Import" CSV of updated grades to D2L.  (Grades>Enter Grades>Import)

## Usage

```
$ python3 main.py --help
usage: main.py [-h] --gradescope GRADESCOPE --d2l_input D2L_INPUT --d2l_output D2L_OUTPUT

Upload gradescope csv to d2l

options:
  -h, --help            show this help message and exit
  --gradescope GRADESCOPE
                        Gradescope csv file
  --d2l_input D2L_INPUT
                        D2L csv input file
  --d2l_output D2L_OUTPUT
                        D2L csv output file

```
