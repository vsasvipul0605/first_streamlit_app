import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("Snowflake Trial")

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Apple','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

#1
def get_fruityvice_data(fruit):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')  
  if not fruit_choice:
    streamlit.error("Please select fruit")
  else:
    result=get_fruityvice_data(fruit_choice)  
    streamlit.dataframe(result)
except URLError as e:
  streamlit.error()

  #2
streamlit.header("The FRUIT LOAD LIST TABLE contains")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()

if streamlit.button('GET fruit load list table rows'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

  
 #3
def insert_row_snowflake(fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO fruit_load_list VALUES ('"+fruit+"')")
    return "Thanks for adding "+ fruit

fruit_choice = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add fruit to list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  result = insert_row_snowflake(fruit_choice)
  my_cnx.close()
  streamlit.text(result)
