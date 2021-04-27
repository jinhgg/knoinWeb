from datetime import datetime, timedelta

from docx.shared import Cm
from docxtpl import InlineImage

from knoin_backend.utils.exceptions import logger


def parse_pathogen(pathogen):
    if pathogen == '-' or pathogen == '':
        return pathogen
    if ',' in pathogen:
        pathogen_list = pathogen.split(',')
    elif '，' in pathogen:
        pathogen_list = pathogen.split('，')
    else:
        pathogen_list = [pathogen]
    pathogen_str = '+'.join(pathogen_list)
    return pathogen_str


def parse_date(row):
    if not row or row == '-' or row == 'NaN-NaN-NaN':
        return '-'
    return row


def parse_test_date(row):
    """test_date是report_time前一天"""
    if not row or row == '-' or row == 'NaN-NaN-NaN':
        return '-'

    # 1.把2021-03-21 转换为 ['2021','03','21']
    split_row = row.split('-')
    if not split_row:
        return '-'

    # 2.把['2021','03','21']转换为[2021,03,21]
    date_list = [int(i) for i in split_row]

    # 3.生成日期并减一天
    test_date = (datetime(*date_list) - timedelta(1))

    return test_date.strftime('%Y-%m-%d')


def parse_age(row):
    if not row or row == '-':
        return '-'

    if '岁' in row or '月' in row or '天' in row:
        return row

    return row + '岁'


def parse_diagnosis(diagnosis):
    if not diagnosis:
        return '-'

    return diagnosis


def parse_qc_result(qc_path, qc2_path):
    qc_result = {
        'all_reads': '',
        'non_human': '',
        'non_human_fre': '',
        'q20': '',
        'q30': ''
    }
    if qc_path:
        with open(qc_path) as f:
            qc_file = f.read().split('\t')
        qc_result['all_reads'] = qc_file[3].split('\n')[1]
        qc_result['non_human'] = qc_file[4]
        qc_result['non_human_fre'] = qc_file[5]
        qc_result['q20'] = qc_file[6].split('\n')[0]

    if qc2_path:
        with open(qc2_path) as f:
            qc2_file = f.read()
        qc_result['q30'] = qc2_file.split('\t')[-1].strip('\n')

    return qc_result


def parse_img(tpl, img_path):
    if not tpl or not img_path:
        return
    return InlineImage(tpl, img_path, width=Cm(17.95))


def parse_detect_data(data_list):
    """解析data_list数据"""

    detect_data = {
        'f_results_list': [],
        'important_f_results_list': [],
        'f_results': [],
        'important_f_results': [],

        'list_1': [],  # 细菌
        'list_2': [],  # 真菌
        'list_3': [],  # DNA病毒
        'list_4': [],  # 寄生虫
        'list_5': [],  # 结核分枝杆菌
        'list_6': [],  # 非结核分枝杆菌
        'list_7': [],  # 支原体/衣原体
        'list_8': [],  # 耐药基因
        'list_9': [],  # 背景微生物
        'list_10': [],  # 关注/重点关注
        'list_11': [],  # RNA病毒

        'fh': '-',
        'explain': '无'
    }
    if data_list:
        for i in data_list:
            i_status = i.get('status')
            if i.get('status') == '背景微生物':
                detect_data['list_9'].append(i)
            elif i.get('sub_type') == '细菌':
                detect_data['list_1'].append(i)
            elif i.get('sub_type') == '真菌':
                detect_data['list_2'].append(i)
            elif i.get('sub_type') in 'DNA病毒':
                detect_data['list_3'].append(i)
            elif i.get('sub_type') in 'RNA病毒':
                detect_data['list_11'].append(i)
            elif i.get('sub_type') in '寄生虫':
                detect_data['list_4'].append(i)
            elif i.get('sub_type') in '结核分枝杆菌':
                detect_data['list_5'].append(i)
            elif i.get('sub_type') in '非结核分枝杆菌':
                detect_data['list_6'].append(i)
            elif i.get('sub_type') in '支原体/衣原体':
                detect_data['list_7'].append(i)
            elif i.get('sub_type') in '耐药基因':
                detect_data['list_8'].append(i)
            else:
                pass

            if '关注' in i_status:
                if i.get('species_Cname') == '-':
                    chinese_name = i.get('genus_Cname')
                else:
                    chinese_name = i.get('species_Cname')

                desc = i.get('des_C')
                if desc and desc != '-' and '）' in desc:
                    i['des_C'] = desc[desc.index('）') + 1:]
                else:
                    i['des_C'] = desc

                if i_status == '重点关注':
                    detect_data['important_f_results'].append(chinese_name)
                    detect_data['important_f_results_list'].append(i)
                else:
                    detect_data['f_results'].append(chinese_name)
                    detect_data['f_results_list'].append(i)

                detect_data['list_10'].append(i)

    detect_data['list1_7'] = detect_data['list_1'] + detect_data['list_7']

    # 细菌
    detect_data['list1_5_6_7'] = detect_data['list_1'] + detect_data['list_5'] + \
                                 detect_data['list_6'] + detect_data['list_7']
    # 病毒
    detect_data['list3_11'] = detect_data['list_3'] + detect_data['list_11']
    # 所有除了背景微生物list9和关注list10
    detect_data['list_all'] = detect_data['list_1'] + detect_data['list_2'] + detect_data['list_3'] + \
                              detect_data['list_4'] + detect_data['list_5'] + detect_data['list_6'] + \
                              detect_data['list_7'] + detect_data['list_8'] + detect_data['list_11']

    guide = []
    for i in detect_data['list_all']:
        guide_all = i.get('guide')
        if guide_all:
            guide.extend(i.get('guide').split('#'))
    guide = set(guide)
    if '-' in guide:
        guide.remove('-')
    detect_data['guide'] = guide

    if detect_data['f_results'] or detect_data['important_f_results']:
        detect_data['fh'] = '+'
        detect_data['explain'] = ''
        detect_data['f_results'] = '、'.join(detect_data['f_results'])
        detect_data['important_f_results'] = '、'.join(detect_data['important_f_results'])

    return detect_data
