# -*- coding: utf-8 -*-
# author Hua
# date:2018/3/17
# function：格式化run.py跑出来的数据

import datetime
from copy import deepcopy


def format_FtimeFit(FtimeFit, num_To_nodes_weapon_id_dic, newGeneration):
    """
    将1,2,3顺序序列转回离散序列号
    :param FtimeFit:
    :param num_To_nodes_weapon_id_dic:
    :param newGeneration:
    :return:
    """
    format_FtimeFit_data = deepcopy(FtimeFit)
    start_id = newGeneration['Chromossome'][0]
    format_FtimeFit_data[0] = {'NR': start_id, 'TimeEnd': 0}
    for node in format_FtimeFit_data:
        node['NR'] = num_To_nodes_weapon_id_dic[str(node['NR'])]
    return format_FtimeFit_data


def get_format_result_data(
        FtimeFit,
        num_To_nodes_weapon_id_dic,
        newGeneration,
        data_info):
    """
    加入start_time, end_time
    :param FtimeFit:
    :param num_To_nodes_weapon_id_dic:
    :param newGeneration:
    :param data_info:
    :return:
    """
    copy_node = []
    format_FtimeFit_data = format_FtimeFit(
        FtimeFit, num_To_nodes_weapon_id_dic, newGeneration)
    nt = datetime.datetime.now()
    for task in format_FtimeFit_data:
        for node in data_info["nodes"]:
            if task['NR'] == node["node_weapon_id"]:
                st = task['TimeEnd'] - int(node['score']['spend_time']*60)
                if st == 0:
                    node['start_time'] = nt.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    t1 = nt + datetime.timedelta(seconds=st)
                    node['start_time'] = t1.strftime("%Y-%m-%d %H:%M:%S")
                if node['score']['spend_time'] == 0:
                    node['end_time'] = node['start_time']
                else:
                    t2 = datetime.datetime.strptime(
                        node['start_time'],
                        "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=int(node['score']['spend_time']*60))
                    node['end_time'] = t2.strftime("%Y-%m-%d %H:%M:%S")
                copy_node.append(deepcopy(node))
    data_info["nodes"] = copy_node
    return data_info


if __name__ == '__main__':
    newGeneration = {
        'Chromossome': [
            1,
            3,
            2,
            4,
            6,
            9,
            5,
            7,
            8,
            10],
        'Cost': 26}
    FtimeFit = [
        1, {
            'NR': 3, 'TimeEnd': 1}, {
            'NR': 2, 'TimeEnd': 1}, {
                'NR': 4, 'TimeEnd': 6}, {
                    'NR': 6, 'TimeEnd': 12}, {
                        'NR': 9, 'TimeEnd': 7}, {
                            'NR': 5, 'TimeEnd': 11}, {
                                'NR': 7, 'TimeEnd': 17}, {
                                    'NR': 8, 'TimeEnd': 26}, {
                                        'NR': 10, 'TimeEnd': 26}]
    num_To_nodes_weapon_id_dic = {
        '1': '5',
        '2': '7',
        '3': '-1',
        '4': '-2',
        '5': '-3',
        '6': '9',
        '7': '20',
        '8': '17',
        '9': '0',
        '10': '13'}

    data_info = {
        "nodes": [{
            "node_weapon_id": "5",
            "score": {
                "spend_time": 0,
            }
        },
            {
            "node_weapon_id": "7",
            "score": {
                "spend_time": 1,
            }
        },
            {
            "node_weapon_id": "-1",
            "score": {
                "spend_time": 1,
            }
        },
            {
            "node_weapon_id": "-2",
            "score": {
                "spend_time": 1,
            }
        },
            {
            "node_weapon_id": "-3",
            "score": {
                "spend_time": 1,
            }
        },
            {
            "node_weapon_id": "9",
            "score": {
                "spend_time": 1,
            }
        },
            {
            "node_weapon_id": "20",
            "score": {
                "spend_time": 1,
            }
        },
            {
            "node_weapon_id": "17",
            "score": {
                "spend_time": 1,
            }
        },
            {
            "node_weapon_id": "0",
            "score": {
                "spend_time": 1,
            }
        },
            {
            "node_weapon_id": "13",
            "score": {
                "spend_time": 1,
            }
        }]
    }

    new_nodes = get_format_result_data(
        FtimeFit,
        num_To_nodes_weapon_id_dic,
        newGeneration,
        data_info)
    print 'new_nodes', new_nodes
