# -*- coding: utf-8 -*-

import requests
from lxml import etree
import pandas as pd


class Boss:
    def __init__(self):
        self.start_url = 'https://www.zhipin.com/c100010000/?query=python&page={}&ka=page-{}'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        }

    def get_url_list(self):
        starturl = self.start_url
        url_list = []
        for i in range (10):
            url_list.append (starturl.format (str (i + 1), str (i + 1)))
        return url_list  # 列表url

    def parse_url(self):
        url_list = self.get_url_list ()
        resp_list = []
        for url in url_list:
            resp = requests.get (url, headers=self.headers)
            resp = resp.content.decode ()
            resp_list.append (resp)
        return resp_list

    def get_info(self):
        resp_list = self.parse_url ()
        position_list = []
        pay_list = []
        company_list = []
        add_list = []
        work_year_list = []
        study_list=[]
        for i in resp_list:
            info_temp = etree.HTML (i)
            position = info_temp.xpath ("//div[@class='job-title']/text()")
            position_list.append (position)  # 职位列表
            pay = info_temp.xpath ("//span[@class='red']/text()")
            pay_list.append (pay)  # 工资列表
            company = info_temp.xpath ("//div[@class='info-company']//a/text()")
            company_list.append (company)  # 公司列表
            add_workyear = info_temp.xpath ("//div[@class='info-primary']/p/text()")
            add = add_workyear[1::3]
            add_list.append (add)  # 年限列表
            work_year = add_workyear[2::3]
            work_year_list.append (work_year)  # 学历列表
            study=add_workyear[0::3]    # 地址列表
            study_list.append(study)
            # company_info = info_temp.xpath("//div[@class='company-text']/p/text()")
            # # company_sort = company_info[1::3]
            # #
            # # company_people=company_info[3::3]


        return (position_list, pay_list, company_list, study_list, add_list, work_year_list)

    def clear_data(self):
        position_list, pay_list, company_list, study_list, add_list, work_year_list = self.get_info ()
        data_list = []
        for i in range (10):
            position = position_list[i]
            pay = pay_list[i]
            company = company_list[i]
            add = add_list[i]
            work_year = work_year_list[i]
            study = study_list[i]
            for k in range (30):
                data_list.append(position[k])
                data_list.append(pay[k])
                data_list.append(company[k])
                data_list.append(study[k])
                data_list.append(add[k])
                data_list.append(work_year[k])


        return data_list

    def data_sum(self):
        data= self.clear_data ()
        sum_list = []
        sum_list.append(data)
        return sum_list

    def knife_data(self):
        boss_data = self.clear_data ()
        boss_data = [boss_data[i:i + 6] for i in range (0, len (boss_data), 6)]
        return boss_data

    def create_csv(self):
        list = self.knife_data ()
        name = ['职位', '薪资', '公司名称', '公司地址', '工作年限', '学历']
        test = pd.DataFrame (columns=name, data=list)
        test.to_csv ('Boss_info.csv', encoding='gbk')


if __name__ == "__main__":
    a = Boss ()
    a.create_csv()