import csv

# Output RDF file
output = open("assignment3_rdf_withprefix.ttl", "w", encoding="utf-8")

# RDF Prefix
output.write("""@prefix gu:<http://www.gu.se/ontology/> .
             @prefix rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
             """)

students = set()
programmes = set()
departments = set()
divisions = set()
teachers = set()
tas = set()
courses = set()
hoursIds = set()


# HELPER FUNCTION

def clean(text):
    return text.strip().replace(" ", "_").replace("-", "")


# 1. STUDENTS

with open("Students.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        sid = clean(row["Student id"])

        graduated = row["Graduated"].lower()

        output.write(f"""
                    gu:{sid} rdf:type gu:Student ;
                    gu:studentId {sid} ;
                    gu:studentName "{row['Student name']}" ;
                    gu:year "{row['Year']}" ;
                    gu:graduated {graduated} ;
                    gu:belongsToProgram gu:Programme_{row['Programme']} .
                    """)

# 2. SENIOR TEACHERS

with open("Senior_Teachers.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        teacher_id = clean(row["Teacher id"])
        department = row["Department name"]
        division = clean(row["Division name"])

        output.write(f"""
                     gu:{teacher_id} rdf:type gu:SeniorTeacher ;
                     gu:teacherId "{teacher_id}"^^xsd:integer ;
                     gu:teacherName "{row['Teacher name']}" ;
                     gu:belongsToDivision gu:Division_{division} .
                     """)
        
        # Department
        if department and department not in departments:
            output.write(f"""
                        gu:Department_{department} rdf:type gu:Department .
                        """)

        # Division
        if division and division not in divisions:
            output.write(f"""
                        gu:Division_{division} rdf:type gu:Division ;
                        gu:divisionName "{division}" ;
                        gu:divisionOf gu:Department_{department} .
                        """)


# 3. TEACHING ASSISTANTS

with open("Teaching_Assistants.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        teacher_id = clean(row["Teacher id"])
        department = row["Department name"]
        division = clean(row["Division name"])

        output.write(f"""
                     gu:{teacher_id} rdf:type gu:TeachingAssistant ;
                     gu:teacherName "{row['Teacher name']}" ;
                     gu:teacherId "{teacher_id}" ;
                     gu:belongsToDivision :Division_{division} .
                     """)
        
        # Department
        if department and department not in departments:
            output.write(f"""
                        gu:Department_{department} rdf:type gu:Department .
                        """)

        # Division
        if division and division not in divisions:
            output.write(f"""
                        gu:Division_{division} rdf:type gu:Division ;
                        gu:divisionName "{division}" ;
                        gu:divisionOf gu:Department_{department} .
                        """)

# 4. PROGRAMMES

with open('Programmes.csv', newline='', encoding='utf-8') as csvfile:

    reader = csv.DictReader(csvfile)

    for row in reader:

        code = clean(row.get('Programme code'))
        programme_name = row.get('Programme name')
        department = row.get('Department name')
        director = clean(row.get('Director'))

        output.write(f"""
                     gu:Programme_{code} rdf:type gu:Programme ;
                     gu:programmeName "{programme_name}" ;
                     gu:programmeCode "{code}" ;
                     gu:belongsToDepartment gu:Department_{department} .
                     gu:{director} gu:directorOfProgramme gu:Programme_{code} .
                     """)

# 5. COURSES

with open("Courses.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        course = row.get('Course name')
        course_code = row.get('Course code')
        credits = row.get('Credits')
        level = row.get('Level')
        division = clean(row.get('Division'))
        department = row.get('Department')
        programme = row.get('Owned By')

        if department and department not in departments:
            departments.add(department)
            output.write(f"""
                        gu:Department_{department} rdf:type gu:Department .
                        """)

        if division and division not in divisions:
            output.write(f"""
                        gu:Division_{division} rdf:type gu:Division ;
                        gu:divisionOf gu:Department_{department} .
                        """)

        output.write(f"""
                    gu:Courses_{course_code} rdf:type gu:Course ;
                    gu:courseCode "{course_code}" ;
                    gu:courseName "{course}" ;
                    gu:credits "{credits}" ;
                    gu:level "{level}" ;
                    gu:givenByDivision gu:Division_{division} ;
                    gu:ownedByProgramme gu:Programme_{programme} .
                    """)

# 6. COURSE INSTANCES

with open("Course_Instances.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        instance_id = clean(row.get("Instance_id"))
        course_code = row.get('Course code')
        study_period = row.get('Study period')
        academic_year = row.get('Academic year')[:4]
        examiner = clean(row.get('Examiner'))

        output.write(f"""
                     gu:Course_Instance_{instance_id} rdf:type gu:Course_instance ;
                     gu:academicYear "{academic_year}" ;
                     gu:instanceId "{instance_id}" ;
                     gu:studyPeriod "{study_period}" ;
                     gu:instanceOf gu:Courses_{course_code} .
                     gu:{examiner} gu:isExaminerOf gu:Course_Instance_{instance_id} .
                     """)

# 7. ASSIGNED HOURS

with open("Assigned_Hours.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        course = row.get('Course code')
        # study_period = row.get('Study Period')
        academic_year = row.get('Academic Year')[:4]
        teacher = clean(row.get('Teacher Id'))
        assigned_hours = row.get('Hours')
        course_instance = clean(row.get('Course Instance'))
        hoursId = f"Hours_Id_{teacher}_{course_instance}"

        output.write(f"""
                     gu:{hoursId} rdf:type gu:Hours ;
                     gu:hoursId "{hoursId}" ;
                     gu:assignedHours {assigned_hours} ;
                     gu:hoursIn gu:Course_Instance_{course_instance} .
                     gu:{teacher} gu:hasHours gu:{hoursId} .
                     """)

# 8. REPORTED HOURS

with open("Reported_Hours.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        course_instance = clean(row.get('Course code'))
        teacher = clean(row.get('Teacher Id'))
        reported_hours = row.get('Hours')
        hoursId = f"Hours_Id_{teacher}_{course_instance}"

        output.write(f"""
                     gu:{hoursId} rdf:type gu:Hours ;
                     gu:hoursId "{hoursId}" ;
                     gu:reportedHours {reported_hours} ;
                     gu:hoursIn gu:Course_Instance_{course_instance} .
                     gu:{teacher} gu:hasHours gu:{hoursId} .
                     """)

# 9. COURSE PLANNINGS

with open("Course_plannings.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    count = 1
    
    for row in reader:

        course_instance = clean(row.get('Course'))
        plannedNumber = row.get('Planned number of Students')
        senior_hours = row.get('Senior Hours')
        assistant_hours = row.get('Assistant Hours')

        output.write(f"""
                    gu:Course_Instance_{course_instance} rdf:type gu:Course_instance ;
                    gu:assistantHours {assistant_hours} ;
                    gu:seniorHours {senior_hours} ;
                    gu:plannedNumberOfStudents {plannedNumber} .
                    """)
        count += 1

# 10. PROGRAMME COURSES

with open("Programme_Courses.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    count = 1

    for row in reader:

        programme = row.get('Programme code')
        study_year = row.get('Study Year')
        academic_year = row.get('Academic Year')[:4]
        course = row.get('Course')
        course_type = row.get('Course Type')

        output.write(f"""
                     gu:Programme_Courses_{count} rdf:type gu:ProgrammeCourse ;
                     gu:programmeCourseId "Programme_Courses_{count}" ;
                     gu:programmeCode "{programme}" ;
                     gu:studyYear "{study_year}" ;
                     gu:academicYear "{academic_year}" ;
                     gu:courseType "{course_type}" ;
                     gu:courseIn gu:Programme_{programme} ;
                     gu:ofCourse gu:Courses_{course} .
                     """)
        count += 1

# 11. REGISTRATIONS

with open("Registrations.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        student_id = clean(row["Student id"])
        grade = row['Grade']
        course_instance = clean(row["Course Instance"])

        output.write(f"""
                     gu:Registrations_{count} rdf:type gu:Registration ;
                     gu:registrationId "Registrations_{count}" ;
                     gu:status "{row['Status']}" ;
                     gu:registrationFor gu:Course_Instance_{course_instance} .
                     gu:{row['Student id']} gu:registeredAt gu:Registrations_{count} .
                     """)
        if grade:
            output.write(f"""
                        gu:Registrations_{count} gu:grade "{row['Grade']}"^^xsd:integer .
                        """)
        count += 1


output.close()

print("Created RDF file: assignment3_rdf.ttl")
