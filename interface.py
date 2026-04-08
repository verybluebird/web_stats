import streamlit as st


def color_survived(val):
    color = 'green' if val > 0.05 else 'red'
    return f'background-color: {color}'
def yes_callback():
    st.session_state.step = 2

def result(test_df):
    st.dataframe(
        test_df.style.map(lambda x: f"background-color: {'green' if x >= 0.05 else 'red'}", subset='p-value'),
        column_config={
            "_index": st.column_config.Column(width="medium"),
            "p-value": st.column_config.Column(width="small")
        },
        width='content'  # Set to True to stretch table to container width

    )


def click_button():
    bttn = 1
def line(width):
    if width == 5:
        st.markdown("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """,
                unsafe_allow_html=True)
    elif width == 10:
        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
                    unsafe_allow_html=True)
