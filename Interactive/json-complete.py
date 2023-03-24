import os
import json
import sys
from jsonschema import validate, Draft7Validator, draft7_format_checker, RefResolver


def check_file_existence(file_path):
    """检查文件是否存在"""
    if not os.path.exists(file_path):
        return False
    return True


def read_json_file(file_path):
    """读取JSON文件"""
    with open(file_path, 'r') as f:
        return json.load(f)


def write_json_file(file_path, json_data):
    """写入JSON文件"""
    with open(file_path, 'w') as f:
        json.dump(json_data, f, indent=4)


def validate_json_data(json_data, schema_data):
    """验证JSON数据是否符合JSON Schema标准"""
    validator = Draft7Validator(
        schema_data, format_checker=draft7_format_checker)
    errors = sorted(validator.iter_errors(json_data), key=lambda e: e.path)
    if errors:
        for error in errors:
            del json_data[str(list(error.path)[0])]
        return False
    return True


def prompt_user_to_create_json_file(file_path):
    """提示用户创建JSON文件"""
    print(f"文件{file_path}不存在，请先创建它！")
    user_input = input("请输入JSON文件内容：")
    try:
        json_data = json.loads(user_input)
        write_json_file(file_path, json_data)
        return json_data
    except ValueError:
        print("输入的JSON格式不正确，请重新输入！")
        prompt_user_to_create_json_file(file_path)


def prompt_user_to_complete_json_data(json_data, schema_data):
    """引导用户补全缺失的键值对"""
    errors = sorted(
        Draft7Validator(
            schema_data, format_checker=draft7_format_checker
        ).iter_errors(json_data),
        key=lambda e: e.path
    )
    for error in errors:
        key_path = error.path
        current = json_data
        for key in key_path:
            if key not in current:
                current[key] = {}
            current = current[key]
        user_input = input(f"请输入缺失的键值对：{key_path}: ")
        try:
            value = json.loads(user_input)
            current[key_path[-1]] = value
        except ValueError:
            print("输入的JSON格式不正确，请重新输入！")
            prompt_user_to_complete_json_data(json_data, schema_data)


def validate_and_complete_json_file(json_file_path, schema_file_path):
    """验证JSON文件是否符合JSON Schema标准，并补全缺失的键值对"""
    if not check_file_existence(json_file_path):
        json_data = prompt_user_to_create_json_file(json_file_path)
    else:
        json_data = read_json_file(json_file_path)

    schema_data = read_json_file(schema_file_path)

    while not validate_json_data(json_data, schema_data):
        prompt_user_to_complete_json_data(json_data, schema_data)

    write_json_file(json_file_path, json_data)
    print("JSON文件符合JSON Schema标准并保存成功！")

