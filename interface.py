# import streamlit as st
# import pandas as pd
# import numpy as np
#
#
# left_column, middle_column, right_column = st.columns(3)
# # You can use a column just like st.sidebar:
# with left_column:
#     txt = st.text_area('Query', height=10, placeholder="Please input your query")
#     st.button("Submit")
#
# with middle_column:
#     txt = st.text_area('QEP plan', height=10, placeholder="Please input your query")
#
#
# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")