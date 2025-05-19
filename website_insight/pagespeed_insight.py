import os
import json
from datetime import datetime
import requests
import base64
import streamlit as st

pagespeed_api_key = st.secrets["GOOGLE_API_KEY"]


def get_data(response_data):
    print("trying to get data from page speed response")
    result = json.loads(response_data.text)
    print("test_mobile : ", result["lighthouseResult"]["categories"]["performance"]["score"] * 100)
    
    ##image
    ss_encoded_img = result["lighthouseResult"]["audits"]["final-screenshot"]["details"]["data"].replace("data:image/jpeg;base64,", "")
    ss_decoded_img = base64.b64decode(ss_encoded_img)
    print(ss_decoded_img[0:50])
    
    
    ### prepare perf score
    performance_score = {
      "performance_score": round(result["lighthouseResult"]["categories"]["performance"]["score"] * 100),
      "accessibility_score": round(result["lighthouseResult"]["categories"]["accessibility"]["score"] * 100),   
      "best_practices_score": round(result["lighthouseResult"]["categories"]["best-practices"]["score"] * 100),
      "seo_score": round(result["lighthouseResult"]["categories"]["seo"]["score"] * 100),
      "img_file_decode": ss_decoded_img,
      # "pwa_score": round(result["lighthouseResult"]["categories"]["pwa"]["score"] * 100),
    }
    # print(f"result data: {performance_score}")
    return performance_score



class GetPageSpeedInsight:
    def __init__(self, website, device):
        self.website = website
        self.device = device
      
    def get_insight(self):
        print(f"calling pagespeed api for {self.device} insight with {self.website}")
        request_url_mobile = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + self.website + "&key=" + pagespeed_api_key + "&category=PERFORMANCE&category=ACCESSIBILITY&category=BEST_PRACTICES&category=PWA&category=SEO" + f"&strategy={self.device}"
        
        try:
            response = requests.get(request_url_mobile)
            # print(" req: ", response)
            if response.status_code != 200:
                print("error: ", response.text)
                
            print(f"finish request for {self.device}")
            final_result = get_data(response)

            return final_result

        except Exception as e:
            print(f"error on page speed calling getting insight: {e}")
            st.write(f"got and error ({e}), please recheck your website url")
