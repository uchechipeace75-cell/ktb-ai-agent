import streamlit as st
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from groq import Groq
load_dotenv()
TAVILY_API_KEY = st.secrets.get('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') or os.getenv('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')
GROQ_API_KEY = st.secrets.get('GROQ_API_KEY') or os.getenv('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)
st.set_page_config(page_title='Klugekopf TechBridge AI Agent', page_icon='🤖')
st.title('🤖 Klugekopf TechBridge AI Agent')
st.subheader('Researcher | Content Creator | SEO Optimizer')
topic = st.text_input('Enter a topic to research and write about:')
if st.button('Generate Content'):
    if topic:
        with st.spinner('Agents are working...'):
            tavily = TavilyClient(api_key=TAVILY_API_KEY)
            research = tavily.search(query=topic, search_depth='advanced')
            research_text = '\n'.join([r['content'] for r in research['results']])
            prompt = f"""
            You are a team of 3 AI agents:
            1. Researcher - You have found this information: {"{research_text}"}
            2. Content Creator - Write a detailed blog post about: {"{topic}"}
            3. SEO Optimizer - Optimize the blog post with keywords, meta description and SEO tips
            Please provide:
            - A full blog post
            - Meta description
            - Recommended keywords
            - SEO tips
            """ 
            response = client.chat.completions.create(
                model='llama-3.3-70b-versatile',
                messages=[{'role': 'user', 'content': prompt}])
            st.success('Done!')
            st.markdown('### Generated Content')
            st.write(response.choices[0].message.content)
else:
            st.warning('Please enter a topic first!')
