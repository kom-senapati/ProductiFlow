import random

import pandas as pd
import requests
import streamlit as st
from PIL import Image
from tasks import *


def greet():
    greetings = [
        "Hi there! 👋✨",
        "Hello! 🌞😊",
        "Hey! 🌈👋",
        "Greetings! 🎉😄",
        "Howdy! 🤠👋",
        "Yo! 👋🌟",
        "Hiya! 🌺😊",
        "Hey there! 🚀👋",
        "Aloha! 🌴🤙",
        "What's up! 🌟😃",
    ]
    greeting = random.choice(greetings)
    return greeting


def get_random_quote():
    quote_api_url = "https://zenquotes.io/api/random"

    try:
        response = requests.get(quote_api_url)
        if response.status_code == 200:
            quote_data = response.json()
            quote_text = quote_data[0]["q"]
            quote_author = quote_data[0]["a"]
            quote = f'"{quote_text}" - {quote_author}'
            return quote
    except Exception as e:
        st.warning(f"Failed to fetch a quote from the API. Error: {str(e)}")

    # Fallback quotes in case the API fails
    fallback_quotes = [
        "The only way to do great work is to love what you do. -Steve Jobs",
        "Believe you can and you're halfway there. -Theodore Roosevelt",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. -Winston Churchill",
        "In the middle of difficulty lies opportunity. -Albert Einstein",
        "Don't watch the clock; do what it does. Keep going. -Sam Levenson",
    ]

    quote = random.choice(fallback_quotes)
    return quote


def get_random_joke():
    joke_api_url = "https://v2.jokeapi.dev/joke/Programming,Spooky?blacklistFlags=political,racist,sexist&format=txt"

    try:
        response = requests.get(joke_api_url)
        if response.status_code == 200:
            joke = response.text
            return joke
    except Exception as e:
        st.warning(f"Failed to fetch a joke from the API. Error: {str(e)}")

    # Fallback jokes in case the API fails
    fallback_jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "How many programmers does it take to change a light bulb? None, that's a hardware issue!",
        "Why was the JavaScript developer sad? Because he didn't 'null' how to be happy!",
        "Why did the computer go to therapy? It had too many bytes of emotional baggage!",
        "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25!",
    ]

    joke = random.choice(fallback_jokes)
    return joke


def tasks():
    def color_df(val):
        if val == "Done":
            color = "green"
        elif val == "Doing":
            color = "orange"
        else:
            color = "red"

        return f"background-color: {color}"

    st.subheader("Tasks Page")
    image = Image.open("images/todo.jpeg")
    st.image(image, use_column_width=True)

    choice = st.sidebar.selectbox(
        "Menu",
        ["Create Task ✅", "Update Task 👨‍💻", "Delete Task ❌", "View Tasks' Status 👨‍💻"],
    )

    create_table()

    if choice == "Create Task ✅":
        st.subheader("Add Item")
        col1, col2 = st.columns(2)

        with col1:
            task = st.text_area("Task To Do")

        with col2:
            task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
            task_due_date = st.date_input("Due Date")

        if st.button("Add Task"):
            add_data(task, task_status, task_due_date)
            st.success('Added Task "{}" ✅'.format(task))
            st.balloons()

    elif choice == "Update Task 👨‍💻":
        st.subheader("Edit Items")
        with st.expander("Current Data"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df.style.applymap(color_df, subset=["Status"]))

        list_of_tasks = [i[0] for i in view_all_task_names()]
        selected_task = st.selectbox("Task", list_of_tasks)
        task_result = get_task(selected_task)

        if task_result:
            task = task_result[0][0]
            task_status = task_result[0][1]
            task_due_date = task_result[0][2]

            col1, col2 = st.columns(2)

            with col1:
                new_task = st.text_area("Task To Do", task)

            with col2:
                new_task_status = st.selectbox(task_status, ["To Do", "Doing", "Done"])
                new_task_due_date = st.date_input(task_due_date)

            if st.button("Update Task 👨‍💻"):
                edit_task_data(
                    new_task,
                    new_task_status,
                    new_task_due_date,
                    task,
                    task_status,
                    task_due_date,
                )
                st.success('Updated Task "{}" ✅'.format(task, new_task))

            with st.expander("View Updated Data 💫"):
                result = view_all_data()
                clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
                st.dataframe(clean_df.style.applymap(color_df, subset=["Status"]))

    elif choice == "Delete Task ❌":
        st.subheader("Delete")
        with st.expander("View Data"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df.style.applymap(color_df, subset=["Status"]))

        unique_list = [i[0] for i in view_all_task_names()]
        delete_by_task_name = st.selectbox("Select Task", unique_list)
        if st.button("Delete ❌"):
            delete_data(delete_by_task_name)
            st.warning('Deleted Task "{}" ✅'.format(delete_by_task_name))

        with st.expander("View Updated Data 💫"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df.style.applymap(color_df, subset=["Status"]))

    else:
        with st.expander("View All 📝"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df.style.applymap(color_df, subset=["Status"]))

        with st.expander("Task Status 📝"):
            task_df = clean_df["Status"].value_counts().to_frame()
            task_df = task_df.reset_index()
            st.dataframe(task_df)


def home():
    greeting = greet()
    joke = get_random_joke()
    quote = get_random_quote()

    st.title("Welcome to ProductiFlow!")
    image = Image.open("images/home.jpg")
    st.image(image, use_column_width=True)

    st.header(greeting)

    if st.button("Motivate me"):
        st.subheader("Motivational Quote")
        st.write(quote)

    if st.button("Make me laugh"):
        st.subheader("Joke of the Day")
        st.write(joke)


def main():
    st.set_page_config(
        page_title="ProductiFlow",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    page = st.sidebar.selectbox("Select a page", ["Home", "Tasks"])

    if page == "Home":
        home()
    elif page == "Tasks":
        tasks()


if __name__ == "__main__":
    main()
