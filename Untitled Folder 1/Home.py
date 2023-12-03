import streamlit as st
from streamlit.logger import get_logger
import json
from streamlit_lottie import st_lottie


LOGGER = get_logger(__name__)

def load_lottiefile(animation1_json: str):
    with open("animation1.json", "r") as f:
        return json.load(f)



def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.markdown(
        """
        # Welcome to Sentify! 👋
        
        """
    )
    st.markdown(
        """
        Here we analyze your reviews for you!
        
        """
    )
    animation_container = st.container()  # Adjust height as needed

    with animation_container:
        # Load and display the Lottie animation
        lottie_animation1 = load_lottiefile("animation1.json")
        st_lottie(
            lottie_animation1,
            #renderer="json",
            speed=1,
            reverse=False,
            loop=True,
            quality="low",  # medium ; high
            height=None,
            width=None,
            key=None,
        )

    


if __name__ == "__main__":
    run()
