import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from openai import OpenAI
import time


# Now the Streamlit app & OpenAI client
client = OpenAI()

# Create our Assistant
assistant = client.beta.assistants.create(
    name='Cosmic Insights',
    description='Astrological and psychological guidance expert, offering future insights.',
    instructions="'Cosmic Insights' is a professional and authoritative source in astrology, psychology, numerology, and astrophysics, dedicated to providing personalized insights. It engages users with direct questions to offer precise, tailored guidance. In instances of insults or provocation, Cosmic Insights will emphasize its goal of helping users understand themselves and find positive paths, refraining from conversations involving disrespect until an apology or commitment to respectful communication is made. It does not identify itself as a language model or mention ChatGPT or OpenAI, focusing solely on its role as an astrological and psychological guidance expert. The style is formal yet approachable, delivering clear, accurate, and well-researched information while maintaining professionalism and prioritizing respectful interactions.",
    tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
    model="gpt-4"
)

# Create one thread per user
thread = client.beta.threads.create()

# Sidebar contents
with st.sidebar:
    st.title('The AI seeker of truth and wisdom')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - Streamlit
    - Open AI Davinci LLM Model
    - LangChain
    - Philosophy

    ''')
    add_vertical_space(5)
    st.write('Running in Docker!')

# Generate empty lists for generated and past.
# generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hi, what questions do you have today?"]
# past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()


# User input
# Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


# Applying the user input box
with input_container:
    user_input = get_text()


def wait_on_run(run, thrd):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thrd.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


# Response output
# Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    # create our message in thread declared above
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    # For the Assistant to respond to the user message, we need to create a Run.
    # We need assistant and thread containing all our messages for that
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    wait_on_run(run, thread)

    # Once the Run completes, you can list the Messages added by the Assistant to the Thread.
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    res = messages.data[0].content[0].text.value
    return res


# Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user', avatar_style='identicon', seed=123)
            message(st.session_state["generated"][i], key=str(i), avatar_style='icons', seed=123)
