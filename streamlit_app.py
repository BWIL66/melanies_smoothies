# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie ! :cup_with_straw: {st.__version__}")
st.write(
  """**Choose the fruits you want in your custom smoothie!**"""
)

name_on_order = st.text_input("Name on Smoothie :")
st.write("The name of your smoothie will be", name_on_order)


# option = st.selectbox(
#     "What is your favorite fruit ?",
#     ("Bananas", "strawberries", "Peaches"),
# )
#st.write("You selected:", option)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    "**Choose up to 5 ingredients**",
    #["Dragon Fruit", "Guava", "Jackfruit", "Elderberries", "Kiwi"],
    my_dataframe,
    #default=["Yellow", "Red"],
    max_selections=5
)


if ingredients_list :
    #st.write("You selected:", ingredients_list)
    #st.text(ingredients_list)
    
    ingredients_string='';

    for fruit_chosen in ingredients_list :
        ingredients_string += fruit_chosen + ' '
    st.text(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert :
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
    #st.write(my_insert_stmt)    
    #if ingredients_string:
    #    session.sql(my_insert_stmt).collect()

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response.json())
