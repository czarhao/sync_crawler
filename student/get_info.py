#!/usr/bin/env python3
import json
from other import return_soup


# 获取和更新学生的个人信息
def get_student_info(student, session, now_url, soup, use_header):
    try:
        info_url = now_url + soup.find(onclick="GetMc('个人信息');")["href"]
        student_info = session.get(info_url, headers=use_header)
        student_soup, text = return_soup(student_info)
        student.set_other(student_soup.find(id="xm").text, student_soup.find(id="lbl_xy").text,
                          student_soup.find(id="lbl_zymc").text, student_soup.find(id="lbl_xzb").text,
                          student_soup.find(id="lbl_xb").text, student_soup.find(id="lbl_csrq").text,
                          student_soup.find(id="lbl_rxrq").text[:4])
        return return_json_info(True, "", student.name, student.sno, student.spw, student.college, student.s_class,
                                student.prof, student.sex, student.birth, student.grade)
    except Exception as err:
        return return_json_info(False, str(err), "", "", "", "", "", "", "", "", "")


def return_json_info(success, info, name, sno, spw, college, s_class, prof, sex, birth, grade):  # 返回json数据
    r_json = {
        "success": success,
        "info": info,
        "name": name,
        "sno": sno,
        "spw": spw,
        "college": college,
        "class": s_class,
        "prof": prof,
        "sex": sex,
        "birth": birth,
        "grade": grade
    }
    return r_json
