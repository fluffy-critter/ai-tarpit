""" main implementation of the thing """

import random
import user_agents

with open('/usr/share/dict/words', 'r') as wordlist:
    WORDS = wordlist.read().split()

def make_title():
    return ' '.join(word.title() for word in random.sample(WORDS, k=random.randrange(2, 7)))

def make_page():

    title = make_title()

    parts = [f'<html><head><title>{title}</title></head><body>\n<h1>{title}</h1>\n']

    for _ in range(random.randrange(1,15)):
        make_section(parts)

    parts.append('</body></html>')
    return '\n'.join(parts)

def make_section(parts):
    """ Build a page section full of nonsense """

    parts.append(f'<h2>{" ".join(random.sample(WORDS, k=random.randrange(1,10)))}</h2>\n')

    for _ in range(random.randrange(1,6)):
        make_paragraph(parts)

def make_paragraph(parts):
    parts.append('<p>')

    sentences = []
    for _ in range(random.randrange(1,7)):
        make_sentence(sentences)
    parts.append(' '.join(sentences))

    parts.append('</p>\n')

def make_sentence(parts):
    phrases = [make_phrase(True)]
    for _ in range(random.randrange(0,3)):
        phrases.append(make_phrase(False))

    parts.append(f'{", ".join(phrases)}.')

def linkify(words):
    end = random.randrange(0, len(words))
    start = random.randrange(0, end + 1)
    words[end] += '</a>'
    href = '/'.join(random.sample(WORDS, k=random.randrange(1,4)))
    words[start] = f'<a href="/{href}">{words[start]}'

def make_phrase(capitalize):
    words = random.sample(WORDS, k=random.randrange(1,11))
    if capitalize:
        words[0] = words[0].title()

    if random.random() < 0.25:
        linkify(words)

    return ' '.join(words)

async def app(scope, receive, send):
    """ ASGI app """
    if scope["type"] != "http":
        raise Exception("Only the HTTP protocol is supported")

    is_bot = False
    if 'headers' in scope:
        for k,v in scope['headers']:
            if k.decode('iso-8859-1').casefold() == 'user-agent'.casefold():
                if user_agents.parse(v.decode('iso-8859-1')).is_bot:
                    is_bot = True

    if scope['path'] == '/robots.txt':
        content_type = b'text/plain'
        body = b'User-Agent: *\nDisallow: /\n'
    elif is_bot:
        content_type = b'text/html'
        body = '<html><head><title>Nothing to see here</title></head><body><p>Hello</p></body></html>'.encode('iso-8859-1')
    else:
        content_type = b'text/html'
        body = make_page().encode('iso-8859-1')

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', content_type),
            (b'content-length', str(len(body)).encode('iso-8859-1')),
        ],
    })

    await send({
        'type': 'http.response.body',
        'body': body,
    })