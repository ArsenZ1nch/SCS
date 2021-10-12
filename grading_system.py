grade_map = {
    1050: "AAA",
    1030: "AA",
    1001: "A+",
    1000: "A",
    960: "A-",
    850: "B",
    600: "C",
    0: "D"
}

RVgrade_map = {
    "AAA": 1050,
    "AA": 1030,
    "A+": 1001,
    "A": 1000,
    "A-": 960,
    "B": 850,
    "C": 600,
    "D": 0
}

grade_list = list(RVgrade_map.keys())


def sorter(oldDict):
    newDict = {
        "AAA": [],
        "AA": [],
        "A+": [],
        "A": [],
        "A-": [],
        "B": [],
        "C": [],
        "D": []
    }
    for key in oldDict.keys():
        if oldDict[key] <= 0:
            newDict["D"].append(key)
            continue

        for score in grade_map.keys():
            if oldDict[key] >= score:
                newDict[grade_map[score]].append(key)
                break

    return newDict


def sorterRvrs(oldDict: dict):
    for key in oldDict.keys():
        if oldDict[key] <= 0:
            oldDict[key] = "D"
            continue

        for score in grade_map.keys():
            if oldDict[key] >= score:
                oldDict[key] = grade_map[score]
                break

    return oldDict


def check_grade(score):
    if score <= 0:
        return "D"

    for key in grade_map.keys():
        if score >= key:
            return grade_map[key]


def needed_sc(sc: int, grade: str):
    if grade == "AAA":
        return

    i = grade_list.index(grade)
    next_grade = grade_list[i-1]
    needed_total = RVgrade_map[next_grade]
    needed_score = needed_total - sc
    return [needed_score, next_grade]
