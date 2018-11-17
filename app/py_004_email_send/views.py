from flask import render_template, Blueprint, flash, redirect
import py_004_email_send_lib
from app.lib_master_python import ds_recipe_lib
from app.lib_master_python import ds_authentication

bp_004 = Blueprint('py_004_email_send', __name__)

@bp_004.route('/')  # Sends the envelope and shows the result
def index():
    r = py_004_email_send_lib.send()
    redirect_url = ds_authentication.reauthenticate_check(r, ds_recipe_lib.get_base_url())
    if redirect_url:
        return redirect(redirect_url)
    if r["err"]:
        flash(r["err"])
        return redirect(ds_recipe_lib.get_base_url(2))
    else:
        return render_template('generic_sent.html', title='Send email--Python', data=r, base_url=ds_recipe_lib.get_base_url(2))
        # base_url is the home page in the nav bar

