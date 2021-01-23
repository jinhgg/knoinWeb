from docxtpl import DocxTemplate

tpl = DocxTemplate('C:\\Users\\诺因\Desktop\\tpl.docx')

context = {"name": 'name', "sex": 'sex', "num": 'num', "age": 'age', "linchuang": 'linchuang', "result": 'result',
           "important": 'important', "hospital": 'hospital', "Sample_type": 'Sample_type', "Department": 'Department',
           "Sampling_date": 'Sampling_date', "physician": 'physician', "Test_date": 'Test_date',
           "report_date": 'report_date', 'important_f_results': 'important_f_results', 'f_results': 'f_results',
           'fh': 'fh',
           'list_1': 'list_1',  # Bacteria
           'list_2': 'list_2',  # Fungi
           'list_3': 'list_3',  # Viruses
           'list_4': 'list_4',  # Parasite
           'list_5': 'list_5',
           'list_6': 'list_6',
           'list_7': 'list_7',
           'list_8': 'list_8',  # rgi
           'list_9': 'list_9',
           'list_10': 'list_10',
           'all_reads': 'all_reads',
           'non_human': 'non_human',
           'non_human_fre': 'non_human_fre', 'q20': 'q20', 'img': 'img', 'explain': 'explain',
           'tpl': tpl}
context['tpl'].render(context)
tpl.save('result.docx')


# 报告生成
def rene_report(self, event):
    dlg = wx.FileDialog(self, message=u"导出",
                        defaultDir=os.getcwd(),
                        defaultFile="",
                        wildcard=file4,
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    if dlg.ShowModal() == wx.ID_OK:
        self.path6 = dlg.GetPath()
    ana_file = pd.read_excel(self.path1)
    select1 = []
    for i in range(len(ana_file)):
        if self.ana_table.GetCellValue(i, 0) == '1':
            select1.append(i)
    ana_t = ana_file.loc[select1]
    name = ana_t['患者姓名'].values[0]
    sex = ana_t['性别'].values[0]
    num = ana_t['客户编号'].values[0]
    age = ana_t['年龄'].values[0]
    linchuang = ana_t['临床诊断'].values[0] + '，' + ana_t['临床表现'].values[0]
    result = ana_t['培养鉴定结果'].values[0]
    important = ana_t['重点关注病原'].values[0]
    hospital = ana_t['医院'].values[0]
    Sample_type = ana_t['样本类型'].values[0]
    Department = ana_t['科室'].values[0]
    Sampling_date = ana_t['采样日期'].dt.date.values[0]
    physician = ana_t['医生'].values[0]
    Test_date = ana_t['收样日期'].dt.date.values[0]
    report_date = ana_t['报告日期'].dt.date.values[0]
    result_file = pd.read_table(self.path2)
    # 背景微生物
    select2 = []
    # 重点关注
    select3 = []
    # 关注
    select4 = []
    for i in range(len(result_file)):
        if self.result_table.GetCellValue(i, 0) == '0':
            select2.append(i)
        elif self.result_table.GetCellValue(i, 0) == '1':
            select3.append(i)
        elif self.result_table.GetCellValue(i, 0) == '2':
            select4.append(i)
    re_bg = result_file.loc[select2]
    re_f = result_file.loc[select3]
    re_if = result_file.loc[select4]
    re_a = result_file.loc[select4 + select3]
    if (len(select3) + len(select4)) == 0:
        fh = '-'
    else:
        fh = '+'
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []
    list_7 = []
    list_8 = []
    list_9 = []
    E_name = ['Mycobacterium', 'Chlamydia', 'Mycoplasma', 'Rickettsia', 'Neorickettsia']
    tax_id = [33894, 78331, 1806, 77643, 1773]
    '''检出细菌列表'''
    if len(re_a['level1'][re_a['level1'] == 'Bacteria']) == 0:
        list_1.append({
            'type1': '未发现',
            'Bacteria_nm': '',
            'Bacteria_nm2': '',
            'B_sequences': '',
            'B_name': '',
            'B_name2': '',
            'B_sequences2': ''
        })
    elif len(re_a['level1'][re_a['level1'] == 'Bacteria']) == (
            len(re_a['genus_Ename'][re_a['genus_Ename'] == 'Mycobacterium']) \
            + len(re_a['genus_Ename'][re_a['genus_Ename'] == 'Chlamydia']) + \
            len(re_a['genus_Ename'][re_a['genus_Ename'] == 'Mycoplasma']) + \
            len(re_a['genus_Ename'][re_a['genus_Ename'] == 'Rickettsia']) + \
            len(re_a['genus_Ename'][re_a['genus_Ename'] == 'Neorickettsia'])):
        list_1.append({
            'type1': '未发现',
            'Bacteria_nm': '',
            'Bacteria_nm2': '',
            'B_sequences': '',
            'B_name': '',
            'B_name2': '',
            'B_sequences2': ''
        })
    else:
        df_t = re_a[re_a['level1'] == 'Bacteria']
        df_t = df_t.reset_index()
        for row in range(df_t.iloc[:, 0].size):
            if df_t['genus_Ename'][row] not in E_name:
                list_1.append({
                    'type1': df_t['gram'][row],
                    'Bacteria_nm': df_t['genus_Cname'][row],
                    'Bacteria_nm2': df_t['genus_Ename'][row],
                    'B_sequences': df_t['G_Count'][row],
                    'B_name': df_t['species_Cname'][row],
                    'B_name2': df_t['species_Ename'][row],
                    'B_sequences2': df_t['S_UniqCount'][row]
                })
    '''检出真菌列表'''
    if len(re_a['level1'][re_a['level1'] == 'Fungi']) == 0:
        list_2.append({
            'Eukaryota_nm': '未发现',
            'Eukaryota_nm2': '',
            'E_sequences': '',
            'E_name': '',
            'E_name2': '',
            'E_sequences2': '',
        })
    else:
        df_t = re_a[re_a['level1'] == 'Fungi']
        df_t = df_t.reset_index()
        for row in range(df_t.iloc[:, 0].size):
            list_2.append({
                'Eukaryota_nm': df_t['genus_Cname'][row],
                'Eukaryota_nm2': df_t['genus_Ename'][row],
                'E_sequences': df_t['G_Count'][row],
                'E_name': df_t['species_Cname'][row],
                'E_name2': df_t['species_Ename'][row],
                'E_sequences2': df_t['S_Count'][row],
            })
    '''检出DNA病毒列表'''
    if len(re_a['level1'][re_a['level1'] == 'Viruses']) == 0:
        list_3.append({
            'D_name': '未发现',
            'D_name2': '',
            'D_sequences2': '',
        })
    else:
        df_t = re_a[re_a['level1'] == 'Viruses']
        df_t = df_t.reset_index()
        for row in range(df_t.iloc[:, 0].size):
            list_3.append({
                'D_name': df_t['species_Cname'][row],
                'D_name2': df_t['species_Ename'][row],
                'D_sequences2': df_t['S_Count'][row]
            })
    '''检出寄生虫列表'''
    if len(re_a['level1'][re_a['level1'] == 'Parasite']) == 0:
        list_4.append({
            'Parasite_nm': '未发现',
            'Parasite_nm2': '',
            'P_sequences': '',
            'P_name': '',
            'P_name2': '',
            'P_sequences2': '',
        })
    else:
        df_t = re_a[re_a['level1'] == 'Parasite']
        df_t = df_t.reset_index()
        for row in range(df_t.iloc[:, 0].size):
            list_4.append({
                'Parasite_nm': df_t['genus_Cname'][row],
                'Parasite_nm2': df_t['genus_Ename'][row],
                'P_sequences': df_t['G_Count'][row],
                'P_name': df_t['species_Cname'][row],
                'P_name2': df_t['species_Ename'][row],
                'P_sequences2': df_t['S_Count'][row],
            })
    '''结核分枝杆菌复合群'''
    df_mt = re_a[re_a['TaxID'] == 1765]
    for item in tax_id:
        df_mt = pd.merge(df_mt, re_a[re_a['TaxID'] == item], how='outer')
    mt1 = len(df_mt)
    if len(df_mt) == 0:
        list_5.append({
            'Species_complex_nm': '未发现',
            'Species_complex_nm2': '',
            'S_sequences': '',
            'Species_nm': '',
            'Species_nm2': '',
            'S_sequences2': '',
        })
    else:
        df_t = df_mt
        for row in range(df_t.iloc[:, 0].size):
            list_5.append({
                'Species_complex_nm': df_t['genus_Cname'][row],
                'Species_complex_nm2': df_t['genus_Ename'][row],
                'S_sequences': df_t['G_Count'][row],
                'Species_nm': df_t['species_Cname'][row],
                'Species_nm2': df_t['species_Ename'][row],
                'S_sequences2': df_t['S_Count'][row],
            })
    '''非结核分枝杆菌（NTM）'''
    if (len(re_a['genus_Ename'][re_a['genus_Ename'] == 'Mycobacterium']) - mt1) == 0:
        list_6.append({
            'NTM_nm': '未发现',
            'NTM_nm2': '',
            'N_sequences': '',
            'N_name': '',
            'N_name2': '',
            'N_sequences2': '',
        })
    else:
        df_t = re_a[re_a['genus_Ename'] == 'Mycobacterium']
        df_t = df_t.reset_index()
        for row in range(df_t.iloc[:, 0].size):
            if df_t['TaxID'][row] not in df_mt['TaxID']:
                list_6.append({
                    'Species_complex_nm': df_t['genus_Cname'][row],
                    'Species_complex_nm2': df_t['genus_Ename'][row],
                    'S_sequences': df_t['G_Count'][row],
                    'Species_nm': df_t['species_Cname'][row],
                    'Species_nm2': df_t['species_Ename'][row],
                    'S_sequences2': df_t['S_Count'][row],
                })
    '''支原体/衣原体'''
    df_mt = re_a[re_a['genus_Ename'] == 'Chlamydia']
    for item in E_name[2:]:
        df_mt = pd.merge(df_mt, re_a[re_a['genus_Ename'] == item], how='outer')
    if len(df_mt) == 0:
        list_7.append({
            'MC_nm': '未发现',
            'MC_nm2': '',
            'MC_sequences': '',
            'M_name': '',
            'M_name2': '',
            'M_sequences2': '',
        })
    else:
        df_t = df_mt
        for row in range(df_t.iloc[:, 0].size):
            list_7.append({
                'MC_nm': df_t['genus_Cname'][row],
                'MC_nm2': df_t['genus_Ename'][row],
                'MC_sequences': df_t['G_Count'][row],
                'M_name': df_t['species_Cname'][row],
                'M_name2': df_t['species_Ename'][row],
                'M_sequences2': df_t['S_Count'][row],
            })
    '''检出耐药基因列表'''
    if len(re_a['level1'][re_a['level1'] == 'rgi']) == 0:
        list_8.append({
            'rgi_nm': '未发现',
            'rgi_sequences': '',
            'rgi_family_name': '',
            'rgi_mechanism': '',
            'source_species': '',
        })
    else:
        df_t = re_a[re_a['level1'] == 'rgi']
        df_t = df_t.reset_index()
        for row in range(df_t.iloc[:, 0].size):
            list_8.append({
                # 'MC_nm': df_t['genus_Cname'][row],
                'MC_nm2': df_t['genus_Ename'][row],
                'MC_sequences': df_t['G_Count'][row],
                'M_name': df_t['species_Cname'][row],
                'M_name2': df_t['species_Ename'][row],
                'M_sequences2': df_t['S_Count'][row],
            })
    '''疑似背景微生物列表'''
    if len(re_bg['level1'][re_bg['level1'] == 'Bacteria']) != 0:
        df_t = re_bg[re_bg['level1'] == 'Bacteria']
        df_t = df_t.reset_index()
        for row in range(df_t.iloc[:, 0].size):
            list_9.append({
                'background_type': df_t['gram'][row],
                'bg_nm': df_t['genus_Cname'][row],
                'bg_nm2': df_t['genus_Ename'][row],
                'bg_sequences': df_t['G_Count'][row],
                'b_name': df_t['species_Cname'][row],
                'b_name2': df_t['species_Ename'][row],
                'b_sequences2': df_t['S_UniqCount'][row]
            })
    if len(re_bg['level1'][re_bg['level1'] == 'Eukaryota']) != 0:
        df_t = re_bg[re_bg['level1'] == 'Eukaryota']
        df_t = df_t.reset_index()
        for row in range(df_t.iloc[:, 0].size):
            list_9.append({
                'background_type': '真菌',
                'bg_nm': df_t['genus_Cname'][row],
                'bg_nm2': df_t['genus_Ename'][row],
                'bg_sequences': df_t['G_Count'][row],
                'b_name': df_t['species_Cname'][row],
                'b_name2': df_t['species_Ename'][row],
                'b_sequences2': df_t['S_UniqCount'][row]
            })
    if len(re_bg['level1'][re_bg['level1'] == 'Viruses']) != 0:
        df_t = re_bg[re_bg['level1'] == 'Viruses']
        df_t = df_t.reset_index()
        for row in range(df_t.iloc[:, 0].size):
            list_9.append({
                'background_type': '病毒',
                'bg_nm': df_t['genus_Cname'][row],
                'bg_nm2': df_t['genus_Ename'][row],
                'bg_sequences': df_t['G_Count'][row],
                'b_name': df_t['species_Cname'][row],
                'b_name2': df_t['species_Ename'][row],
                'b_sequences2': df_t['S_UniqCount'][row]
            })
    if len(re_if) == 0:
        important_f_results = '-'
    else:
        important_f_results = '，'.join(list(re_if['species_Cname']))
    if len(re_f) == 0:
        f_results = '-'
    else:
        f_results = '，'.join(list(re_f['species_Cname']))
    qc_file = pd.read_table(self.path3)
    select5 = []
    for i in range(len(qc_file)):
        if self.qc_table.GetCellValue(i, 0) == '1':
            select5.append(i)
    qc_t = qc_file.loc[select5]
    all_reads = qc_t['all_reads'][0]  # 总序列数
    non_human = qc_t['non_human'][0]  # 人类核酸过滤后序列数
    non_human_fre = qc_t['non_human_fre'][0]  # 非人类序列百分比
    q20 = qc_t['q20'][0]  # Q20
    tpl = DocxTemplate(self.path5)
    img = InlineImage(tpl, self.path4, width=Cm(17.95))
    list_10 = []
    re_a = re_a.reset_index()
    for i in range(re_a.iloc[:, 0].size):
        list_10.append({
            'm1': re_a['species_Cname'][i],
            'm2': re_a['species_Ename'][i],
            'm3': re_a['des_C'][i][(re_a['des_C'][i].index('）') + 1):]
        })
    if fh == '-':
        explain = '无'
    else:
        explain = ''
    context = {"name": name, "sex": sex, "num": num, "age": age, "linchuang": linchuang, "result": result,
               "important": important, "hospital": hospital, "Sample_type": Sample_type, "Department": Department,
               "Sampling_date": Sampling_date, "physician": physician, "Test_date": Test_date,
               "report_date": report_date, 'important_f_results': important_f_results, 'f_results': f_results,
               'fh': fh, 'list_1': list_1, 'all_reads': all_reads,
               'non_human': non_human, 'list_2': list_2,
               'list_4': list_4, 'list_5': list_5, 'list_6': list_6, 'list_7': list_7, 'list_8': list_8,
               'list_9': list_9, 'list_10': list_10,
               'non_human_fre': non_human_fre, 'q20': q20, 'img': img, 'list_3': list_3, 'explain': explain,
               'tpl': tpl}
    context['tpl'].render(context)
    print(self.path6)
    try:
        self.message.SetValue('开始生成报告')
        tpl.save(self.path6)
        self.message.SetValue('成功生成')
    except:
        self.message.SetValue('error')

