import requests
import json
import os
import sys
from taipy import Gui
import pandas

API_BASE="https://api.coingecko.com/api/v3"
COIN_LIST_SERVICE="/coins/list"
SIMPLE_PRICE_SERVICE="/simple/price"
COIN_LIST_FILE="coin_list.json"
API_KEY_FILE="api.key"
api_key=""

coinList=[]
coinJson=[]

def cg_api_request(service, parameters):
    url=API_BASE+service
    r=requests.get(url, params=parameters)
    return r

def get_coin_list(parameters):
    if os.path.exists(COIN_LIST_FILE)==False:
        print("Making API call")
        r=cg_api_request(COIN_LIST_SERVICE, parameters)
        with open(COIN_LIST_FILE, "w", encoding="utf-8") as f:
            f.write(r.text)
        return json.loads(r.text)
    else:
        with open(COIN_LIST_FILE, "r", encoding="utf-8") as f:
            print("Reading from file")
            content=f.read()
            return json.loads(content)

    return r

def table_clicked(state,var_name,payload):
    index=payload["index"]
    print(coinJson[index])
    parameters={"x_cg_demo_api_key":api_key,
                "ids":coinJson[index]["id"],
                "vs_currencies":"usd",
                "include_market_cap":"true",
                "include_24hr_vol":"true",
                "include_last_updated_at":"true"
                }
    r=cg_api_request(SIMPLE_PRICE_SERVICE, parameters)
    rjson=json.loads(r.text)
    print(rjson)


def main():
    global coinList
    global coinJson
    global api_key

    if os.path.exists(API_KEY_FILE)==False:
        print("API key file not found")
        sys.exit()
    else:
        with open(API_KEY_FILE, "r", encoding="utf-8") as f:
            api_key=f.read()
    parameters={"x_cg_demo_api_key":api_key}
    coinJson=get_coin_list(parameters)
    coinList=pandas.DataFrame(coinJson)
    
main()

page1="""
<|navbar|>
<|{coinList}|table|on_action=table_clicked|page_size=10|>
"""

page2="""
<|navbar|>
# Page 2
"""

pages={
	"Page1":page1,
	"Page2":page2
}

Gui(pages=pages).run(port="auto", use_reloader=True)