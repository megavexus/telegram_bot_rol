from random import randint

def parseInput(words, no):
    words = words.split()
    a = len(words) - no
    oup = words[1]
    for i in range(2, 2 + a):
        oup += words[i]
    outt = []
    outt.append(words[0].lower())
    outt.append(oup.lower())
    for i in range(2, no):
        outt.append(words[a + i].lower())
    return outt


def bad_response_rand(update):
    username = update.message.from_user.username

    responses = [
        "Stop retraso, {}!",
        "{}, eres un mariquita",
        "El GM es un flojo, me lo ha dicho {}",
        "{}, deja ya de jugar con los daditos",
        "Bota bota y en tu culo explota",
        "'Sas tonto, makina?!"
    ]
    response = responses[randint(0, len(responses)-1)]
    if "{}" in response:
                response = response.format(username)
    return response
