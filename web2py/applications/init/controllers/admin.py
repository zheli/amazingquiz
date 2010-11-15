# -*- coding: utf-8

#@auth.requires_login()
@auth.requires_membership('admins')
def index():
    session.characters = db().select(db.characters.ALL, orderby=db.characters.id)
    form = SQLFORM(db.characters)
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

@auth.requires_login()
def setup():
    admin_group_ID = auth.add_group('admins', 'the root!')
    auth.add_membership(admin_group_ID)
    return True
