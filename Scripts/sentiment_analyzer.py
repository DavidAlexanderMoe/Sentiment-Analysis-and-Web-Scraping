import streamlit as st

st.title('Sentiment Analyzer App')
st.write('Welcome to my sentiment analysis app!')
form = st.form(key='sentiment-form')
user_input = form.text_area('Enter your text')
submit = form.form_submit_button('Submit')