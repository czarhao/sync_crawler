#!/usr/bin/env python3
import json

from other import return_soup
from student.models import Grade


def get_grade(session, now_url, soup, use_header):  # 获取学生成绩
    try:
        name = soup.find(id="xhxm").text[:-2]
        url = now_url + soup.find(onclick="GetMc('成绩查询');")["href"]
        grade = session.get(url, headers=use_header)
        student_soup, text = return_soup(grade)
        view = student_soup.find('input', attrs={'name': '__VIEWSTATE'}).get('value')
        form_table = {'__EVENTTARGET': '', '__EVENTARGUMENT': '', '__VIEWSTATE': view, 'hidLanguage': '', 'ddlXN': '',
                      'ddlXQ': '', 'ddl_kcxz': '', 'btn_zcj': name}
        grade_pages = session.post(url, form_table, headers=use_header)
        grade_soup, _ = return_soup(grade_pages)
        start = False
        return_map = []
        for tmp_tr in grade_soup.find(id="Datagrid1").find_all("tr"):
            if start:
                tmp = []
                for tmp_td in tmp_tr.find_all("td"):
                    tmp_add = "".join(tmp_td.text.split())
                    if tmp_add == "":
                        tmp_add = "0"
                    tmp.append(tmp_add)
                new_grade = Grade(tmp[0], tmp[1], tmp[3], float(tmp[6]), float(tmp[7]), tmp[8],
                                  tmp[9], tmp[10], tmp[11], tmp[12])
                return_map.append(new_grade)
            else:
                start = not start
        return return_json_grade(True, "", return_map)
    except Exception as err:
        return return_json_grade(False, str(err), [])


def return_json_grade(success, info, lists):    # 返回成绩json
    maps = []
    return_json = {
        "success": success,
        "info": info,
        "grade": maps
    }
    if success:
        for i in lists:
            tmp_map = {
                "year": i.year,
                "semester": int(i.semester),
                "cname": i.cname,
                "credit": i.credit,
                "point": i.point,
                "usually": i.usually,
                "mid": i.mid,
                "final": i.final,
                "experiment": i.experiment,
                "grade": i.grade
            }
            maps.append(tmp_map)
    return return_json
