import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

st.set_page_config(page_title="slwGPT", page_icon=":robot:")
st.header("slwGPT")
col1, col2, col3 = st.columns([3,1,1])

template = """
    Below is a {content_type} draft that may be poorly structured, poorly worded, and lacking examples and details.
    Your goal is to:
    - Organize the writing to have a clear introduction/hook for the intended reader of {audience}.
    - Add examples and details to each section
    - Revise the writing for clarity, emulating the style of {style}
    - Give {versions} versions 
DRAFT: {draft}
    YOUR {length} {content_type} RESPONSE:
"""
with col3:
    # Models for /v1/chat/completions - https://platform.openai.com/docs/models/model-endpoint-compatibility
    user_model = st.selectbox('model', ("gpt-4", "gpt-4-0314", "gpt-4-32k", "gpt-4-32k-0314", "gpt-3.5-turbo", "gpt-3.5-turbo-0301"), 4)
    user_max_tokens = st.slider('tokens', 42, 4000, 333, 100)
    # between 0 and 2
    user_temperature = st.slider('temperature', 0.0, 2.0, 0.2)
    # 0 and 1, either alter this or temperature, not both
    user_top_p = st.slider('top_p', 0.0, 1.0, 1.0)
    # how many completions to generate
    user_n= st.slider('completions', 1, 10, 1)
    # user defined string
    user_stop = "xxstop"
    # between -2 and 2 to penalize tokens for having appeared already
    user_presence_penalty= st.slider('presence penalty', -2.0, 2.0, 0.0)
    # -2 and 2; penalty for frequency
    user_frequency_penalty=st.slider('frequency penalty', -2.0, 2.0, 0.0)
 #   user_user= "default user"
#    st.write("user: ", user_user)
#    st.write("stop command: ", user_stop)
    def get_api_key():
        input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
        return input_text
    openai_api_key = get_api_key()
    
prompt = PromptTemplate(
    input_variables=["draft", "content_type", "length", "audience", "style", "versions"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=user_temperature, max_tokens=user_max_tokens, top_p=user_top_p, n=user_n,  presence_penalty=user_presence_penalty, frequency_penalty=user_frequency_penalty,  openai_api_key=openai_api_key)
    return llm
## --- TODO allow selecting gptmodel (need to set different endpoint to do this(ie v1/chat/completions rather than v1/completions))

with col1:
    st.markdown("### Input")
    def get_text():
        input_text = st.text_area(label="Input", label_visibility='collapsed', placeholder="In a hole in the ground...", key="draft_input")
        return input_text

    draft_input = get_text()

    if len(draft_input.split(" ")) > 2800:
        st.write("The maximum length is 2800 words.")
        st.stop()
    
with col2:
    st.markdown("### Instructions")
    option_content_type = st.selectbox(
        'content type',
        ('blog', 'tweet'))
    option_length=st.text_input("how long would you like it?", "1 pg")
    option_style=st.text_input("what style?", "openzeppelin, gitlab")
    option_audience=st.text_input("who is your audience?", "web3 developers")
    option_versions=st.slider('versions', 1, 20, 1)
with col1:
    st.markdown("### Output")

if draft_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_draft = prompt.format(length=option_length, content_type=option_content_type, draft=draft_input, audience=option_audience, style=option_style, versions=option_versions)

    generated_content = llm(prompt_with_draft)

    with col1:
        st.write(generated_content)
