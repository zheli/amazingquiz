# -*- coding: utf-8

@auth.requires_membership('admins')
def index():
    response.title = 'Admin Panel'
    session.characters = db().select(db.characters.ALL, orderby=db.characters.answer)
    form = SQLFORM(db.characters)
    if form.accepts(request.vars, session):
        session.characters = db().select(db.characters.ALL, orderby=db.characters.answer)
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

def modifyRecord():
    response.title = 'Admin Panel'
    session.characters = db().select(db.characters.ALL, orderby=db.characters.answer)
    record = db.characters(request.args(0)) or redirect(URL('index'))
    form = SQLFORM(db.characters, record, deletable=True)
    if form.accepts(request.vars, session):
        session.characters = db().select(db.characters.ALL, orderby=db.characters.answer)
        response.flash = 'record updated!'
    elif form.errors:
        response.flash = 'errors!'
    return dict(form=form)

@auth.requires_login()
def setup():
    admin_group_ID = auth.add_group('admins', 'the root!')
    auth.add_membership(admin_group_ID)
    return True
