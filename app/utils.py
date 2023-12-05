import constants
import http.client
import urllib.parse
import json
import logging

def get_horoscope(day: str, sunsign: str) -> dict:
    conn = http.client.HTTPSConnection(constants.RAPID_API_HOST)
    
    headers = {
        'X-RapidAPI-Key': constants.RAPID_API_KEY,
        'X-RapidAPI-Host': constants.RAPID_API_HOST
    }
    
    url = "/horoscope"
    params = {
        "day": day,
        "sunsign": sunsign
    }    
    params_encoded = urllib.parse.urlencode(params)
    url = url + "?" + params_encoded
    
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    logging.warning(res)
    data = res.read()
    logging.warning(data)

    conn.close()

    horoscope_dict = json.loads(data)
    return horoscope_dict

def get_tarot_card() -> dict:
    conn = http.client.HTTPSConnection(constants.RAPID_API_HOST)
    
    headers = {
        'X-RapidAPI-Key': constants.RAPID_API_KEY,
        'X-RapidAPI-Host': constants.RAPID_API_HOST
    }
    
    url = "/tarotcard"
    params = {}    
    params_encoded = urllib.parse.urlencode(params)
    url = url + "?" + params_encoded
    
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    logging.warning(res)
    data = res.read()
    logging.warning(data)

    conn.close()

    res_dict = json.loads(data)
    return res_dict