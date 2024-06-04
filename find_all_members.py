import requests
from hashlib import md5

base_url = "https://api.ok.ru/fb.do"
application_key = "CJCIHOLGDIHBABABA"
session_key = "-n-mIBKItthi31vjS12uH89NovAdCAsLdKoIu1YUE99zKWVxsLo4AUZnndWaU10OKQurlHYGfaHCkvkiEXFG"


def generate_sig(params, secret_key):
    sorted_params = ''.join([f'{key}={value}' for key, value in sorted(params.items())])
    for_sig = f'{sorted_params}{secret_key}'
    return md5(for_sig.encode('utf-8')).hexdigest().lower()


def get_members(uid):
    count = 0
    has_more = True
    anchor = None
    members_list = []

    while has_more:
        params = {
            'application_key': application_key,
            'count': "1000",
            'format': "json",
            'method': "group.getMembers",
            'session_key': session_key,
            'uid': uid,
            'direction': 'FORWARD'
        }

        if anchor:
            params['anchor'] = anchor

        sig = generate_sig(params, "your_secret_key")  # Убедитесь, что подставили ваш секретный ключ
        params['sig'] = sig

        response = requests.post(base_url, data=params)
        data = response.json()

        if 'members' in data:
            for member in data['members']:
                count += 1
                members_list.append(member)

        has_more = data.get('has_more', False)
        anchor = data.get('anchor', None)

        if not has_more:
            break

    return members_list
