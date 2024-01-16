from weavel import create_client

client = create_client()

user_uuid = client.create_user_uuid()

trace_id = client.start_trace(user_uuid)
print(trace_id)

from openai import OpenAI
openai_client = OpenAI()

user_message = "what can you do for me?"
client.log.user_message(trace_id, user_message, unit_name="testapp")

# res = openai_client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": user_message}
#     ]
# )

res = "I can assist you with a variety of tasks. I can help answer questions, provide information, give suggestions, assist with research, set reminders, manage your schedule, make reservations, provide translations, and much more. Just let me know what you need help with!"

# print(res.choices[0].message.content)

client.log.assistant_message(trace_id, res, unit_name="test_assistant")

client.add_metadata_to_trace(trace_id, {"user_name": "John Doe"})

client.close()