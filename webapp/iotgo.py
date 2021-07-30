import streamlit as st
import streamlit.components.v1 as components

#streamlit.components.v1.html(html, width=None, height=None, scrolling=False)
urlis="https://makecode.microbit.org/--docs?md=%23%23%0A%0A%60%60%60%20blocks%0Abasic.pause%281000%29%0Abasic.forever%28function%20%28%29%20%7B%0A%20%20%20%20if%20%28input.temperature%28%29%20%3E%2028%29%7B%0A%20%20%20%20%20%20%20%20basic.showIcon%28IconNames.Sad%29%0A%20%20%20%20%20%20%20%20basic.pause%28100%29%0A%20%20%20%20%20%7D%20else%20%7Bbasic.clearScreen%28%29%0A%20%20%20%20%20%20%20%20basic.pause%28100%29%0A%20%20%20%20%7D%0A%7D%29%0A%60%60%60%0A%0A%0A"
# embed streamlit docs in a streamlit app
st.header("My cards are:")

col1, emptycol, col3, col4, col5, col6 = st.beta_columns(6)

with col1:
    st.write("Mission:")
    st.image("https://snap.inf.unibz.it/img/mission/mission3.jpg", width=175)
with col3:
    st.write("Persona:")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=95)
with col4:
    st.write("Thing:")
    st.image("https://snap.inf.unibz.it/img/environment/t-shirt.jpg", width=100)
with col5:
    st.write("Input:")
    st.image("https://snap.inf.unibz.it/img/input/button.jpg", width=100)
with col6:
    st.write("Output:")
    st.image("https://snap.inf.unibz.it/img/output/icon.jpg", width=100)
st.header("My code is:")
components.iframe(urlis,width=800, height=900)#, scrolling=False)
