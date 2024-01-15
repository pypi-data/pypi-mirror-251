import pandas as pd

from featureuitls import typeUtils


feature_name_flag = "FEATURE_NAME"
feature_value_flag = "FEATURE_VALUE"
info_flag = "[ALIOTH - INFO - <feature>] "  # <feature>为占位符
error_flag = "[ALIOTH - ERROR] "


def print_error_info(info_type):
    if info_type == "feature_name":
        print(error_flag + "wrong feature_name type, please input string or list")
    elif info_type == "data":
        print(error_flag + "wrong data type, please check your data type")


def print_feature_name(feature_name):
    result = "["
    for feature in feature_name:
        result += "\"" + feature + "\","
    result = result[:-1] + "]"
    print(info_flag.replace("<feature>", feature_name_flag) + result)


def print_feature_value(feature_name, feature_value):
    for feature in feature_name:
        temp = feature_value[feature]
        print_str = "["
        for value in temp:
            print_str += "\"" + str(value) + "\","
        print_str = print_str[:-1] + "]"
        print(info_flag.replace("<feature>", feature_value_flag) + feature + ": " + print_str)


def get_feature_info(data, feature_name):
    """
    获取特征信息
    :param data: 数组、字典、dataFrame、numpy.array、csv、excel（表格使用路径传入）
    :param feature_name: string、list
    :return: 输出信息至控制台
    """
    # 判断feature_name格式，支持string & list
    feature_name_list = []
    feature_name_type = typeUtils.get_data_type(feature_name)
    if feature_name_type == "string":
        feature_name_list.append(feature_name)
    elif feature_name_type == "list":
        feature_name_list = feature_name
    else:
        print_error_info("feature_name")
        return
    # 格式转换为DataFrame
    data_type = typeUtils.get_data_type(data)
    df_data = pd.DataFrame()
    if data_type == "other":
        print_error_info("data")
        return
    else:
        try:
            df_data = typeUtils.change_type_to_dataframe(data, data_type)
        except Exception as e:
            print_error_info("data")
        if df_data.empty:
            print_error_info("data")
    # 解析
    print_feature_name(feature_name_list)
    print_feature_value(feature_name_list, df_data)
