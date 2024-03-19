# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """choose the fruits you want in your smoothie!
       """
)

#option = st.selectbox(
#    'what is your faverate fruits?',
#    ('choose one','Banana', 'Apple', 'Cherry'))

#st.write('Your faverate fruit is:', option)

name_on_order = st.text_input('name on smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

# session = get_active_session() #this is an extra session and no need, cause error which Baily helped me to comments out

my_df=session.table("smoothies.public.fruit_options").select(col("Fruit_Name"))
# st.dataframe(data=my_dataframe, use_container_width=True)

# ingredients_list=st.multiselect('choose up to 5 ingredients:', my_df)

ingredients_list=st.multiselect('choose up to 5 ingredients:'
                                , my_df
                                , max_selections=5
                               )

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for each_fruit_chosen in ingredients_list:
        ingredients_string+=each_fruit_chosen + ' '    
        st.subheader(each_fruit_chosen + "Nutrition information")
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + each_fruit_chosen )
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop

    time_to_insert=st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your smoothie ordered,' + name_on_order + '!', icon="✔")


