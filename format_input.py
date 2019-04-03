# -*- coding: utf-8 -*-
from copy import deepcopy
import json



class data_to_new_data(object):
    # 给data数据加上虚点和虚边
    # docstring for data_to_new_data

    def __init__(self, data_info):
        super(data_to_new_data, self).__init__()
        self.data_info = data_info

    # 得到起始结点和终结点列表
    def __get_start_and_end_nodes(self):
        start_nodes = []  # 起始结点
        end_nodes = []  # 终点
        source_nodes = []
        target_nodes = []
        for edge in self.data_info["edges"]:
            source_nodes.append(edge["source_id"])
            target_nodes.append(edge["target_id"])
        for node in self.data_info["nodes"]:
            if node["node_weapon_id"] not in source_nodes:
                end_nodes.append([node["node_weapon_id"],
                                  node["node_name"] + "+" + node["weapon_name"]])
            if node["node_weapon_id"] not in target_nodes:
                start_nodes.append(
                    [node["node_weapon_id"], node["node_name"] + "+" + node["weapon_name"]])
        return start_nodes, end_nodes

    # 创建新的虚起点和虚终点
    def __create_fake_nodes(self):
        fake_start_node = {
            "weapon_id": "-2",
            "node_score": 0,
            "node_id": "-2",
            "resource": {"R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0},
            "weapon_name": "virtual_start",
            "power": {},
            "score": {
                "cost": 0,
                "spend_time": 0,
                "success_rate": 0,
                "invisibility": 0
            },
            "node_weapon_id": "-2",
            "node_name": ""
        }
        fake_end_node = {
            "weapon_id": "-3",
            "node_score": 0,
            "node_id": "-3",
            "resource": {"R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0},
            "weapon_name": "virtual_end",
            "power": {},
            "score": {
                "cost": 0,
                "spend_time": 0,
                "success_rate": 0,
                "invisibility": 0
            },
            "node_weapon_id": "-3",
            "node_name": ""
        }
        return fake_start_node, fake_end_node

    # 创建虚的起始边和虚的终边
    def __creat_fake_edges(self):
        start_nodes, end_nodes = self.__get_start_and_end_nodes()
        new_fake_edges = []
        for node_target_id in start_nodes:
            temp = {
                "source_id": "-2",
                "source_name": "virtual_start",  # 虚起点
                "target_name": node_target_id[1],
                "target_id": node_target_id[0],
                "and": ""
            }
            new_fake_edges.append(temp)
        for node_source_id in end_nodes:
            temp = {
                "source_id": node_source_id[0],
                "source_name": node_source_id[1],
                "target_name": "virtual_end",  # 虚终点
                "target_id": "-3",
                "and": ""
            }
            new_fake_edges.append(temp)
        return new_fake_edges

    # 创建新的data数据集
    def get_new_data_info(self):
        new_data_info = deepcopy(self.data_info)
        fake_start_node, fake_end_node = self.__create_fake_nodes()
        new_fake_edges = self.__creat_fake_edges()

        new_data_info["nodes"].append(fake_start_node)
        new_data_info["nodes"].append(fake_end_node)
        new_data_info["edges"].extend(new_fake_edges)

        # 把新生成的数据写入进json文件中去
        json_str = json.dumps(new_data_info, indent=4)
        with open('new_data.json', 'w') as json_file:
            json_file.write(json_str)

        return new_data_info


# 把data数据修改为输入“galgorithm_rcpsp.py”的输入数据
class new_data_to_in_file(object):

    """docstring for new_data_to_in_file"""

    def __init__(self):
        super(new_data_to_in_file, self).__init__()

    # 排序
    def __get_sort(self, elem):
        return int(elem[0])

    # 列表拼接成文本
    def __get_txt(self, info_list):
        sub_content_txt = []
        for sub_info in info_list:
            sub_content_txt.append("        ".join(sub_info))
        content_txt = "\n".join(sub_content_txt)
        return content_txt

    # 获取REQUESTS/DURATIONS, RESOURCEAVAILABILITIES
    def __get_requests_duration(self, nodes):
        info_list = []
        resource_dic = {}
        for node in nodes:
            for key, value in node["resource"].items():
                resource_dic[key] = str(value)
            temp_list = [
                node["node_weapon_id"], '1', str(
                    node["score"]["spend_time"]*60).split(".")[0]]
            resource_dic_list = sorted(
                resource_dic.iteritems(),
                key=lambda k: k[0][1])
            temp_list.extend(x[1] for x in resource_dic_list)
            info_list.append(temp_list)
        info_list.sort(key=self.__get_sort)
        return info_list

    # 把“REQUESTS/DURATIONS”列表信息返回成文本信息

    def __get_txt_requests_duration(self, nodes):
        info_list = self.__get_requests_duration(nodes)
        content_txt = self.__get_txt(info_list)
        return content_txt, len(info_list)

    # 得到PRECEDENCE RELATIONS列表信息
    def __get_precedence_relations(self, edges):
        edge_dic = {}
        for edge in edges:
            if edge["source_id"] not in edge_dic.keys():
                edge_dic[edge["source_id"]] = [edge["target_id"]]
            else:
                edge_dic[edge["source_id"]].append(edge["target_id"])
        info_list = []
        for edge in edges:
            if edge["target_id"] not in edge_dic.keys():
                info_list.append([edge["target_id"], '1', '0'])
                # info_list.append(finally_node)
        for key, value in edge_dic.items():
            sub_info_list = [key, '1', str(len(value))]
            sub_info_list.extend(value)
            info_list.append(sub_info_list)
        info_list.sort(key=self.__get_sort)
        return info_list

    # 得到PRECEDENCE RELATIONS文本信息
    def __get_txt_precedence_relations(self, edges):
        info_list = self.__get_precedence_relations(edges)
        content_txt = self.__get_txt(info_list)
        return content_txt

    def main(self, data_info, address, resourceavailabilites):
        content_txt_1 = self.__get_txt_precedence_relations(data_info["edges"])
        content_txt_2, num_task = self.__get_txt_requests_duration(
            data_info["nodes"])
        content_txt_3 = ""
        for i in resourceavailabilites:
            content_txt_3 += str(i) + "     "
        with open("base_input.sm", "r") as f:
            data = f.readlines()
        data[5] = "jobs (incl. supersource/sink ):  " + str(num_task) + "\n"
        data[14] = "    1     " + \
            str(num_task - 2) + "      0       0       0       0\n"
        text1 = "*" * 60 + "\nPRECEDENCE RELATIONS:\n" + \
            "jobnr. #modes #successors successors\n" + content_txt_1
        text2 = "\n" + "*" * 60 + "\nREQUESTS/DURATIONS:\n" + \
            "jobnr.  mode  duration    R1    R2    R3    ...   Rn\n" + "-" * 60 + "\n" + content_txt_2
        text3 = "\n" + "*" * 60 + "\nRESOURCEAVAILABILITIES\n" + \
            "R1     R2     R3    ...   Rn\n" + content_txt_3
        text = text1 + text2 + text3
        data[15] = text

        f = open(address, "w")
        f.writelines(data)
        f.close()
        return num_task


def sort_num(elem):
    return int(elem)


# 修改添加虚结点的数据，使他们的node_weapon_id值按照1,2,3...进行排列，并用字典形式保存原始node_weapon_id
def continue_node_weapon_id(new_data_info):
    all_nodes_weapon_id = []
    for node in new_data_info["nodes"]:
        all_nodes_weapon_id.append(node["node_weapon_id"])
    all_nodes_weapon_id.sort(key=sort_num)
    # 把-3虚终点放在列表最后一个
    temp_num = all_nodes_weapon_id[0]
    all_nodes_weapon_id[:-1] = all_nodes_weapon_id[1:]
    all_nodes_weapon_id[-1] = temp_num
    # print all_nodes_weapon_id
    # 使node_weapon_id和num键值对应
    nodes_weapon_id_To_num = {}
    for num in range(len(all_nodes_weapon_id)):
        nodes_weapon_id_To_num[all_nodes_weapon_id[num]] = str(num + 1)
    num_To_nodes_weapon_id = {v: k for k, v in nodes_weapon_id_To_num.items()}
    # print nodes_weapon_id_To_num
    # 得到新的点和边数据，他们的node_weapon_id是连续的
    contine_num_data = deepcopy(new_data_info)
    for i in range(len(contine_num_data["nodes"])):
        node_weapon_id = contine_num_data["nodes"][i]["node_weapon_id"]
        contine_num_data["nodes"][i]["node_weapon_id"] = nodes_weapon_id_To_num[node_weapon_id]
    for i in range(len(contine_num_data["edges"])):
        source_id = contine_num_data["edges"][i]["source_id"]
        target_id = contine_num_data["edges"][i]["target_id"]
        contine_num_data["edges"][i]["source_id"] = nodes_weapon_id_To_num[source_id]
        contine_num_data["edges"][i]["target_id"] = nodes_weapon_id_To_num[target_id]

    return num_To_nodes_weapon_id, contine_num_data


# 预留接口
def get_resourceavailabilites(generic_view_nodes):
    # todo 获取资源限制
    return [20, 20, 20, 20, 20]


def get_format_input_data(generic_view_nodes, generic_view_edges, address):
    data_info = {}
    data_info["nodes"] = generic_view_nodes  # 点
    data_info["edges"] = generic_view_edges  # 边
    # 把原始数据添加虚结点生成新的数据，运行第一个类·················1
    class_new_data = data_to_new_data(data_info)
    new_data_info = class_new_data.get_new_data_info()
    # 修改添加虚结点的数据，使他们的node_weapon_id值按照1,2,3...进行排列，并用字典形式保存原始node_weapon_id···········2
    num_To_nodes_weapon_id_dic, contine_num_data = continue_node_weapon_id(
        new_data_info)
    # 得到resourceavailabilites列表值
    resourceavailabilites = get_resourceavailabilites(generic_view_nodes)

    # 得到输入文件，运行的是········2生成的数据
    get = new_data_to_in_file()
    numTasks = get.main(contine_num_data, address, resourceavailabilites)
    return numTasks, num_To_nodes_weapon_id_dic

    '''
    #得到输入文件，运行第二个类，运行的是·······1生成的数据
    get = new_data_to_in_file()
    numTasks = get.main(new_data_info, address, resourceavailabilites)
    return numTasks
    '''


if __name__ == '__main__':
    # 调用方法，直接调用main,传入点信息，边信息，sm文件保存信息，resourceavailabilites信息
    data_info = {"nodes": [{"weapon_id": "5",
                            "node_score": 9.0,
                            "node_id": "5",
                            "resource": {"R1": 5,
                                         "R2": 4,
                                         "R3": 3,
                                         "R4": 2,
                                         "R5": 1,
                                         "R6": 0},
                            "weapon_name": "GetVPNInfo",
                            "power": {},
                            "score": {"cost": 2.0,
                                      "spend_time": 1,
                                      "success_rate": 1.4,
                                      "invisibility": 1.2},
                            "node_weapon_id": "5",
                            "node_name": "Device02"},
                           {"weapon_id": "12",
                            "node_score": 9.0,
                            "node_id": "12",
                            "resource": {"R1": 1,
                                         "R2": 2,
                                         "R3": 3,
                                         "R4": 4,
                                         "R5": 5,
                                         "R6": 0},
                            "weapon_name": "RemoteAccess",
                            "power": {},
                            "score": {"cost": 3.0,
                                      "spend_time": 2,
                                      "success_rate": 3.0,
                                      "invisibility": 1.7999999999999998},
                            "node_weapon_id": "12",
                            "node_name": "Device02"},
                           {"weapon_id": "20",
                            "node_score": 10.0,
                            "node_id": "20",
                            "resource": {"R1": 0,
                                         "R2": 0,
                                         "R3": 0,
                                         "R4": 0,
                                         "R5": 0,
                                         "R6": 0},
                            "weapon_name": "AttackHMI/ExploitCVE-2014-0751",
                            "power": {},
                            "score": {"cost": 2.0,
                                      "spend_time": 1,
                                      "success_rate": 1.2,
                                      "invisibility": 1.2},
                            "node_weapon_id": "20",
                            "node_name": "ElectricDevice"},
                           {"weapon_id": "3",
                            "node_score": 9.0,
                            "node_id": "3",
                            "resource": {"R1": 0,
                                         "R2": 0,
                                         "R3": 0,
                                         "R4": 0,
                                         "R5": 0,
                                         "R6": 0},
                            "weapon_name": "EmailExploitCVE-2014-4114",
                            "power": {},
                            "score": {"cost": 1.0,
                                      "spend_time": 1,
                                      "success_rate": 0.7,
                                      "invisibility": 0.6},
                            "node_weapon_id": "3",
                            "node_name": "Device02"},
                           {"weapon_id": "-1",
                            "node_score": 0,
                            "node_id": "-1",
                            "resource": {"R1": 0,
                                         "R2": 0,
                                         "R3": 0,
                                         "R4": 0,
                                         "R5": 0,
                                         "R6": 0},
                            "weapon_name": "virtual_end_tool",
                            "power": {},
                            "score": {"cost": 0,
                                      "spend_time": 0,
                                      "success_rate": 1,
                                      "invisibility": 0},
                            "node_weapon_id": "-1",
                            "node_name": "virtual_end_device"}],
                 "edges": [{"source_id": "3",
                            "source_name": "Device02+EmailExploitCVE-2014-4114",
                            "target_name": "Device02+GetVPNInfo",
                            "target_id": "5",
                            "and": ""},
                           {"source_id": "3",
                            "source_name": "Device02+EmailExploitCVE-2014-4114",
                            "target_name": "Device02+RemoteAccess",
                            "target_id": "12",
                            "and": ""},
                           {"source_id": "3",
                            "source_name": "Device02+EmailExploitCVE-2014-4114",
                            "target_name": "ElectricDevice+AttackHMI/ExploitCVE-2014-0751",
                            "target_id": "20",
                            "and": ""},
                           {"source_id": "5",
                            "source_name": "Device02+GetVPNInfo",
                            "target_name": "Device02+RemoteAccess",
                            "target_id": "12",
                            "and": ""},
                           {"source_id": "20",
                            "source_name": "ElectricDevice+AttackHMI/ExploitCVE-2014-0751",
                            "target_name": "virtual_end_device+virtual_end_tool",
                            "target_id": "-1",
                            "and": ""},
                           {"source_id": "12",
                            "source_name": "Device02+RemoteAccess",
                            "target_name": "ElectricDevice+AttackHMI/ExploitCVE-2014-0751",
                            "target_id": "20",
                            "and": ""}],
                 "score": {"spend_time": 8.0,
                           "efficacy": 400,
                           "success_rate": 0.0,
                           "cost": 10.0,
                           "invisibility": 6.0,
                           "node_number": 5},
                 "wuqi": ["EmailExploitCVE-2014-4114",
                          "GetVPNInfo",
                          "RemoteAccess",
                          "AttackHMI/ExploitCVE-2014-0751",
                          "virtual_end_tool"]}
    numTasks, num_To_nodes_weapon_id_dic = get_format_input_data(
        data_info["nodes"], data_info["edges"], "teste77.sm")
    print numTasks, num_To_nodes_weapon_id_dic
