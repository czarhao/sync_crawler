#!/usr/bin/env python3
from student.all import get_all_info, return_json_all
from student.get_info import get_student_info, return_json_info
from student.grade import get_grade, return_json_grade
from student.schedule import get_schedule, return_json_schedule


# 这些是路由函数
def route(do, student, login_session, now_url, login_soup, send_header, jud, err_info):
    # 当执行的操作为获取当前用户信息时
    if do == "info":
        if jud:
            return get_student_info(student, login_session, now_url, login_soup, send_header)
        else:
            return return_json_info(jud, err_info, "", "", "", "", "", "", "", "", "")
    elif do == "all":
        if jud:
            return get_all_info(student, login_session, now_url, login_soup, send_header)
        else:
            return return_json_all(jud, err_info, None, None, None)
    else:
        if do == "schedule":
            if jud:
                return get_schedule(login_session, now_url, login_soup, send_header)
            else:
                return return_json_schedule(False, "", [])
        elif do == "grade":
            if jud:
                return get_grade(login_session, now_url, login_soup, send_header)
            else:
                return return_json_grade(False, "", [])
