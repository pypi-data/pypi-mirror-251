import numpy as np
import pandas as pd


def get_data_type(data):
    data_type = type(data)
    if data_type == type([[]]):
        return "list"
    elif data_type == type({}):
        return "dict"
    elif data_type == type(pd.DataFrame()):
        return "dataFrame"
    elif data_type == type(np.array([])):
        return "numpy"
    elif data_type == type(""):
        return "string"
    else:
        return "other"


def list_to_numpy(data):
    result = []
    for i in range(len(data)):
        result.append(np.array(data[i]))
    return np.array(result)


def list_to_dict(data):
    data = list_to_numpy(data)
    result = {}
    # 设置列名
    head = data[0]
    data = np.delete(data, 0, 0)
    for i in range(len(head)):
        result[str(head[i])] = data[:, i]
    return result


def dict_to_dataframe(data):
    return pd.DataFrame(data)


def list_to_dataframe(data):
    data = list_to_dict(data)
    return dict_to_dataframe(data)


def numpy_to_dataframe(data):
    return pd.DataFrame(data)


def csv_to_dataframe(data):
    return pd.read_csv(data)


def excel_to_dataframe(data):
    return pd.read_excel(data)


def change_type_to_dataframe(data, data_type):
    result = pd.DataFrame()
    if data_type == "list":
        result = list_to_dataframe(data)
    elif data_type == "dict":
        result = dict_to_dataframe(data)
    elif data_type == "dataFrame":
        result = data
    elif data_type == "numpy":
        result = numpy_to_dataframe(data)
    elif data_type == "string":
        if data.endswith(".csv"):
            result = csv_to_dataframe(data)
        elif data.endswith(".xlsx"):
            result = excel_to_dataframe(data)
    return result
