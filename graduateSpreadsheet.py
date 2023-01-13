'''
Fields:
- Have data of possible courses for each requirement

Methods:
- Get list of courses planned (course, credits, name, category, number)
- Get list of liberal studies
- Get list of major electives
- Get list of ORIE electives
- Check each requirement
    - If fulfilled: add to spreadsheet

At end: If spreadsheet filled --> can graduate


TODO:
- Make csv of major elective catA and exception
- Make csv of ORIE electives
- CourseList1 titles and data
'''

import pandas as pd

def get_liberal_studies():
    liberal_studies_courses = pd.read_csv("LiberalStudies.csv", encoding='latin-1').dropna()
    # print("Liberal Studies Courses: ")
    return liberal_studies_courses['Field + Number'].tolist()

def get_majoreleca_electives():
    major_eleca_courses = pd.read_csv("categoryA.csv", encoding='latin-1').dropna()
    # print("Got major electives A")
    return major_eleca_courses['Field + Number'].tolist()

def get_majorelecb_electives():
    major_elecb_courses = pd.read_csv("categoryB.csv", encoding='latin-1').dropna()
    # print("Got major electives B")
    return major_elecb_courses['Field + Number'].tolist()

def get_orie_electives():
    orie_elective_courses = pd.read_csv("ORIEElectives.csv", encoding='latin-1').dropna()
    # print("Got ORIE electives")
    return orie_elective_courses['Field + Number'].tolist()

def get_planned_courses():
    # print("Getting planned courses")
    planned_courses = pd.read_csv("CourseList1.csv", encoding='latin-1').dropna()
    df = {'Course': 'PHYS 1110', 'Credits': 1, 'Name': 'Introduction to Experimental Physics'}
    planned_courses.loc[len(planned_courses)] = df
    # planned_courses.concat(df, ignore_index=True)
    return planned_courses

def add_to_spreadsheet(df, index, course, used):
    if (course not in used):
        # print("Adding " + course + " to spreadsheet at " + str(index+2))
        df.at[index, "Course"] = course
        df.to_csv("GraduationChecklist.csv", index=False)

def canGraduate(planned_courses):
    liberal_studies_courses = get_liberal_studies()
    major_eleca_courses = get_majoreleca_electives()
    major_elecb_courses = get_majorelecb_electives()
    orie_elective_courses = get_orie_electives()
    used = []
    satisfied = 0

    checklist = pd.read_csv("GraduationChecklist.csv")
    for checklist_index, checklist_row in checklist.iterrows():
        requirement = checklist_row["Requirement"]
        substitutes = checklist_row["Substitutes"]
        for planned_courses_index, planned_courses_row in planned_courses.iterrows():
            course = planned_courses_row["Course"]
            if course == "CS 2110":
                course = "ENGRD 2110"
            name = planned_courses_row["Name"]
            if (requirement in course) or (course in requirement):
                add_to_spreadsheet(checklist, checklist_index, course, used)
                if course not in used:
                    used.append(course)
                    satisfied += 1
                    break
            elif "FWS" in name and "FWS" in requirement:
                add_to_spreadsheet(checklist, checklist_index, course, used)
                if course not in used:
                    used.append(course)
                    satisfied += 1
                    break
            elif requirement == "ENGRC" and "ENGRC" in course:
                add_to_spreadsheet(checklist, checklist_index, course, used)
                if course not in used:
                    used.append(course)
                    satisfied += 1
                    break
            elif requirement == "Liberal Studies" and course in liberal_studies_courses:
                add_to_spreadsheet(checklist, checklist_index, course, used)
                if course not in used:
                    used.append(course)
                    satisfied += 1
                    break
            elif requirement == "Major Approved":
                appended = False
                for major_eleca_course in major_eleca_courses:
                    if major_eleca_course in course:
                        add_to_spreadsheet(checklist, checklist_index, course, used)
                        if course not in used:
                            used.append(course)
                            satisfied += 1
                            appended = True
                if "Group" in planned_courses_row["Name"] or "Team" in planned_courses_row["Name"] and planned_courses_row["Credits"] >= 3:
                    add_to_spreadsheet(checklist, checklist_index, course, used)
                    if course not in used:
                        used.append(course)
                        satisfied += 1
                        appended = True
                if appended:
                    break
            elif requirement == "Major Approved Non ORIE":
                appended = False
                for major_elecb_course in major_elecb_courses:
                    if major_elecb_course in course:
                        add_to_spreadsheet(checklist, checklist_index, course, used)
                        if course not in used:
                            used.append(course)
                            satisfied += 1
                            appended = True
                if appended:
                    break
            elif requirement == "ORIE Elective":
                appended = False
                for orie_elective_course in orie_elective_courses:
                    if orie_elective_course in course:
                        add_to_spreadsheet(checklist, checklist_index, course, used)
                        if course not in used:
                            used.append(course)
                            satisfied += 1
                            appended = True
                if appended:
                    break
            else:
                try:
                    if course in substitutes:
                        add_to_spreadsheet(checklist, checklist_index, course, used)
                        if course not in used:
                            used.append(course)
                            satisfied += 1
                            break
                except (TypeError):
                    pass
    # print(used)

    remaining_courses = []
    for planned_courses_index, planned_courses_row in planned_courses.iterrows():
        course = planned_courses_row["Course"]
        if course == "CS 2110":
            course = "ENGRD 2110"
            print("Note: CS 2110 has been considered as ENGRD 2110\n")
        if course not in used and "AEW" not in planned_courses_row["Name"]:
            remaining_courses.append(course)
    if len(remaining_courses) >= 2:
        print("Ask your advisor to approve two courses in this list as Advisor Approved Electives: ")
        print(*remaining_courses, sep=", ")
        print()
    else:
        print("You still need " + str(2-len(remaining_courses)) + " Advisor Approved Courses")
    percent_graduated = str(satisfied/38*100)
    if (percent_graduated == "100.0"):
        print("You can graduate!")
    else:
        print("You are " + percent_graduated + "% of the way to graduating!")

# print(get_liberal_studies())
canGraduate(get_planned_courses())

'''
DEAL with ENGRD and CS2110

if num(ENGRD) == 3:
    put ENGRD2700 in ED
    put ENGRD2110 in ED
   
if num(ENGRD) == 2 and CS2110 and num(major_elec_A) = 1:
    change CS2110 into ENGRD2110
    put ENGRD2700 in ED
    put ENGRD2110 in ED
    put ENGRD3rd in major_elec_A
   
if num(ENGRD) == 2 and CS2110 and num(major_elec_A) > 1:
    pass

if num(ENGRD) = 1 and CS2110:
    change CS2110 into ENGRD2110
    put ENGRD2700 in ED
    put ENGRD2110 in ED
'''