import flask
import flask_login


from .. import forms
from ...constants import messages
from ...models import db


__all__ = (
    "change_password",
    "delete_account",
    "settings",
)


@flask_login.login_required
def change_password():
    form = forms.ChangePasswordForm()
    if form.validate_on_submit():
        password1 = form.password1.data
        password2 = form.password2.data
        if password1 == password2:
            user = flask_login.current_user
            user.password_hash = flask.g.bcrypt.generate_password_hash(password1).decode("utf-8")
            db.session.add(user)
            db.session.commit()
            flask.flash(messages.PASSWORD_UPDATE_SUCCESS, category="success")
        else:
            flask.flash(messages.PASSWORD_UPDATE_MATCH_ERROR, category="error")
    return flask.redirect(flask.url_for(".settings"))


@flask_login.login_required
def delete_account():
    """
    This view could get deleted in the future in favor of marking the user as pending
    for deletion instead of deleting them right away. This would be necessary if there
    were many objects related the user object that also required deletion which could
    cause the client's request to timeout while each object was deleted.
    """
    form = forms.DeleteAccountForm()
    if form.validate_on_submit():
        # Setting this attribute for the future where a deletion queue exists and a job
        # that checks for all user accounts marked for deletion runs periodically.
        flask_login.current_user.deleted = True

        db.session.delete(flask_login.current_user)
        db.session.commit()
        flask_login.logout_user()
        flask.flash(messages.DELETE_ACCOUNT_SUCCESS, category="success")
    return flask.redirect(flask.url_for(".login"))


@flask_login.login_required
def settings():
    return flask.render_template(
        "settings.html",
        change_password_form=forms.ChangePasswordForm(),
        delete_account_form=forms.DeleteAccountForm(),
        email_form=forms.EmailForm(),
        logout_form=forms.LogoutForm(),
    )