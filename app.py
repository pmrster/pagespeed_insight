import streamlit as st 
from datetime import datetime

from website_insight.pagespeed_insight import GetPageSpeedInsight
from login import login_modal

app_token = st.secrets["APP_TOKEN"]

st.set_page_config(
    page_title="Get pagespeed insight",
    page_icon="🧑‍💻",
    layout="wide"
)

if 'login_key' not in st.session_state:
    st.session_state['login_key'] = None
    
if 'ps_mobile' not in st.session_state:
    st.session_state['ps_mobile'] = None
    
if 'ps_desktop' not in st.session_state:
    st.session_state['ps_desktop'] = None


input_key = st.session_state.login_key 

st.header('💻:gray[Get your] :blue[_Website Performance_] :gray[from] :blue[_PageSpeed_]')

if input_key  == app_token:
    print("start time from main page: ",datetime.now().strftime('%Y-%m-%d, %H:%M:%S'))

    user_website = st.text_input(label="Insert your website url with `https://...`", value="https://medium.com")
    get_button = st.button(label="Get insight!",type="primary")
    
    
    if get_button:
        
        # print("user press button!")
        container1, container2 = st.columns(2,gap="small")
        ## mobile container
        with container1:
            with st.container(border=True):
                with st.spinner("Running mobile performance.."):
                    st.session_state["ps_mobile"] = GetPageSpeedInsight(website=user_website, device="mobile").get_insight()
                    
                    if st.session_state["ps_mobile"]:
                        get_mobile_insight = st.session_state["ps_mobile"]
                        # st.write("mobile insight\n", get_mobile_insight)
                        st.subheader("**Mobile Performance**")
                        mb_col1, mb_col2 = st.columns(2,gap="small")
                        with mb_col1:
                            st.image(image=get_mobile_insight["img_file_decode"], caption="mobile")
                        with mb_col2:
                            st.markdown(f'''
                                        :blue-background[**Performance**]:  **{get_mobile_insight["performance_score"]}**\n
                                        :blue-background[**Accessibility**]:  **{get_mobile_insight["accessibility_score"]}**\n
                                        :blue-background[**Best Practices**]:  **{get_mobile_insight["best_practices_score"]}**\n
                                        :blue-background[**SEO**]:  **{get_mobile_insight["seo_score"]}**
                                        ''')                
                            # st.subheader(f"**Performance:** {get_mobile_insight['performance_score']}" )
                            # st.subheader(f"**Accessibility:** {get_mobile_insight['accessibility_score']}" )
                            # st.subheader(f"**Best Practices:** {get_mobile_insight['best_practices_score']}" )
                            # st.subheader(f"**SEO:** {get_mobile_insight['seo_score']}" )
            
                
                
        ## desktop container
        with container2:
            with st.container(border=True):
                with st.spinner("Running desktop performance.."):

                    st.session_state["ps_desktop"] = GetPageSpeedInsight(website=user_website, device="desktop").get_insight()

                        
                    if st.session_state["ps_desktop"]:
                        get_desktop_insight = st.session_state["ps_desktop"]
                        
                        # st.write("desktop insight\n", get_desktop_insight)
                        st.subheader("**Desktop Performance**")
                        dt_col1, dt_col2 = st.columns(2,gap="small")
                        with dt_col1:
                            st.image(image=get_desktop_insight["img_file_decode"], caption="desktop")
                        with dt_col2:
                            st.markdown(f'''
                                        :blue-background[**Performance**]:  **{get_desktop_insight["performance_score"]}**\n
                                        :blue-background[**Accessibility**]:  **{get_desktop_insight["accessibility_score"]}**\n
                                        :blue-background[**Best Practices**]:  **{get_desktop_insight["best_practices_score"]}**\n
                                        :blue-background[**SEO**]:  **{get_desktop_insight["seo_score"]}**
                                        ''') 
                            # st.subheader(f"**Performance:** {get_desktop_insight['performance_score']}" )
                            # st.subheader(f"**Accessibility:** {get_desktop_insight['accessibility_score']}" )
                            # st.subheader(f"**Best Practices:** {get_desktop_insight['best_practices_score']}" )
                            # st.subheader(f"**SEO:** {get_desktop_insight['seo_score']}" )
                
        print("end...")
else:
    st.write("please fill a correct key")
    login_modal()    
