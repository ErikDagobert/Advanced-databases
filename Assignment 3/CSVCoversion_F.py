import csv


# OUTPUT RDF/TURTLE FILE


output = open("assignment3_final.ttl", "w", encoding="utf-8")


# PREFIXES

output.write("""
@prefix : <http://www.semanticweb.org/erikdagobert/ontologies/2026/3/untitled-ontology-3#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

""")


# HELPER FUNCTION

def clean(text):
    return text.strip().replace(" ", "_").replace("-", "_")



# 1. STUDENTS

with open("Students.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        student_id = row["Student id"]

        graduated = row["Graduated"].strip().lower()

        output.write(f"""
:Student_{student_id} rdf:type :Student ;
    :studentId "{student_id}"^^xsd:integer ;
    :studentName "{row['Student name']}" ;
    :graduated "{graduated}"^^xsd:boolean .
""")


# 2. SENIOR TEACHERS


with open("Senior_Teachers.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        teacher_id = row["Teacher id"]

        department = clean(row["Department name"])
        division = clean(row["Division name"])

        output.write(f"""
:SeniorTeacher_{teacher_id} rdf:type :Senior_Teacher ;
    :teacherId "{teacher_id}"^^xsd:integer ;
    :teacherName "{row['Teacher name']}" ;
    :belongsToDivision :Division_{division} .
""")

        # Department individual

        output.write(f"""
:Department_{department} rdf:type :Department .
""")

        # Division individual

        output.write(f"""
:Division_{division} rdf:type :Division ;
    :divisionName "{row['Division name']}" ;
    :divisionOf :Department_{department} .
""")



# 3. TEACHING ASSISTANTS

with open("Teaching_Assistants.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        teacher_id = row["Teacher id"]

        department = clean(row["Department name"])
        division = clean(row["Division name"])

        output.write(f"""
:TeachingAssistant_{teacher_id} rdf:type :Teaching_Assistant ;
    :teacherId "{teacher_id}"^^xsd:integer ;
    :teacherName "{row['Teacher name']}" ;
    :belongsToDivision :Division_{division} .
""")



# 4. PROGRAMMES


with open("Programmes.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        programme_code = clean(row["Programme code"])

        department = clean(row["Department name"])

        output.write(f"""
:Programme_{programme_code} rdf:type :Programme ;
    :programmeCode "{row['Programme code']}" ;
    :programmeName "{row['Programme name']}" ;
    :belongsToDepartmet :Department_{department} .
""")

        # Director relation (Senior Teacher -> Programme)

        director_name = clean(row["Director"])

        output.write(f"""
:SeniorTeacher_{director_name} :directorOfProgramme :Programme_{programme_code} .
""")



# 5. COURSES


with open("Courses.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        course_code = clean(row["Course code"])

        division = clean(row["Division"])

        owned_by = clean(row["Owned By"])

        level = row["Level"].strip().lower()

        output.write(f"""
:Course_{course_code} rdf:type :Course ;
    :courseCode "{row['Course code']}" ;
    :courseName "{row['Course name']}" ;
    :credits "{row['Credits']}"^^xsd:double ;
    :level "{level}" ;
    :givenByDivision :Division_{division} ;
    :ownedByProgramme :Programme_{owned_by} .
""")



# 6. COURSE INSTANCES


with open("Course_Instances.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        instance_id = clean(row["Instance_id"])

        course_code = clean(row["Course code"])

        output.write(f"""
:CourseInstance_{instance_id} rdf:type :Course_instance ;
    :instanceId "{row['Instance_id']}"^^xsd:string ;
    :studyPeriod "{row['Study period']}"^^xsd:integer ;
    :academicYear "{row['Academic year']}"^^xsd:string ;
    :instanceOf :Course_{course_code} .
""")



# 7. ASSIGNED HOURS

with open("Assigned_Hours.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    count = 1

    for row in reader:

        teacher_id = row["Teacher Id"]

        course_instance = clean(row["Course Instance"])

        output.write(f"""
:Hours_Assigned_{count} rdf:type :Hours ;
    :hoursId "AH{count}" ;
    :assignedHours "{row['Hours']}"^^xsd:double ;
    :hoursIn :CourseInstance_{course_instance} .
""")

        # Teacher -> Hours relation

        output.write(f"""
:SeniorTeacher_{teacher_id} :hasHours :Hours_Assigned_{count} .
""")

        count += 1


# 8. REPORTED HOURS

with open("Reported_Hours.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    count = 1

    for row in reader:

        teacher_id = row["Teacher Id"]

        course_instance = clean(row["Course code"])

        output.write(f"""
:Hours_Reported_{count} rdf:type :Hours ;
    :hoursId "RH{count}" ;
    :reportedHours "{row['Hours']}"^^xsd:double ;
    :hoursIn :CourseInstance_{course_instance} .
""")

        output.write(f"""
:SeniorTeacher_{teacher_id} :hasHours :Hours_Reported_{count} .
""")

        count += 1



# 9. COURSE PLANNINGS



with open("Course_plannings.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    count = 1

    for row in reader:

        course_instance = clean(row["Course"])

        output.write(f"""
:CoursePlanning_{count} rdf:type :Course_planning ;
    :plannedNumberOfStudents "{row['Planned number of Students']}"^^xsd:int ;
    :seniorHours "{row['Senior Hours']}"^^xsd:double ;
    :assistantHours "{row['Assistant Hours']}"^^xsd:double ;
    :planningFor :CourseInstance_{course_instance} .
""")

        count += 1




# 10. PROGRAMME COURSES


with open("Programme_Courses.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    count = 1

    for row in reader:

        programme_code = clean(row["Programme code"])

        course_instance = clean(row["Course"])

        course_type = row["Course Type"].strip().lower()

        output.write(f"""
:ProgrammeCourse_{count} rdf:type :Programme_course ;
    :programmeCourseId "PC{count}" ;
    :studyYear "{row['Study Year']}"^^xsd:integer ;
    :courseType "{course_type}" ;
    :courseIn :Programme_{programme_code} ;
    :programmeCourseOfInstance :CourseInstance_{course_instance} .
""")

        count += 1




# 11. REGISTRATIONS

with open("Registrations.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    count = 1

    for row in reader:

        student_id = row["Student id"]

        course_instance = clean(row["Course Instance"])

        output.write(f"""
:Registration_{count} rdf:type :Registration ;
    :registrationId "R{count}" ;
    :status "{row['Status'].strip().lower()}" ;
    :grade "{row['Grade']}"^^xsd:integer ;
    :registrationFor :CourseInstance_{course_instance} .
""")

        # Student -> Registration relation

        output.write(f"""
:Student_{student_id} :registeredAt :Registration_{count} .
""")

        count += 1



output.close()

print("assignment3_final.ttl")
