""" main implementation of the thing """

import random
import user_agents
import string

with open('/usr/share/dict/words', 'r', encoding='iso-8859-1') as wordlist:
    WORDS = wordlist.read().split()


def make_title():
    """ Generate a page title """
    return string.capwords(' '.join(random.sample(WORDS, k=random.randrange(2, 7))))


def make_page():
    """ Make a page full of useful essays """
    title = make_title()

    parts = [f'<html><head><title>{title}</title></head><body>\n<h1>{title}</h1>\n',
             '<nav><a href="/">Back to main page</a><nav>', '<article>']

    for _ in range(random.randrange(3, 15)):
        make_section(parts, 2)

    parts.append('</article></body></html>')
    return '\n'.join(parts)


def make_section(parts, depth):
    """ Build a page section full of nonsense """

    words = random.sample(WORDS, k=random.randrange(1, 10))
    words[0] = string.capwords(words[0])

    if depth == 2:
        parts.append('<section>')

    parts.append(f'<h{depth}>{" ".join(words)}</h{depth}>\n')

    for _ in range(random.randrange(1, 3)):
        make_paragraph(parts)

    if depth < 5 and random.random() < 0.5**depth:
        for _ in range(random.randrange(0, 3)):
            make_section(parts, depth + 1)

    if depth == 2:
        parts.append('</section>')


def make_paragraph(parts):
    """ Let's make some discourse """
    parts.append('<p>')

    sentences = []
    for _ in range(random.randrange(1, 7)):
        make_sentence(sentences)
    parts.append(' '.join(sentences))

    parts.append('</p>\n')


def make_sentence(parts):
    """ More lucid than a typical Twitter user """
    phrases = [make_phrase(True)]
    for _ in range(random.randrange(0, 3)):
        phrases.append(make_phrase(False))

    parts.append(f'{", ".join(phrases)}.')


def linkify(words):
    """ Randomly add a link to a phrase """
    end = random.randrange(0, len(words))
    start = random.randrange(0, end + 1)
    words[end] += '</a>'
    href = '/'.join(random.sample(WORDS, k=random.randrange(1, 4)))
    words[start] = f'<a href="/{href}">{words[start]}'


def make_phrase(capitalize):
    """ Make a phrase to add to a sentence """
    words = random.sample(WORDS, k=random.randrange(1, 11))
    if capitalize:
        words[0] = string.capwords(words[0])

    if random.random() < 0.25:
        linkify(words)

    return ' '.join(words)


async def app(scope, _, send):
    """ ASGI app """
    is_bot = False
    if 'headers' in scope:
        for k, v in scope['headers']:
            if k.decode('iso-8859-1').casefold() == 'user-agent'.casefold():
                if user_agents.parse(v.decode('iso-8859-1')).is_bot:
                    is_bot = True

    if scope['path'] == '/robots.txt':
        content_type = b'text/plain'
        body = b'User-Agent: *\nDisallow: /\n'
    elif is_bot:
        content_type = b'text/html; charset=utf-8'
        body = '''<html><head><title>Nothing to see here</title></head>
        <body><p>Hello</p></body></html>'''.encode('utf-8')
    else:
        content_type = b'text/html; charset=utf-8'
        body = make_page().encode('iso-8859-1')

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', content_type),
            (b'content-length', str(len(body)).encode('utf-8')),
            (b'x-robots-tag', 'none'.encode('utf-8')),
        ],
    })

    await send({
        'type': 'http.response.body',
        'body': body,
    })
