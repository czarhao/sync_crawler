class Grade:
    def __init__(self, year, semester, cname, credit, point, usually, mid, final, experiment, grade):
        self.year = year
        self.semester = semester
        self.cname = cname
        self.credit = credit
        self.point = point
        self.usually = usually
        self.mid = mid
        self.final = final
        self.experiment = experiment
        self.grade = grade


class Student:  # 建立学生对象
    def __init__(self, sno, spw):
        self.sno = sno
        self.spw = spw
        self.name = ""
        self.college = ""
        self.s_class = ""
        self.prof = ""
        self.sex = 1
        self.birth = ""
        self.grade = ""

    def set_other(self, name, college, prof, s_class, sex, birth, grade):
        self.name = name
        self.college = college
        self.s_class = s_class
        self.prof = prof
        self.sex = sex
        self.birth = birth
        self.grade = grade


class Course:  # 建立课程对象
    def __init__(self, cname, where, day_week, section, start, end, tname, jud):
        self.cname = cname
        self.where = where
        self.day_week = day_week_map[day_week]
        self.section = section
        self.start = start
        self.end = end
        self.tname = tname
        self.jud = jud


day_week_map = {
    "一": 0,
    "二": 1,
    "三": 2,
    "四": 3,
    "五": 4,
    "六": 5,
    "日": 6
}
