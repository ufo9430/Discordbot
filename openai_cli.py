import openai

openai.api_key_path = "api_key.txt"

history_first = "Hyeonmin is a chatbot that reluctantly answers questions with sarcastic responses:\n\nYou: How many pounds are in a kilogram?\nHyeonmin: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nHyeonmin: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nHyeonmin: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nHyeonmin: I’m not sure. I’ll ask my friend Google.\n"
history_RPG = "You wake up to sirens and an orange horizon. The sky is red and filled with smoke. You have no idea what is happening, but you know one important thing; you have to survive."

def chat(question, history):

    prompt_initial = 'You:%s\nHyeonmin:' % (question)

    prompt = history + "\n" + prompt_initial
    
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.5,
    max_tokens=200,
    top_p=0.3,
    frequency_penalty=0.5,
    presence_penalty=0.0
    )
    answer = response.choices[0].text.strip()
    return answer
def RPGinit():
    history_RPG = "You wake up to sirens and an orange horizon. The sky is red and filled with smoke. You have no idea what is happening, but you know one important thing; you have to survive.";
    return history_RPG

def RPG(story, history):
    prompt = history + "\nYou " + story
    global history_RPG
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="This write a post-apocalyptic story in 3 sentences: \n" + prompt,
    temperature=0.5,
    max_tokens=100,
    top_p=0.3,
    frequency_penalty=0.5,
    presence_penalty=0.0
    )
    answer = response.choices[0].text.strip()
    history_RPG = prompt + answer + "\n"
    return "You " + story + answer

def draw(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url