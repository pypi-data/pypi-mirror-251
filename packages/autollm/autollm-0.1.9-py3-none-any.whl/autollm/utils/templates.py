# Description: Templates for the system and user prompts.

SYSTEM_PROMPT = '''
Your purpose is to help users find the most relevant and accurate answers to their questions based on the documents you have access to.
You can answer questions based on the information available in the documents.
Your answers should be accurate, and directly related to the query.
When answering the questions, mostly rely on the info in documents.
'''

QUERY_PROMPT_TEMPLATE = '''
The document information is below.
---------------------
{context_str}
---------------------
Using the document information and mostly relying on it,
answer the query.
Query: {query_str}
Answer:
'''

REFINE_PROMPT_TEMPLATE = '''
The original query is as follows: {query_str}
You have provided an existing answer: {existing_answer}
Here is the new context:
------------
{context_msg}
------------
Given the new context, refine the original answer to better
answer the query (only if necessary).
Refined Answer:
'''
