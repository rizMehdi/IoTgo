import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(page_title="IoTgo",page_icon=None,layout="wide")
urlis="https://makecode.microbit.org/--docs?md=%0A%0A%60%60%60%20blocks%0Abasic.pause%281000%29%0Abasic.forever%28function%20%28%29%20%7B%0A%20%20%20%20if%20%28input.temperature%28%29%20%3E%3D%2028%29%7B%0A%20%20%20%20%20%20%20%20pins.digitalWritePin%28DigitalPin.P1%2C1%29%0A%20%20%20%20%20%20%20%20basic.pause%28100%29%0A%20%20%20%20%20%7D%20else%20%7B%0A%20%20%20%20%20%20%20%20pins.digitalWritePin%28DigitalPin.P1%2C0%29%0Abasic.pause%28100%29%0A%0A%0A%20%20%20%20%7D%0A%20%20%20%20if%20%28%21input.buttonIsPressed%28Button.A%29%29%7B%0A%20%20%20%20%20%20%20%20basic.showString%28%22Ciao%20from%20Bari%22%29%0A%20%20%20%20%20%20%20%20basic.pause%28100%29%0A%20%20%20%20%20%7D%20else%20%7B%0A%20%20%20%20%20%20%20%20basic.clearScreen%28%29%0Abasic.pause%28100%29%0A%0A%0A%20%20%20%20%7D%0A%7D%29%0A%60%60%60%0A%0A"

cardWidth=100
pluscardwidht=100
missionCardWidth=120
vertiPaddingWidth=35

# st.markdown("""""")
applogo, empty1, empty2, mission, persona, empty3, thing, empty4,empty5  = st.beta_columns(9)

with applogo:
    st.image("http://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/applogo3.png",width=250)
with mission:
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/cards/EN-mission-7.png", width=missionCardWidth)
with persona:
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/cards/EN-persona-4.png", width=cardWidth)
with thing:
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/cards/EN-thing-art-9.png", width=cardWidth)

input_col, plus_col, output_col,  code_col, emptycol , emptycol2 , emptycol3, emptycol4,emptycol5,emptycol6 = st.beta_columns(10)


with input_col:    
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=vertiPaddingWidth)
    st.write("when...")
    # ("Input1:")
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/cards/EN-inputPhy-TemperatureHigh.png", width=cardWidth)
    # ("Input2:")
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/cards/EN-inputPhy-buttonNotpressed.png", width=cardWidth)
    # ("Input3:")
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/cards/noInput.png", width=cardWidth)

with plus_col:    
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=vertiPaddingWidth)
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/plus.png", width=pluscardwidht)
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/plus.png", width=pluscardwidht)
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/plus.png", width=pluscardwidht)    
with output_col:    
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=vertiPaddingWidth)
    st.write("then...")
    # ("Output1:")
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/cards/EN-outputPhy-TurnOnLight.png", width=cardWidth)
    # ("Output2:")
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/cards/EN-outputPhy-ShowText.png", width=cardWidth)
    # ("Output3:")
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/cards/noOutput.png", width=cardWidth)
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=vertiPaddingWidth)


with code_col:
    # st.header("My code is:")
    components.iframe(urlis,width=700, height=1500, scrolling=True)

with emptycol5:
    st.button("Refresh (r)")
with emptycol6:
    st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=32)
    st.markdown("[Edit/Download]("+urlis+")", unsafe_allow_html=True)
