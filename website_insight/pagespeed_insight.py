import os
import json
from dotenv import load_dotenv
from datetime import datetime
import requests
import base64
# import streamlit as st

load_dotenv()

pagespeed_api_key = os.environ.get("GOOGLE_API_KEY")

# pagespeed_api_key = st.secret["GOOGLE_API_KEY"]

def call_page_speed(website_url):
    print(f"calling pagespeed api with {website_url}")

    request_url_mobile = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + website_url + "&key=" + pagespeed_api_key + "&category=PERFORMANCE&category=ACCESSIBILITY&category=BEST_PRACTICES&category=PWA&category=SEO" + "&strategy=mobile"
    request_url_desktop = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + website_url + "&key=" + pagespeed_api_key + "&category=PERFORMANCE&category=ACCESSIBILITY&category=BEST_PRACTICES&category=PWA&category=SEO" + "&strategy=desktop"

    try:
        response_mobile = requests.get(request_url_mobile)
        print("mobile req: ", response_mobile)
        if response_mobile.status_code != 200:
          print("error: ", response_mobile.text)
        print("finish request for mobile")

        response_desktop = requests.get(request_url_desktop)
        print("desktop req: ", response_desktop)
        if response_desktop.status_code != 200:
          print("error: ", response_desktop.text)
        print("finish request for desktop")
        return response_mobile, response_desktop

    except Exception as e:
      print(f"error on page speed calling: {e}")



def get_pagespeed_data(website_url):
  print("trying to get data from page speed response")
  try:
    pagespeed_response = call_page_speed(website_url)
    mobile_result = json.loads(pagespeed_response[0].text)
    print("finish get mobile")
    print("test_mobile : ", mobile_result["lighthouseResult"]["categories"]["performance"]["score"] * 100)
    
    desktop_result = json.loads(pagespeed_response[1].text)
    print("finish get desktop")
    print("test_desktop : ", desktop_result["lighthouseResult"]["categories"]["performance"]["score"] * 100)
    
    
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(current_dir, "output_file_path")
    print("output folder path:", output_file_path)
    
    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)
        print("finish make dir")
        
        
        
    ### save image
    
    ss_encoded_mobile_img = mobile_result["lighthouseResult"]["audits"]["final-screenshot"]["details"]["data"].replace("data:image/jpeg;base64,", "")
    ss_decoded_mobile_img = base64.b64decode(ss_encoded_mobile_img)
    print(ss_decoded_mobile_img[0:50])
    # current_time = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"


    with open(f"{output_file_path}/lh_screenshot_mobile.jpg", "wb+") as f:
        f.write(ss_decoded_mobile_img)
    
  
    ss_encoded_desktop_img = desktop_result["lighthouseResult"]["audits"]["final-screenshot"]["details"]["data"].replace("data:image/jpeg;base64,", "")
    ss_decoded_desktop_img = base64.b64decode(ss_encoded_desktop_img)
    print(ss_decoded_desktop_img[0:50])
    with open(f"{output_file_path}/lh_screenshot_desktop.jpg", "wb+") as f:
        f.write(ss_decoded_desktop_img)

    mobile_performance_score = {
      "req_url": website_url,
      "performance_score": round(mobile_result["lighthouseResult"]["categories"]["performance"]["score"] * 100),
      "accessibility_score": round(mobile_result["lighthouseResult"]["categories"]["accessibility"]["score"] * 100),   
      "best_practices_score": round(mobile_result["lighthouseResult"]["categories"]["best-practices"]["score"] * 100),
      "seo_score": round(mobile_result["lighthouseResult"]["categories"]["seo"]["score"] * 100),
      "img_file_name": f"{output_file_path}/lh_screenshot_mobile.jpg"
      # "pwa_score": round(mobile_result["lighthouseResult"]["categories"]["pwa"]["score"] * 100),
    }
    print(f"mobile data: {mobile_performance_score}")
    
    desktop_performance_score = {
        "req_url": website_url,
        "performance_score": round(desktop_result["lighthouseResult"]["categories"]["performance"]["score"] * 100),
        "accessibility_score": round(desktop_result["lighthouseResult"]["categories"]["accessibility"]["score"] * 100),   
        "best_practices_score": round(desktop_result["lighthouseResult"]["categories"]["best-practices"]["score"] * 100),
        "seo_score": round(desktop_result["lighthouseResult"]["categories"]["seo"]["score"] * 100),
        "img_file_name": f"{output_file_path}/lh_screenshot_desktop.jpg"
        # "pwa_score": round(desktop_result["lighthouseResult"]["categories"]["pwa"]["score"] * 100),
    }
    print(f"desktop data: {desktop_performance_score}")
    
  except Exception as e:
    print(f"error on get pagespeed, we will using mock data for this website: {website_url}")
    mobile_performance_score = {
      "req_url": website_url,
      "performance_score": "-",
      "accessibility_score": "-",   
      "best_practices_score": "-",
      "seo_score": "-",
      "img_file_name": "noimg"
      # "pwa_score": "-",
    }
    print(f"mobile data: {mobile_performance_score}")
    
    desktop_performance_score = {
        "req_url": website_url,
        "performance_score": "-",
        "accessibility_score": "-",   
        "best_practices_score": "-",
        "seo_score": "-",
        "img_file_name": "noimg"
        # "pwa_score": "-",
    }
    print(f"desktop data: {desktop_performance_score}")
  
  return desktop_performance_score, mobile_performance_score


if __name__ == "__main__":
  desktop_performance_score, mobile_performance_score = get_pagespeed_data("https://medium.com")
  print("desktop result:\n",desktop_performance_score)
  print("mobile result:\n",mobile_performance_score)