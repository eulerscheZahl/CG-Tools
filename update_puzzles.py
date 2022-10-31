import requests
import json

cookie = '*redacted*'

with requests.Session() as s:
    for c in cookie.split(';'):
        p = c.split('=')
        s.cookies.set(p[0], p[1], domain='codingame.com')
    r = s.post('https://www.codingame.com/services/ContributionRemoteService/getAcceptedContributions', json=['ALL'])
    data = r.json()
    handles = [d['publicHandle'] for d in data]

    update_url = 'https://eulerschezahl.herokuapp.com/codingame/puzzles/update/'
    #update_url = 'http://127.0.0.1:8000/codingame/puzzles/update/'
    r = s.post(update_url, data={'handles':' '.join(handles)})
    print(r._content.decode())
