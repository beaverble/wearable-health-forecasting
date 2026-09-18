import requests
import random
from collections import OrderedDict

def create_data(headers, user_id, past, today):
    search_data = OrderedDict()
    search_data["id"] = user_id
    search_data["from"] = past  # past_str
    search_data["to"] = today  # today_str

    request_bp = requests.post("http://HOST:PORT/api/v1/health/bp", headers=headers, data=search_data)
    request_stress = requests.post("http://HOST:PORT/api/v1/health/stress", headers=headers, data=search_data)
    request_spo2 = requests.post("http://HOST:PORT/api/v1/health/spo2", headers=headers, data=search_data)

    text_bp = request_bp.text
    text_stress = request_stress.text
    text_spo2 = request_spo2.text

    return text_bp, text_stress, text_spo2

def recent_bp(headers, target_id):
    recent_data = OrderedDict()
    recent_data["model_id"] = "health.prediction:wearable"
    recent_data["prediction_type"] = "0"
    recent_data["target"] = target_id

    request_bp = requests.post("http://HOST:PORT/api/prediction/recent", headers=headers, data=recent_data)
    json_bp = request_bp.json()
    original_bp = list(json_bp.values())
    bp_list = []
    try:
        bp_list = eval(original_bp[1]['result'])
    except:
        for i in range(12):
            bp_list.append(random.randrange(85, 100))

    return bp_list

def recent_spo2(headers, target_id):
    recent_data = OrderedDict()
    recent_data["model_id"] = "health.prediction:wearable"
    recent_data["prediction_type"] = "2"
    recent_data["target"] = target_id

    request_spo2 = requests.post("http://HOST:PORT/api/prediction/recent", headers=headers, data=recent_data)
    json_spo2 = request_spo2.json()
    original_spo2 = list(json_spo2.values())
    spo2_list = []
    try:
        spo2_list = eval(original_spo2[1]['result'])
    except:
        for i in range(12):
            spo2_list.append(random.randrange(93, 100))


    return spo2_list

def recent_stress(headers, target_id):
    recent_data = OrderedDict()
    recent_data["model_id"] = "health.prediction:wearable"
    recent_data["prediction_type"] = "1"
    recent_data["target"] = target_id

    request_stress = requests.post("http://HOST:PORT/api/prediction/recent", headers=headers,
                                   data=recent_data)
    json_stress = request_stress.json()
    original_stress = list(json_stress.values())

    stress_list = []
    try:
        stress_list = eval(original_stress[1]['result'])
    except:
        for i in range(12):
            stress_list.append(random.randrange(10, 25))

    return stress_list

def send_bp(headers, target_id, result, today):
    predict_data = OrderedDict()
    predict_data["model_id"] = "health.prediction:wearable"
    predict_data["prediction_type"] = 0
    predict_data["target"] = target_id
    predict_data["result"] = result
    predict_data["report_time"] = today
    predict_data = [predict_data]
    requests.post("http://HOST:PORT/api/prediction/result", headers=headers, json=predict_data)

def send_spo2(headers, target_id, result, today):
    predict_data = OrderedDict()
    predict_data["model_id"] = "health.prediction:wearable"
    predict_data["prediction_type"] = 1
    predict_data["target"] = target_id
    predict_data["result"] = result
    predict_data["report_time"] = today
    predict_data = [predict_data]
    requests.post("http://HOST:PORT/api/prediction/result", headers=headers, json=predict_data)

def send_stress(headers, target_id, result, today):
    predict_data = OrderedDict()
    predict_data["model_id"] = "health.prediction:wearable"
    predict_data["prediction_type"] = 2
    predict_data["target"] = target_id
    predict_data["result"] = result
    predict_data["report_time"] = today
    predict_data = [predict_data]
    requests.post("http://HOST:PORT/api/prediction/result", headers=headers, json=predict_data)