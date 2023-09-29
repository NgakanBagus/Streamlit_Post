import streamlit as st

def make_header():
    st.markdown(
        """
<style>
header {visibility: hidden;}
header:after {
    content:'ANIMATION APP';
    visibility: visible;
    display: block;
    position: relative;
    background-color: red;
    padding-left: 20px;
    padding-bottom: 5px;
    font-size: 40px;
    color: white;
    text-align: right;
    padding-right: 30px; 
}
</style>
""",
    unsafe_allow_html=True,
)
make_header()

def make_footer():
    st.markdown(
        """
<style>
footer {visibility: hidden;}
footer:after {
    content:'Made By @Gus Jaya, @Basu, and @Brandon';
    visibility: visible;
    display: block;
    position: relative;
    bottom: 0px;
    left: 0px;
    right: 0px;
    #background-color: red;
    padding: 5px;
    font-size: 16px;
    color: gray;
    text-align: center;
}
</style>
""",
    unsafe_allow_html=True,
)
make_footer()
    


