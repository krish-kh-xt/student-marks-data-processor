
import csv
import logging
from pathlib import Path

# File paths
INPUT_FILE = Path("students_excel_test.csv")
OUTPUT_FILE = Path("output.csv")
REJECTED_FILE = Path("rejected.csv")

# Configuration
SUBJECTS = ["Math", "Science", "English"]
MAX_MARKS = 100

# Logging configuration
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
def reader_file(file):
    """THIS IS EXTRACTING ROWS AND HEADER FROM CSV"""
    try:
        with open(file, newline="", encoding="utf-8") as f:
            reader=csv.DictReader(f)
            return list(reader) , reader.fieldnames
    except FileNotFoundError:
        logging.WARNING("Input file not found")
        print("errror occured")
        raise
def val_mark(value):
        if value is None or value.strip()=="":
            return None ,"missing"
        try :
             mark=float(value)
        except ValueError:
            return None , "it is not a number "
        if not 0<=mark<=MAX_MARKS : return None , "out of range"
        return (int(mark) if mark.is_integer() else mark ) , None
def student_process(row):
    marks , problems = {},[]
    for sub in SUBJECTS:
        mark , problem = val_mark(row.get(sub))
        if problem :
            problems.append( f"{sub}:{problem}" )
        else:
            marks[sub]=mark;
    total=sum(marks.values())
    clean={"name":row["name"].strip(),**marks}
    return clean , problems
def write_csv(clean_rows,heading,file):
    with open(file, "w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=heading)
        writer.writeheader()
        writer.writerows(clean_rows)
def main():
    print("start")
    student, heading=reader_file(INPUT_FILE)  #Recieves a list of dictionary(row)
    print(student)
    logging.info("Data is successfully fetch")
    clean_rows,rejected_rows=[],[]
    for line_no , row in enumerate (student,start=2): # Line 1 is header
        clean , problem = student_process(row)
        if problem:
            reason=";".join(problem)
            logging.warning("Line %d got issue in value %s", line_no, reason)
            rejected_rows.append(row)
        else:
            clean_rows.append(clean)
    print(clean_rows)                              #The clean rows and rejected rows are saved as list dictories in clean_rows , rejected_rows
    print("processing done")
    print("writing in output and rejected start!")
    write_csv(clean_rows, heading,OUTPUT_FILE)
    write_csv(rejected_rows,heading,REJECTED_FILE)
    print("writting done")
main()