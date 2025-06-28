import streamlit as st

def page_main():
    st.title("TrustSurgy")
    st.write("Welcome to the main page.")
    
    # Display the image (adjust the path to your image)
    st.image("assets/images/main.png", use_container_width=True)
    
    # Add a button
    if st.button("시작하기"):
        # You can set a session state or perform an action here
        st.success("시작하기 버튼이 눌렸습니다!")
        return True
    return False
