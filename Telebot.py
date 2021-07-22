import requests
from datetime import datetime
from requests.api import request
from requests.sessions import session
import time
import schedule

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
api_url_telegram = "https://api.telegram.org/bot1885900595:AAGicuJstdtn7EPhJfjcmBWXumUqY7PIBpw/sendMessage?chat_id=@__groupid__&text="
group_id = "kovai_covid_alert"
link = "Registration Link - https://selfregistration.cowin.gov.in"
tamilnadu_district_ids = [539]

def fetch_data_from_cowin(district_id):
    query_params = "?district_id={}&date={}".format(district_id, today_date)
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    final_url = base_cowin_url+query_params
    response = requests.get(final_url, headers=headers)
    extract_availability_data(response)
#    print(response.text)

def fetch_data_for_state(district_ids):
    for district_id in district_ids:
        fetch_data_from_cowin(district_id)

def extract_availability_data(response):
    response_json = response.json()
    i = 0
    for center in response_json["centers"]:
        i = i +1
        if i >3:
            break
        message = ""
        for session in center["sessions"]:
            if session["available_capacity_dose1"] > 0 and session["available_capacity_dose2"] > 0 and session["min_age_limit"]==18:
                message += "Center ID: {}, \nCenter Name: {}, \nAddress: {}, \nFee Type: {}, \nVaccine: {}, \nAvailable Dose1: {}, \nAvailable Dose2: {}, \nDate: {}, \nMinimum Age: {}, \nSlots: {}, \n-- -- -- -- -- -- -- --\n".format(
                    center["center_id"], center["name"], center["address"], center["fee_type"],
                    session["vaccine"], session["available_capacity_dose1"], session["available_capacity_dose2"], session["date"], session["min_age_limit"], session["slots"],                 
                )
#        print(message)
        send_message_telegram(message)

def send_message_telegram(message):
    final_telegram_url = api_url_telegram.replace("__groupid__",group_id)
    final_telegram_url = final_telegram_url + message + link
    response = requests.get(final_telegram_url)
    #print(response.text)

if __name__ == "__main__":
    fetch_data_for_state(tamilnadu_district_ids)
#    schedule.every(10).seconds.do(fetch_data_for_state(tamilnadu_district_ids))
#    while True:
#        schedule.run_pending()
#        time.sleep(1)