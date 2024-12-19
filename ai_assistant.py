# -*- coding: utf-8 -*-
"""AI_Assistant.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14Ddy6JxMxpHJfbIuDc8d5a9PguCpvTRT
"""



## Libraries Required
!pip install langchain-huggingface
## For API Calls
!pip install huggingface_hub
!pip install transformers
!pip install accelerate
!pip install bitsandbytes
!pip install langchain

# # Environment secret keys
from google.colab import userdata
sec_key=userdata.get("HF_TOKEN")
print(sec_key)

#Using huggingface endpoints
from langchain_huggingface import HuggingFaceEndpoint
import os
os.environ['HF_TOKEN'] = sec_key

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(repo_id=repo_id, max_length = 128, temperature= 0.7, token = sec_key)

llm

llm.invoke("CSK vs RCB, which is better, answer in one word")

from langchain import PromptTemplate, LLMChain
question = "if brain rot was a person discribe them in a funny way"
template = """Question: {question}
Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)
print(llm_chain.invoke(question))

#huggingface Pipeline
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

"""model_id = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

"""

from langchain_huggingface import HuggingFaceEndpoint
import logging

# Initialize logging
logging.basicConfig(filename="queries.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def get_llm(repo_id, max_length=128, temperature=0.7):
    token = os.getenv("HF_TOKEN")
    return HuggingFaceEndpoint(repo_id=repo_id, max_length=max_length, temperature=temperature, token=token)

def ask_question(llm, question):
    logging.info(f"User Question: {question}")
    response = llm.invoke(question)
    logging.info(f"LLM Response: {response}")
    return response

def summarize_text(llm, text):
    prompt = f"Summarize the following text:\n\n{text}"
    logging.info(f"Summarization Request: {text}")
    response = llm.invoke(prompt)
    logging.info(f"Summarization Response: {response}")
    return response

def generate_text(llm, prompt):
    logging.info(f"Custom Prompt: {prompt}")
    response = llm.invoke(prompt)
    logging.info(f"Generated Text: {response}")
    return response

from langchain_huggingface import HuggingFaceEndpoint
import os
import logging

# Initialize logging
logging.basicConfig(filename="queries.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def get_llm(repo_id, max_length=128, temperature=0.7):
    token = os.getenv("HF_TOKEN")
    return HuggingFaceEndpoint(repo_id=repo_id, max_length=max_length, temperature=temperature, token=token)

def ask_question_conversational(llm, conversation_history, question):
    # Add user query to the conversation history
    conversation_history.append({"role": "user", "content": question})

    # Construct the context for the model
    context = "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in conversation_history])

    # Prompt the model to continue the conversation
    prompt = f"{context}\nAssistant:"
    response = llm.invoke(prompt)

    # Add assistant's response to the history
    conversation_history.append({"role": "assistant", "content": response})

    return response

def conversational_mode(llm):
    print("\nEntering Conversational Mode! Type 'exit' to end.\n")
    conversation_history = []  # Initialize conversation history

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Exiting Conversational Mode.")
            break

        response = ask_question_conversational(llm, conversation_history, user_input)
        print(f"Assistant: {response}")

def main():
    # Set up environment and model
    sec_key = userdata.get("HF_TOKEN")  # Add your token here
    os.environ["HF_TOKEN"] = sec_key
    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
    llm = get_llm(repo_id=repo_id)

    print("Welcome to the AI Assistant!")

    while True:
        print("\nOptions:")
        print("1. General Q&A")
        print("2. Summarization")
        print("3. Creative Text Generation")
        print("4. Conversational Mode")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            question = input("Enter your question: ")
            response = ask_question_conversational(llm, [], question)  # Direct question mode
            print(f"\nAI Response: {response}")

        elif choice == "2":
            text = input("Enter the text to summarize: ")
            summary = ask_question_conversational(llm, [], f"Summarize the following: {text}")  # Summarization mode
            print(f"\nSummary: {summary}")

        elif choice == "3":
            prompt = input("Enter your custom prompt: ")
            response = ask_question_conversational(llm, [], prompt)  # Custom text generation
            print(f"\nGenerated Text: {response}")

        elif choice == "4":
            conversational_mode(llm)  # Start conversational mode

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

main = main()