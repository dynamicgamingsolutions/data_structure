import os
import sys
import pymssql
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(dir_path, 'static'))
from flask import Blueprint, redirect, url_for, session, render_template

logOut_bp = Blueprint('logOut', __name__)

@logOut_bp.route('/logout')
def logout():
    session.pop('username', None)  # remove the username from the session
    return render_template('logOut.html')  # render the logout page