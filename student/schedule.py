#!/usr/bin/env python3
import json

from other import return_soup
from student.models import Course


def get_schedule(session, now_url, soup, use_header):  # 获取用户课程表
    try:
        url = now_url + soup.find(onclick="GetMc('学生个人课表');")["href"]
        schedule_info = session.get(url, headers=use_header)
        schedule_soup, _ = return_soup(schedule_info)
        tmp_time = 0
        tmp_info = []
        for tmp_tr in schedule_soup.find(id="Table1").find_all("tr"):
            if tmp_time > 1:
                for tmp_td in tmp_tr.find_all("td"):
                    if tmp_td.text in ["上午", "下午", "晚上"]:
                        pass
                    elif tmp_td.text == "":
                        pass
                    else:
                        tmp_info = tmp_info + get_info_td(str(tmp_td))
            tmp_time = tmp_time + 1
        return return_json_schedule(True, "", tmp_info)
    except Exception as err:
        return return_json_schedule(False, str(err), [])


def return_start_end(start_end):  # 获取上课时间，第几节，第几周
    if "|" in start_end:
        return start_end[1], start_end[start_end.find('第') + 1: start_end.find("{") - 1], \
               start_end[start_end.find("{") + 2: start_end.find("-")], start_end[start_end.find("-") + 1:-5]
    return start_end[1], start_end[start_end.find('第') + 1: start_end.find("{") - 1], \
           start_end[start_end.find("{") + 2: start_end.find("-")], start_end[start_end.find("-") + 1:-2]


def return_start_end_jud(start_end):  # 获取上课时间，第几节，第几周，单双周
    if '单周' in start_end:
        return start_end[1], start_end[start_end.find('第') + 1: start_end.find("{") - 1], \
               start_end[start_end.find("{") + 2: start_end.find("-")], start_end[start_end.find("-") + 1:-5], 1
    elif '双周' in start_end:
        return start_end[1], start_end[start_end.find('第') + 1: start_end.find("{") - 1], \
               start_end[start_end.find("{") + 2: start_end.find("-")], start_end[start_end.find("-") + 1:-5], 2
    else:
        return start_end[1], start_end[start_end.find('第') + 1: start_end.find("{") - 1], \
               start_end[start_end.find("{") + 2: start_end.find("-")], start_end[start_end.find("-") + 1:-2], 0


def get_info_td(td):  # 对td进行分词，得到学生课表
    return_list = []
    start = True
    r_list = []
    tmp_info = ""
    for value in td:
        if value == ">":
            start = not start
        elif value == "<":
            start = not start
            r_list.append(tmp_info)
            tmp_info = ""
        elif start:
            tmp_info = tmp_info + value
    if len(r_list) > 4:
        if len(r_list) > 10:
            week, sec, star, end, jud = return_start_end_jud(r_list[3])
            new_course = Course(r_list[1] + "(" + r_list[2] + ")", r_list[5], week, sec,
                                int(star), int(end), r_list[4], jud)
            return_list.append(new_course)
            week, sec, star, end, jud = return_start_end_jud(r_list[9])
            other_course = Course(r_list[7] + "(" + r_list[8] + ")", r_list[11], week, sec,
                                  int(star), int(end), r_list[10], jud)
            return_list.append(other_course)
        else:
            week, sec, star, end = return_start_end(r_list[3])
            new_course = Course(r_list[1] + "(" + r_list[2] + ")", r_list[5], week, sec,
                                int(star), int(end), r_list[4], 0)
            return_list.append(new_course)
    return return_list


def return_json_schedule(jud, err_info, info_list):  # 返回json
    maps = []
    return_json = {
        "success": jud,
        "info": err_info,
        "courses": maps
    }
    if jud:
        time = 0
        for i in info_list:
            if "(学必)" in i.cname:
                cour_type = 0
            elif "(学选)" in i.cname:
                cour_type = 1
            else:
                cour_type = 2
            tmp = i.section.find(',')
            if tmp == -1:
                cour_start = int(i.section)
                cour_length = 1
            else:
                cour_start = int(i.section[:tmp])
                cour_length = int(i.section[tmp + 1:]) - cour_start + 1
            tmp_map = {
                "id": time,
                "type": cour_type,
                "start": i.start,
                "end": i.end,
                "day_week": i.day_week,
                "cour_start": cour_start,
                "cour_length": cour_length,
                "cour_name": i.cname,
                "teacher_name": i.tname,
                "cour_where": i.where,
                "jud": i.jud
            }
            maps.append(tmp_map)
            time += 1
    return return_json
