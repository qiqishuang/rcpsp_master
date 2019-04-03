# -*- coding: UTF-8 -*-
# function:运行文件，得到序列信息


from galgorithm_rcpsp import ga_processor
from format_input import get_format_input_data
from format_output import get_format_result_data


def run(nodes, edges):
    data_info["nodes"] = nodes
    data_info["edges"] = edges
    num_pop = 1
    num_pot = 2
    tx_slt = 2
    num_iter = 10
    inst_file = "teste7.sm"

    # 标准化输入
    numTasks, num_To_nodes_weapon_id_dic = get_format_input_data(data_info["nodes"], data_info["edges"], inst_file)
    # 遗传算法
    newGeneration, FtimeFit = ga_processor(numTasks, num_pop, num_pot, tx_slt, num_iter, inst_file)
    if newGeneration == -1:
        print "No solution, resources not enough for this task."
        return "No Solvelution! resources not enough for this task."
    # 格式化输出
    result = get_format_result_data(FtimeFit, num_To_nodes_weapon_id_dic, newGeneration, data_info)

    print "newGeneration", newGeneration
    print "num_To_nodes_weapon_id_dic", num_To_nodes_weapon_id_dic
    print "data_info", result
    return result


if __name__ == '__main__':

    data_info = {
    "nodes": [{
        "weapon_id": "5",
        "node_score": 9.0,
        "node_id": "5",
        "resource": {"R1": 1, "R2": 1, "R3": 1, "R4": 1, "R5": 1},
        "weapon_name": "GetVPNInfo",
        "power": {},
        "score": {
            "cost": 2.0,
            "spend_time": 0.1,
            "success_rate": 1.4,
            "invisibility": 1.2
        },
        "node_weapon_id": "5",
        "node_name": "Device02"
    }, {
        "weapon_id": "12",
        "node_score": 9.0,
        "node_id": "12",
        "resource": {"R1": 6, "R2": 6, "R3": 6, "R4": 6, "R5": 6},
        "weapon_name": "RemoteAccess",
        "power": {},
        "score": {
            "cost": 3.0,
            "spend_time": 360.0,
            "success_rate": 3.0,
            "invisibility": 1.7999999999999998
        },
        "node_weapon_id": "12",
        "node_name": "Device02"
    }, {
        "weapon_id": "20",
        "node_score": 10.0,
        "node_id": "20",
        "resource": {"R1": 5, "R2": 4, "R3": 3, "R4": 2, "R5": 1},
        "weapon_name": "AttackHMI/ExploitCVE-2014-0751",
        "power": {},
        "score": {
            "cost": 2.0,
            "spend_time": 0,
            "success_rate": 1.2,
            "invisibility": 1.2
        },
        "node_weapon_id": "20",
        "node_name": "ElectricDevice"
    }, {
        "weapon_id": "3",
        "node_score": 9.0,
        "node_id": "3",
        "resource": {"R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5},
        "weapon_name": "EmailExploitCVE-2014-4114",
        "power": {},
        "score": {
            "cost": 1.0,
            "spend_time": 0,
            "success_rate": 0.7,
            "invisibility": 0.6
        },
        "node_weapon_id": "3",
        "node_name": "Device02"
    }, {
        "weapon_id": "-1",
        "node_score": 0,
        "node_id": "-1",
        "resource": {"R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0},
        "weapon_name": "virtual_end_tool",
        "power": {},
        "score": {
            "cost": 0,
            "spend_time": 0,
            "success_rate": 1,
            "invisibility": 0
        },
        "node_weapon_id": "-1",
        "node_name": "virtual_end_device"
    }],
    "edges": [{
        "source_id": "3",
        "source_name": "Device02+EmailExploitCVE-2014-4114",
        "target_name": "Device02+GetVPNInfo",
        "target_id": "5",
        "and": ""
    }, {
        "source_id": "3",
        "source_name": "Device02+EmailExploitCVE-2014-4114",
        "target_name": "Device02+RemoteAccess",
        "target_id": "12",
        "and": ""
    }, {
        "source_id": "3",
        "source_name": "Device02+EmailExploitCVE-2014-4114",
        "target_name": "ElectricDevice+AttackHMI/ExploitCVE-2014-0751",
        "target_id": "20",
        "and": ""
    }, {
        "source_id": "5",
        "source_name": "Device02+GetVPNInfo",
        "target_name": "Device02+RemoteAccess",
        "target_id": "12",
        "and": ""
    }, {
        "source_id": "20",
        "source_name": "ElectricDevice+AttackHMI/ExploitCVE-2014-0751",
        "target_name": "virtual_end_device+virtual_end_tool",
        "target_id": "-1",
        "and": ""
    }, {
        "source_id": "12",
        "source_name": "Device02+RemoteAccess",
        "target_name": "ElectricDevice+AttackHMI/ExploitCVE-2014-0751",
        "target_id": "20",
        "and": ""
    }],
    "score": {
        "spend_time": 0,
        "efficacy": 400,
        "success_rate": 0.0,
        "cost": 10.0,
        "invisibility": 6.0,
        "node_number": 5
    },
    "wuqi": ["EmailExploitCVE-2014-4114", "GetVPNInfo", "RemoteAccess", "AttackHMI/ExploitCVE-2014-0751", "virtual_end_tool"]
    }

    new_nodes = run(data_info["nodes"], data_info["edges"])
