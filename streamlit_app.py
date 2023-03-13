# Code for a snowflake course 
# bad structure of this file is due to i want to keep the code inte the order that is it presented throughout the course 

import streamlit
import pandas as pd 
import requests
import snowflake.connector
from urllib.error import URLError
import folium
from streamlit_folium import st_folium, folium_static



m = folium.Map(location=[57.708870, 11.974560], zoom_start=6)

tooltip = "Click me!"

folium.Marker(
    [56.260860, 12.550790], popup="<p>Holy Smoke BBQ</p> <p>Recesent: Dagen nyheter  Betyg: 5/5 L&auml;nk: https://www.dn.se/kultur/holy-smoke-skansk-barbecue-pa-riktigt/</p>", tooltip=tooltip
).add_to(m)
folium.TileLayer('cartodbdark_matter').add_to(m)

st_data = st_folium(m, width=700)


streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


#Loading data
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvce_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
  
try: 
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice: 
    streamlit.error('Please select a fruit to get information.')
  else:
    streamlit.dataframe(get_fruityvce_data(fruit_choice))
except URLError as e: 
  streamlit.error()

streamlit.header("View out fruit list - Add your favorites!:")
# snowflake related function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        function_return = my_cur.fetchall()
        return function_return
    
# Add a button to load the fruit
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)


# allow the end user to add a fruit to the list 
def insert_row_into_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('{}');".format(new_fruit))
        return "Thanks for adding " + new_fruit
  
add_my_fruit = streamlit.text_input('What fruit would you like add to the list?')
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_into_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)




