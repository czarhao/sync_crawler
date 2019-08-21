# 初始化用户信息，获取全部的用户
from student.get_info import get_student_info
from student.grade import get_grade
from student.schedule import get_schedule


def get_all_info(student, login_session, now_url, login_soup, send_header):
    try:
        return return_json_all(True, "", get_student_info(student, login_session, now_url, login_soup, send_header),
                               get_grade(login_session, now_url, login_soup, send_header),
                               get_schedule(login_session, now_url, login_soup, send_header))
    except Exception as err:
        return return_json_all(False, str(err), None, None, None)


def return_json_all(success, info, info_map, grade_map, schedule_map):
    return_map = {
        "success": success,
        "info": info,
        "info_json": info_map,
        "grade_json": grade_map,
        "schedule_json": schedule_map
    }
    return return_map
