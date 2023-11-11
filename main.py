import streamlit as st
import requests
import random

def get_joke():
    genres = [
        "Christmas",
        # "Dark",
        "Misc",
        "Pun",
        "Spooky",
        # "Programming",
    ]

    genre = random.choice(genres)
    type = "twopart" # "single"
    link = f"https://v2.jokeapi.dev/joke/{genre}?lang=en&blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type={type}"

    joke = requests.get(link).json()
    part_1 = joke["setup"]
    part_2 = joke["delivery"]

    return part_1, part_2

def main():
    st.markdown("""
    # Akhila Joke Assistant
    Since you can't make any jokes yourself, use these to attempt being funny.
    """)
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

        st.session_state["jokes"] = get_joke()
    part_1, part_2 = st.session_state["jokes"]
    
    if "Delivery" not in st.session_state:
        st.session_state["Delivery"] = False
    if "Delivered" not in st.session_state:
        st.session_state["Delivered"] = False

    st.session_state["messages"] += [
        dict(
            role = "assistant",
            content = part_1
        )
    ]
    
    def add_others():
        st.session_state["messages"] += [
            dict(
                role = "user",
                content = "Go on."
            ),
            dict(
                role = "assistant",
                content = f"""
                {part_2}

                Hope you liked it. Here's another one.
                """
            )
        ]
        st.session_state["jokes"] = get_joke()
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])
    if st.session_state["Delivered"] is False:
        st.session_state["Delivery"] = st.button(
            "Go on.",
            on_click=add_others
        )

if __name__ == "__main__":
    main()