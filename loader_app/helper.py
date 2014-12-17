__author__ = 'funkycoda'

from functools import wraps

from flask import request, abort, redirect, g

import requests

from loader_app import app


def mol_user_auth(*role):
    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            cookie_name = app.config.get('REMEMBER_COOKIE_NAME', 'muprsns')
            auth_base_url = app.config.get('MOL_AUTH_BASE_URL', 'http://auth.mol.org/')

            if cookie_name not in request.cookies:
                return redirect('%s/login?next=%s' % (auth_base_url, request.url))

            auth_token = request.cookies[cookie_name]
            payload = {'auth_token': auth_token}
            if role is not None:
                payload.update(role_check=role)

            r = requests.get('%s/api/me' % auth_base_url, params=payload)

            if r.status_code != 200:
                abort(403)
                return None

            user_details = r.json()

            if role is not None:
                if user_details.get('has_role', False) is False:
                    abort(401)
                    return False

            g.user = user_details

            return f(*args, **kwargs)
        return decorated_view
    return wrapper

