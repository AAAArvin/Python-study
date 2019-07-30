import re
import requests
from prettytable import PrettyTable

headers = {
    'Accept': '*/*',
    'Host': 'kyfw.12306.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}
target = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&' \
         'leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes={}'
station_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9107'


def get_stations(url):
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, headers=headers, verify=False)
    stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
    cn_to_en = dict(stations)
    en_to_cn = dict(zip(cn_to_en.values(), cn_to_en.keys()))
    return cn_to_en, en_to_cn


def get_tickets(train_date, from_station, to_station, type, en_to_cn):
    url = target.format(train_date, from_station, to_station, type)
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, headers=headers, verify=False)
    all_tic = response.json()['data']['result']
    for i in all_tic:
        data_list = i.split('|')
        station_train_code = data_list[3]  # 列车车次号，如G71
        from_station_telecode = data_list[4]  # 出发站代码
        to_station_telecode = data_list[5]  # 到达站代码
        start_time = data_list[8]  # 出发时间
        arrive_time = data_list[9]  # 到达时间
        range_time = data_list[10]  # 历时
        gr_num = data_list[21] or "--"  # 高级软卧
        rw_num = data_list[23] or "--"  # 软卧
        rz_num = data_list[24] or "--"  # 软座
        wz_num = data_list[26] or "--"  # 无座
        yw_num = data_list[28] or "--"  # 硬卧
        yz_num = data_list[29] or "--"  # 硬座
        ed_num = data_list[30] or "--"  # 二等座
        yd_num = data_list[31] or "--"  # 一等座
        sw_num = data_list[32] or "--"  # 商务座
        dy_num = data_list[27] or "--"  # 动卧
        data = {
            'station_train_code': station_train_code,
            'from_station_name': en_to_cn[from_station_telecode],
            'to_station_name': en_to_cn[to_station_telecode],
            'start_time': start_time,
            'arrive_time': arrive_time,
            'range_time': range_time,
            'yd_num': yd_num,
            'ed_num': ed_num,
            'sw_num': sw_num,
            'yz_num': yz_num,
            'wz_num': wz_num,
            'yw_num': yw_num,
            'rw_num': rw_num,
            'gr_num': gr_num,
            'rz_num': rz_num,
            'dy_num': dy_num,
        }
        yield data.values()


def pretty_print(results):
    pt = PrettyTable()
    pt.field_names = ('车次 出发站 到达站 出发时间 到达时间 历时 一等座 二等座 商务座 硬座 无座 硬卧 软卧 高级软卧 软座 动卧'.split())
    for result in results:
        pt.add_row(result)
    print(pt)


if __name__ == '__main__':
    cn_to_en, en_to_cn = get_stations(station_url)
    start_date = input('请输入出发日期(xxxx-xx-xx):')
    from_station = input('请输入起始站:')
    to_station = input('请输入终点站:')
    Stu_Or_Adult = input('购买学生票(是/否)')
    from_station_code = cn_to_en[from_station]
    to_station_code = cn_to_en[to_station]
    if Stu_Or_Adult == '是':
        type = '0X00'
    elif Stu_Or_Adult == '否':
        type = 'ADULT'
    else:
        raise Exception('请填写是或否')
    results = get_tickets(start_date, from_station_code, to_station_code, type, en_to_cn)
    pretty_print(results)