class Const:
    # url and port
    BASE_URL = 'http://221.178.157.122'
    FRONT_PORT = ':203'
    BACKEND_PORT = ':204'
    FRONT_URL = BASE_URL + FRONT_PORT
    BACKEND_URL = BASE_URL + BACKEND_PORT
    STATIC_URL = FRONT_URL + '/statics/'


    # file path
    COLLECTION_RESULT_PATH = '/mnt/sda/platform/result_data/{collection_name}/result/'
    AUTO_GEN_JSON_RESULT_PATH = COLLECTION_RESULT_PATH + 'classify/{client_no}.classify_abundance_result.anno.auto.json'
    TEMPLATE_PATH = '/home/lijh/knoinWeb/knoin_backend/templates/{template_name}.docx'
    REPORT_NAME_1 = '病原微生物宏基因组测序检测报告-{patient_name}（{sample_type}）.docx'
    REPORT_NAME_2 = '诺微因{detect_type}_{patient_name}（{sample_type}）.docx'
    REPORT_NAME_3 = '诺微因病原微生物宏基因组测序检测报告-{detect_type}_{patient_name}（{sample_type}）.docx'
    REPORT_NAME_4 = '{hospital}-{detect_type}_{patient_name}（{sample_type}）.docx'
    REPORT_PATH = '/mnt/sda/platform/result_data/{collection_name}/result/report/{report_name}'
    REPORT_URL = FRONT_URL + '/result_data/{collection_name}/result/report/{report_name}'
    STATIC_PATH = '/home/lijh/knoinWeb/knoin_backend/statics/'

    HOSPITAL_MAP = {
        '广州市番禺区何贤纪念医院': '何贤医院',
        '广州市番禺中心医院': '番禺中心',
        '广州市番禺区第八人民医院': '番禺市八',
        '广州市番禺区中医院': '番禺中医',
        '佛山市第一人民医院': '佛山市一',
        '广东省第二人民医院': '省二',
        '广东省人民医院': '省人民',
        '广东省中医院大学城医院': '省中医大学城分院',
        '广东药科大学附属第一医院': '广药附一',
        '广州市第一人民医院': '广州市一',
        '广州医科大学附属第一医院': '广医一院',
        '广州医科大学第一附属医院': '广医一院',
        '广州医科大学附属第二医院': '广医二院',
        '广州医科大学第二附属医院': '广医二院',
        '广州医科大学附属第三医院': '广医三院',
        '广州医科大学第三附属医院': '广医三院',
        '广州医科大学附属第五医院': '广医五院',
        '广州医科大学第五附属医院': '广医五院',
        '广州中医药大学第一附属医院': '中附一',
        '广州市中医药大学第一附属医院': '中附一',
        '广州市第十二人民医': '市十二',
        '广州市荔湾中心医院': '荔湾医院',
        '暨南大学附属第一医院': '华侨医院',
        '南方医科大学珠江医院': '珠江医院',
        '南方医科大学南方医院': '南方医院',
        '南方医科大学中西医结合医院': '南方中西医',
        '中国人民解放军南部战区总医院': '南部战区',
        '中山大学附属第六医院': '中山六院',
        '中山大学附属第三医院': '中山三院',
        '中山大学附属第三医院岭南医院': '中三岭南',
        '中山大学附属第一医院': '中山一院',
        '中山大学附属第一医院东院': '中一黄埔',
        '南方医科大学第三附属医院': '南医三院',
        '汕头大学医学院第一附属医院': '汕大附一',
        '汕头大学医学院第二附属医院': '汕大附二',
        '汕头大学第一附属医院': '汕大附一',
        '汕头大学第二附属医院': '汕大附二',
        '汕头大学医学院第一附属医院龙湖医院': '龙湖医院',
        '揭阳市人民医院': '揭阳人医',
        '汕头市中心医院': '汕头中心'
    }




