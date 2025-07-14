import openai
import constants

# API CREDENTIALS
openai.api_key = constants.APIKEY
organization_id = constants.ORGANIZATION_ID







# IMPORTANT!
# ChatGPT doesnt remember conversations unless you fill the messages array in the api object accordingly


def interact_with_chatbot(prompt):
  response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
      messages=[
        {"role": "user", "content": prompt}   
      ],
    max_tokens=193,
    temperature=0,
) 
  return response





while True:
  user_input = input("> ")
  if user_input == "exit":
    break

  response = interact_with_chatbot(user_input)
  print("ChatGPT: ", response)
