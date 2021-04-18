import json
import requests
from knoin_backend.const import Const


# 测试添加collection

class MngsTest:

    def __init__(self):
        self.gen_report_url = Const.BACKEND_URL + '/mngs/gen-report/'
        self.collection_url = Const.BACKEND_URL + '/mngs/collections/'

    def gen_report(self):
        payload = {
            'dataList': '',
            'template_name': 'DNA',
            'project_id': '550',
            'mode': 'manual'
        }
        res = requests.post(self.gen_report_url, payload)
        assert res.status_code == 200, 'code[{}] /mngs/gen-report/ msg:{}'.format(res.status_code, res.text)
        print(res.text)

    def auto_gen_report(self):
        payload = {
            'template_name': 'DNA',
            'project_id': '757',
            'mode': 'auto'
        }
        res = requests.post(self.gen_report_url, payload)
        assert res.status_code == 200, 'code[{}] /mngs/gen-report/ msg:{}'.format(res.status_code, res.text)
        print(res.text)

    def list_collection_project(self):
        """查询collection"""
        res = requests.get(self.collection_url)
        assert res.status_code == 200, 'code[{}] {} msg:{}'.format(res.status_code, self.collection_url, res.text)

    def create_collection_project(self):
        """创建collection"""
        with open('./test_collection_data.json', 'r', encoding='utf-8') as f:
            json_data = json.loads(f.read())
        res = requests.post(self.collection_url, json=json_data)
        assert res.status_code == 201, 'code[{}] {} msg:{}'.format(res.status_code, self.collection_url, res.text)
        return res.json().get('id')

    def delete_collection_project(self, collection_id):
        """删除collection"""
        res = requests.delete(self.collection_url + str(collection_id))
        assert res.status_code == 204, 'code[{}] {} msg:{}'.format(res.status_code, self.collection_url, res.text)

    def modify_collection_project(self, collection_id):
        """修改collection"""
        payload = {
            'ctrl_file_path': '/path/for/test'
        }
        res = requests.patch(self.collection_url + str(collection_id) + '/', json=payload)
        assert res.status_code == 200, 'code[{}] {} msg:{}'.format(res.status_code, self.collection_url, res.text)


test = MngsTest()
#
# test.gen_report()
test.auto_gen_report()
# test.list_collection_project()
# collection_id = test.create_collection_project()
# test.modify_collection_project(collection_id)
# test.delete_collection_project(209)


def gen_report(client_no):
    if client_no.endswith('rna'):
        client_no = client_no[0:-3]
    payload = {
        'project_client_no': client_no,
        'mode': 'auto'
    }
    try:
        res = requests.post('http://221.178.157.122:204/mngs/gen-report/', payload)
    except Exception as e:
        with open('/home/lijh/knoinWeb/knoin_backend/logs/requests.log', 'w') as f:
            f.write(e)
            f.write(client_no)
    # else:
    #     with open('/home/lijh/knoinWeb/knoin_backend/logs/requests.log', 'w') as f:
    #         f.write(res.text)
    #         f.write(client_no)


#gen_report('DSH04210320002')
