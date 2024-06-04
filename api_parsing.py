import requests
from hashlib import md5

base_url = "https://api.ok.ru/fb.do"

for_sig = ("application_key=CJCIHOLGDIHBABABAcount=1000format=jsonmethod=group.getMemberssession_"
           "key=-n-mIBKItthi31vjS12uH89NovAdCAsLdKoIu1YUE99zKWVxsLo4AUZnndWaU10OKQurlHYGfaHCkvkiE"
           "XFGuid=517623279126561023694a5c62ea458db3b86f50469508")

sig = md5(for_sig.encode('utf-8')).hexdigest().lower()

def group_id(url):
    params = {
        'application_key': "CJCIHOLGDIHBABABA",
        'count': "10",
        'format': "json",
        'method': "url.getInfo",
        'session_key': "-n-mIBKItthi31vjS12uH89NovAdCAsLdKoIu1YUE99zKWVxsLo4AUZnndWaU10OKQurlHYGfaHCkvkiEXFG",
        'sig': sig,
        'url': url
    }
    r = requests.post(base_url, data=params)
    data = r.json()
    group_id = data['objectId']
    return group_id


def count_members(group_id):
    params = {
        'application_key': "CJCIHOLGDIHBABABA",
        'count': "10",
        'format': "json",
        'method': "group.getCounters",
        'session_key': "-n-mIBKItthi31vjS12uH89NovAdCAsLdKoIu1YUE99zKWVxsLo4AUZnndWaU10OKQurlHYGfaHCkvkiEXFG",
        'sig': sig,
        'group_id': group_id,
        'counterTypes': ['MEMBERS']
    }
    r = requests.post(base_url, data=params)
    data = r.json()
    try:
        count = data['counters']['members']
        return count
    except KeyError:
        return None


def name_group(group_id):
    params = {
        'application_key': "CJCIHOLGDIHBABABA",
        'count': "10",
        'format': "json",
        'method': "group.getInfo",
        'session_key': "-n-mIBKItthi31vjS12uH89NovAdCAsLdKoIu1YUE99zKWVxsLo4AUZnndWaU10OKQurlHYGfaHCkvkiEXFG",
        'sig': sig,
        'uids': group_id,
        'fields': ['name']
    }
    r = requests.post(base_url, data=params)
    data = r.json()
    return data[0]['name']


def users_from_group(group_id):
    params = {
        'application_key': "CJCIHOLGDIHBABABA",
        'count': "10",
        'format': "json",
        'method': "group.getMembers",
        'session_key': "-n-mIBKItthi31vjS12uH89NovAdCAsLdKoIu1YUE99zKWVxsLo4AUZnndWaU10OKQurlHYGfaHCkvkiEXFG",
        'sig': sig,
        'uid': group_id
    }
    r = requests.post(base_url, data=params)
    data = r.json()
    try:
        return data['members']
    except KeyError:
        return 0


def members_facts(member_id):
    params = {
        'application_key': "CJCIHOLGDIHBABABA",
        'count': "10",
        'format': "json",
        'method': "users.getInfo",
        'session_key': "-n-mIBKItthi31vjS12uH89NovAdCAsLdKoIu1YUE99zKWVxsLo4AUZnndWaU10OKQurlHYGfaHCkvkiEXFG",
        'sig': sig,
        'uids': member_id,
        'fields': 'AGE, GENDER, last_online, location'
    }
    r = requests.post(base_url, data=params)
    data = r.json()
    try:
        return data
    except:
        return 0
