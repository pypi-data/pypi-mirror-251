import re
import json
from .transform import find_json, to_json_desc

def check_structure(origin: any, compare_target: any, position: str=""):
    errors = []
    if isinstance(origin, dict):
        for key in origin.keys():
            current_position = position + "." + key
            if key not in compare_target:
                errors.append(current_position[1:])
            check_result = check_structure(origin[key], compare_target[key], current_position)
            if check_result != True:
                errors.extend(check_result)
    if isinstance(origin, list):
        for index, item in enumerate(origin):
            current_position = position + "." + str(index)
            if index in enumerate(compare_target):
                check_result = check_structure(item, compare_target[index], current_position)
                if check_result != True:
                    errors.extend(check_result)
    if len(errors) == 0:
        return True
    else:
        return errors

async def fix_json_structure(origin: str, input_dict: any, output_dict: any, request: object, *, is_debug: bool=False, errors = list):
    try:
        '''
        fixed_result = request\
            .input({
                "this JSON is mean to do": input_dict,
                "expect structure": to_json_desc(output_dict),
                "error JSON String": origin ,
                "error": "structure of {error JSON String} is not the same as {except structure}",
                "error position": errors,
            })\
            .output('FIXED {error JSON String} JSON STRING ONLY WITHOUT EXPLANATION that can be parsed by Python')\
            .start()
        '''
        fixed_result = await request\
            .input({
                "error JSON String": origin ,
                "error": "structure of {error JSON String} is not the same as {except structure}",
                "error position": errors,
            })\
            .output('FIXED {error JSON String} JSON STRING ONLY WITHOUT EXPLANATION that can be parsed by Python')\
            .start_async()
        json_string = find_json(fixed_result)
        if is_debug:
            print("[Cleaned JSON String]:\n", json_string)
            print("\n--------------------------\n")
        fixed_result = json.loads(json_string)
        if is_debug:
            print("[Parse JSON to Dict] Done")
            print("\n--------------------------\n")
        return fixed_result
    except Exception as e:
        raise Exception(f"[Agent Request] Error still occured when try to fix JSON decode error: { str(e) }")

async def fix_json_format(origin: str, input_dict: any, output_dict: any, request: object, *, is_debug: bool=False, error: str, position: str):
    try:
        '''
        fixed_result = request\
            .input({
                "this JSON is mean to do": input_dict,
                "expect format": to_json_desc(output_dict),
                "error JSON String": origin ,
                "error": error,
                "error position": position,
            })\
            .output('FIXED {error JSON String} JSON STRING ONLY WITHOUT EXPLANATION that can be parsed by Python')\
            .start()
        '''
        fixed_result = await request\
            .input({
                "error JSON String": origin ,
                "error": error,
                "error position": position,
            })\
            .output('FIXED {error JSON String} JSON STRING ONLY WITHOUT EXPLANATION that can be parsed by Python')\
            .start_async()
        json_string = find_json(fixed_result)
        if is_debug:
            print("[Cleaned JSON String]:\n", json_string)
            print("\n--------------------------\n")
        fixed_result = json.loads(json_string)
        if is_debug:
            print("[Parse JSON to Dict] Done")
            print("\n--------------------------\n")
        return fixed_result
    except Exception as e:
        raise Exception(f"[Agent Request] Error still occured when try to fix JSON decode error: { str(e) }")

async def load_json(origin: str, input_dict: any, output_dict: any, request: object, *, is_debug: bool=False):
    try:
        json_string = find_json(origin)
        if is_debug:
            print("[Cleaned JSON String]:\n", json_string)
            print("\n--------------------------\n")
        parsed_dict = json.loads(json_string)
        '''
        check_structure_result = check_structure(parsed_dict, output_dict)
        if check_structure_result != True:
            if is_debug:
                print("[JSON Structure Do Not As Expect] Start Fixing Process...")
            return fix_json_structure(json_string, input_dict, output_dict, request, is_debug = is_debug, errors = check_structure_result)
        else:
            if is_debug:
                print("[Parse JSON to Dict] Done")
                print("\n--------------------------\n")
            return parsed_dict
        '''
        return parsed_dict
    except json.JSONDecodeError as e:
        if is_debug:
            print("[JSON Decode Error Occurred] Start Fixing Process...")
        return await fix_json_format(json_string, input_dict, output_dict, request, is_debug = is_debug, error = e.msg, position = e.pos)
    except Exception as e:
        if is_debug:
            print("[JSON Decode Error Occurred] Start Fixing Process...")
        return await fix_json_structure(origin, input_dict, output_dict, request, is_debug = is_debug, errors = [str(e)])