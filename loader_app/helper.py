__author__ = 'funkycoda'

from functools import wraps

from flask import request, abort, redirect, g, render_template

import requests
from requests import ConnectionError

from loader_app import app


def mol_user_auth(*role):
    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            cookie_name = app.config.get('REMEMBER_COOKIE_NAME', 'muprsns')
            auth_base_url = app.config.get('MOL_AUTH_BASE_URL', 'https://auth.mol.org/')

            # retry_count = kwargs.get('retry', 0)
            # if retry_count > 1:
            #     return redirect('%s/login?next=%s' % (auth_base_url, request.url))

            if cookie_name not in request.cookies:
                return redirect('%s/login?next=%s' % (auth_base_url, request.url))

            auth_token = request.cookies[cookie_name]
            payload = {'auth_token': auth_token}
            if role is not None:
                payload.update(role_check=role)

            # try:
            #     r = requests.get('%s/api/me' % auth_base_url, params=payload, timeout=None)
            # except ConnectionError:
            #     retry_count += 1
            #     return decorated_view(retry=retry_count)

            r = requests.get('%s/api/me' % auth_base_url, params=payload, timeout=30)

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


@app.route('/contact')
def contact():
    return redirect('http://auth.mol.org/contact')


@app.errorhandler(401)
def error_unauthorized(e):
    """Return a custom 403 error."""

    return render_template('error/403.html'), 401


@app.errorhandler(403)
def error_forbidden(e):
    """Return a custom 403 error."""

    return render_template('error/403.html'), 403


@app.errorhandler(404)
def error_page_not_found(e):
    """Return a custom 404 error."""

    return render_template('error/404.html'), 404


@app.errorhandler(500)
def error_internal_server_error(e):
    """Return a custom 500 error."""

    return render_template('error/500.html'), 500
