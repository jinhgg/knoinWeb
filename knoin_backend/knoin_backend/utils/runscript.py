import os


def runscript(cmd: str) -> list:
    return_list = []
    output = os.popen(cmd).readlines()
    for line in output:
        return_list.append(line)
    return return_list



'''
{%if list3_11 and not list3_11[0].not_found%}{%for i in list3_11%}{%if loop.index == list3_11|length%}{{i.species_Cname}}{%else%}{{i.species_Cname}}，{%endif%}{%endfor%}{%else%}无{%endif%}

{%if list3_11 and not list3_11[0].not_found%}{%for i in list3_11%}{%if loop.index == list3_11|length%}{{i.species_Cname}}{%else%}{{i.species_Cname}}，{%endif%}{%endfor%}{%else%}无{%endif%}    {%else%}无
{%endif%}

{%if list_2%}
{%for i in list1_5_6_7%}{{i.species_Cname}}，{%endfor%}{%else%}{{无}}{%endif%}
'''