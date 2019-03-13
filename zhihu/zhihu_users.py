import requests
from lxml import etree
import json
import time
import pandas as pd


class WeiBo:
    def __init__(self):
        self.start_url = 'https://www.zhihu.com/api/v4/members/ponyma/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}&limit=20'


        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Cookie": 'ALF=1554689630; SCF=Agk73soAs_wI_KMj1xD_Tjp6skFq_xra-SOjeMvemIEw5nprJukENV8JKmm7IWNHy88JFvCVXWQGohJnc-kLv1s.; SUB=_2A25xh9VvDeRhGeVI61AV9CbFwzyIHXVSi_snrDV6PUJbktANLXmskW1NTA50IkjM-hVv0pppp_5xpMQm4sInE8CC; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFDPAQMPiQJajRR6WpWahnI5JpX5K-hUgL.FoecehzXShn41h52dJLoI0YLxK-LBK-LBK-LxKqL1KqLB-qLxKnL122LB-BLxKnL1K-LB.-LxKBLB.2L1-2LxKnLBK5L1-zLxKnL1-BLBoqt; SUHB=0JvwtYUvUbA7gp; SSOLoginState=1552131391; MLOGIN=1; _T_WM=f0514621764cd032150e5fceda3227b3; WEIBOCN_FROM=1110003030; XSRF-TOKEN=9a73a9; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1005052866934782%26fid%3D231051_-_fans_intimacy_-_2866934782%26uicode%3D10000011'
        }
        self.proxies = {'http':'https://222.191.243.187:42649'}

    def get_start_json(self):
        print('正在解析url.....')
        url = self.start_url
        resp = requests.get (url, headers=self.headers,proxies =self.proxies)
        resp = resp.content.decode ()
        jsons = json.loads (resp)

        return jsons

    def get_page(self):
        json = self.get_start_json ()

        total = json['paging']['totals']
        if total % 20 == 0:
            page = total // 20
        else:
            page = (total // 20) + 1

        return page

    def get_url_list(self):

        page = self.get_page ()
        url_list = []
        for i in range (page + 1):
            url = self.start_url.format (i * 20)
            url_list.append (url)
            print ('正在创建url列表{}.....'.format(i))



        return url_list

    def get_json_list(self):
        url_list = self.get_url_list ()
        json_list = []

        for url in url_list:
            resp = requests.get (url, headers=self.headers)
            time.sleep(1)
            resp = resp.content.decode ()
            json_str = json.loads (resp)
            json_list.append (json_str)
            print ('正在创建json列表位置{}.....'.format(url_list.index(url)))
            self.get_user_info(json_list)



    def get_user_info(self,json_list):

        # print (json_list)
        user_info =[]

        try:
            for json in json_list:
                print('正在解析第{}个json'.format(json_list.index(json)))
                for i in range (20):
                    info = json['data'][i]
                    name = info['name']
                    headline = str(info['headline'])
                    user_url = str(info['url'])
                    url_token = str(info['url_token'])
                    fans = str(info['follower_count'])
                    head_pic = str(info['avatar_url'])
                    gender = str(info['gender'])
                    is_vip = str(info['vip_info']['is_vip'])
                    answer = str(info['answer_count'])
                    user_info.append(name) # 姓名
                    user_info.append(headline) # 标题
                    user_info.append(gender) # 性别：男-1 女 0
                    user_info.append(is_vip) # 是否为会员
                    user_info.append(fans) # 粉丝数
                    user_info.append(answer) # 他参与的回答数
                    zhihu_data = [user_info[i:i + 6] for i in range (0, len (user_info), 6)]
                    list = zhihu_data
                    names = ['知乎名称', '个人介绍', '性别', '是否为知乎会员', '粉丝数', '知乎回答数']
                    test = pd.DataFrame (columns=names, data=list)
                    test.to_csv ('zhihu_2222.csv', encoding='utf-8')
                    print('已保存用户{}'.format(name))

        except Exception as e :
            return










if __name__ == '__main__':
    a = WeiBo ()
    a.get_json_list()











