# import numpy as np
import csv

print("@prefix : <http://www.semanticweb.org/kemp/ontologies/2019/3/untitled-ontology-1#> .")
print("@prefix owl: <http://www.w3.org/2002/07/owl#> .")
print("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .")
print("@prefix xml: <http://www.w3.org/XML/1998/namespace> .")
print("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .")
print("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .")
print("@base <http://www.semanticweb.org/kemp/ontologies/2019/3/untitled-ontology-1> .")

with open('Courses.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    deps = []
    divs = []
    for row in reader:
        # Object class declaration:
        print(row['Course name'] + " rdf:type Course .")
        if not (row['Division'] in divs):
            if row['Department'] in deps:
                divs.append(row['Division'])
                print(row['Division'] + " rdf:type Division .")
            else:
                deps.append(row['Department'])
                divs.append(row['Division'])
                print(row['Division'] + " rdf:type Division .")
                print(row['Department'] + " rdf:type Department .")

        # Data properties:
        print(row['Course name'] + " :courseCode " + row['Course code'] + " .")
        print(row['Course name'] + " :courseName " + row['Course name'] + " .")
        print(row['Course name'] + " :credits " + row['Credits'] + " .")
        print(row['Course name'] + " :level " + row['Level'] + " .")  # Caps!

        # Object properties:
        


with open('Programmes.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)


            



