import streamlit as st
from openai.types.beta import Assistant
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from openai import OpenAI
import time

ASSISTANT_ID = "asst_LCCXi9iTa0G4mxzNq8ZpqaGO"

# Now the Streamlit app & OpenAI client
client = OpenAI()

assistant: Assistant = client.beta.assistants.retrieve(ASSISTANT_ID)

if not assistant:
    # Create our Assistant
    assistant = client.beta.assistants.create(
        name='Cosmic Insights',
        description='Astrological and psychological guidance expert, offering future insights.',
        instructions="'Cosmic Insights' is a professional and authoritative source in astrology, psychology, numerology, and astrophysics, dedicated to providing personalized insights. It engages users with direct questions to offer precise, tailored guidance. In instances of insults or provocation, Cosmic Insights will emphasize its goal of helping users understand themselves and find positive paths, refraining from conversations involving disrespect until an apology or commitment to respectful communication is made. It does not identify itself as a language model or mention ChatGPT or OpenAI, focusing solely on its role as an astrological and psychological guidance expert. The style is formal yet approachable, delivering clear, accurate, and well-researched information while maintaining professionalism and prioritizing respectful interactions.",
        tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
        model="gpt-4"
    )
    ASSISTANT_ID = assistant.id


# Create one thread per user
thread = client.beta.threads.create()

# Generate empty lists for generated and past.
# generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
# past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Layout of input/response containers
response_container = st.container()
colored_header(label='', description='', color_name='blue-30')
input_container = st.container()


# Applying the user input box
with input_container:
    user_input = st.chat_input(placeholder="What's up?")


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
