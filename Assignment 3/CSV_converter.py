import csv

# Helper functions
def format_id(value):
    if value is None:
        return ""
    return value.strip().replace(" ", "").replace("-", "")

def normalize_row(row):
    return {k.strip().lower(): (v.strip() if v else "") for k, v in row.items()}

print("@prefix : <http://www.semanticweb.org/erikdagobert/ontologies/2026/3/untitled-ontology-3/> .")
print("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .")
print("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .")
print()

students = set()
programmes = set()
departments = set()
divisions = set()
teachers = set()
tas = set()
courses = set()

# Conversion for Students.csv 
with open('Students.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]

    for row in reader:
        row = normalize_row(row)
        student = format_id(row.get('studentid'))
        programme = format_id(row.get('programme'))
        if not student:
            continue
        if student not in students:
            students.add(student)
            print(f":{student} rdf:type :Student .")
            print(f':{student} :studentId "{row.get("studentid")}" .')
        if programme and programme not in programmes:
            programmes.add(programme)
            print(f":{programme} rdf:type :Programme .")
        if row.get("studentname"):
            print(f':{student} :studentName "{row.get("studentname")}" .')
        if row.get("graduated"):
            print(f':{student} :graduated "{row.get("graduated").lower()}"^^xsd:boolean .')
print()

# Conversion for Registrations.csv 
with open('Registrations.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]
    for i, row in enumerate(reader):
        row = normalize_row(row)
        student = format_id(row.get('studentid'))
        course_instance = format_id(row.get('courseinstance'))
        reg = f"Reg_{i+1}"
        if not student or not course_instance:
            continue
        if course_instance not in courses:
            courses.add(course_instance)
            print(f":{course_instance} rdf:type :Course_instance .")
            print(f':{course_instance} :instanceId "{course_instance}" .')
        print(f":{reg} rdf:type :Registration .")
        print(f':{reg} :registrationId "{reg}" .')
        print(f":{student} :registeredAt :{reg} .")
        print(f":{reg} :registrationFor :{course_instance} .")
        if row.get("status"):
            print(f':{reg} :status "{row.get("status")}" .')
        if row.get("grade"):
            print(f':{reg} :grade {row.get("grade")} .')
print()

# Conversion for Senior_Teachers.csv 
with open('Senior_Teachers.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]
    for row in reader:
        row = normalize_row(row)
        teacher = format_id(row.get('teacher id'))
        dept = format_id(row.get('dept name'))
        div = format_id(row.get('divname'))
        if not teacher:
            continue
        if teacher not in teachers:
            teachers.add(teacher)
            print(f":{teacher} rdf:type :Senior_Teacher .")
            print(f':{teacher} :teacherId "{row.get("teacher id")}" .')
        if dept and dept not in departments:
            departments.add(dept)
            print(f":{dept} rdf:type :Department .")
        if div and div not in divisions:
            divisions.add(div)
            print(f":{div} rdf:type :Division .")
        if row.get("teacher name"):
            print(f':{teacher} :teacherName "{row.get("teacher name")}" .')
        if div:
            print(f":{teacher} :belongsToDivision :{div} .")
        if dept and div:
            print(f":{div} :divisionOf :{dept} .")
print()

# Conversion for Teaching_Assistants.csv
with open('Teaching_Assistants.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]
    for row in reader:
        row = normalize_row(row)
        ta = format_id(row.get('teacher id'))
        dept = format_id(row.get('dept name'))
        div = format_id(row.get('div name'))
        if not ta:
            continue
        if ta not in tas:
            tas.add(ta)
            print(f":{ta} rdf:type :Teaching_Assistant .")
            print(f':{ta} :teacherId "{row.get("teacher id")}" .')
        if dept and dept not in departments:
            departments.add(dept)
            print(f":{dept} rdf:type :Department .")
        if div and div not in divisions:
            divisions.add(div)
            print(f":{div} rdf:type :Division .")
        if row.get("teacher name"):
            print(f':{ta} :teacherName "{row.get("teacher name")}" .')
        if div:
            print(f":{ta} :belongsToDivision :{div} .")
        if dept and div:
            print(f":{div} :divisionOf :{dept} .")
print()
