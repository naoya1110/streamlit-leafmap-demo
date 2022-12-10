import streamlit as st
import leafmap.foliumap as leafmap
import requests
from bs4 import BeautifulSoup

URL = 'http://www.geocoding.jp/api/'

lat = 35.658581
lon = 139.745433

def get_coordinate(address):
    payload = {'q': address}
    html = requests.get(URL, params=payload)
    soup = BeautifulSoup(html.content, "html.parser")
    if soup.find('error'):
        # raise ValueError(f"'{address}'はみつかりませんでした。")
        pass
    latitude = soup.find('lat').string
    longitude = soup.find('lng').string
    return latitude, longitude


with st.sidebar:
    st.title("streamlitとleafmapのデモ")

    with st.form(key="search_form"):
        address = st.text_input("検索する住所・名称")
        search_btn = st.form_submit_button("Search")
        
        lat, lon = get_coordinate(address)
        lat = float(lat)
        lon = float(lon)
        st.text(f"緯度 {lat}, 経度 {lon}")

if search_btn:
    map = leafmap.Map(location=[lat, lon],
                    height = 500,
                    width = 600,
                    zoom=16,
                    )
    
    map.add_basemap("SATELLITE")
    
    # 検索した住所にピンを立てる
    map.add_marker([lat, lon], popup=f"lat={lat}, lon={lon}",)

    map.to_streamlit(width=800, height=600)