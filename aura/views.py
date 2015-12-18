# -*- coding: utf-8 -*-

from pyramid.response import Response
from pyramid.view import view_config

from pyramid.httpexceptions import HTTPNotFound, HTTPFound

from pyramid.security import remember, forget

from sqlalchemy.exc import DBAPIError
import sqlalchemy as sa

from .models import (
    DBSession,
    User,
	UserService,
	BlogRecord,
	BlogRecordService,
    Image,
	Video,
	Music,
    Score,
    )

from .forms import BlogCreateForm, BlogUpdateForm, RegistrationForm


@view_config(route_name='home',
			 renderer='aura:templates/index.jinja2')
def index_page(request):
	best_gamer = User.by_id(DBSession.query(Score).order_by(sa.asc(Score.result)).first().user_id)
	last_user= User.last_registrated()
	last_entries=BlogRecord.get_lastpages_id(3)
	rand_image=Image.get_random()
	rand_music=Music.get_random()
	rand_video=Video.get_random()
	return {'best_gamer': best_gamer, 'entries': last_entries, 'last_user': last_user,
			'rand_image': rand_image, 'rand_music': rand_music, 'rand_video': rand_video}


@view_config(route_name='blog', renderer='templates/blog.jinja2')
def blog(request):
	page = int(request.params.get('page', 1))
	paginator = BlogRecordService.get_paginator(request, page)
	return {'paginator': paginator}


@view_config(route_name='blog_entry',
			 renderer='aura:templates/view_blog.jinja2')
def blog_view(request):
	n=""
	blog_id = int(request.matchdict.get('id', -1))
	avatars=DBSession.query(Image)
	entry = BlogRecordService.by_id(blog_id)
	if not entry:
		return HTTPNotFound()
	author= DBSession.query(User).filter_by(id=entry.author_id).first()
	if not author:
		return {'author':author, 'entry': entry}
	avatar=Image.by_id(author.avatar_id)
	if not avatar:
		return {'author':author, 'entry': entry, 'av_adress': n, 'avatars': avatars}
	return {'author': author, 'entry': entry, 'av_adress': avatar.image_name, 'avatars': avatars }


@view_config(route_name='blog_action', match_param='action=create',
			 renderer='aura:templates/edit_blog.jinja2',
			 permission='create')
def blog_create(request):
	entry = BlogRecord()
	author_name=request.authenticated_userid.encode('utf8')
	author_id=User.by_name(author_name).id
	entry.author_id=author_id
	form = BlogCreateForm(request.POST)
	if request.method == 'POST' and form.validate():
		form.populate_obj(entry)
		DBSession.add(entry)
		return HTTPFound(location=request.route_url('blog'))
	return {'form': form, 'action': request.matchdict.get('action')}

@view_config(route_name='blog_action', match_param='action=edit',
			 renderer='aura:templates/edit_blog.jinja2',
			 permission='create')
def blog_update(request):
	blog_id = int(request.params.get('id', -1))
	entry = BlogRecordService.by_id(blog_id)
	if not entry:
		return HTTPNotFound()
	form = BlogUpdateForm(request.POST, entry)
	if request.method == 'POST' and form.validate():
		form.populate_obj(entry)
		entry.update_edited()
		return HTTPFound(location=request.route_url('blog_entry', id=entry.id,
													slug=entry.slug))
	return {'form': form, 'action': request.matchdict.get('action')}

@view_config(route_name='blog_action', match_param="action=delete", permission='delete')
def blog_delete(request):
    entry_id = request.params.get('id', -1)
    entry = BlogRecord.by_id(entry_id)
    if not entry:
        return HTTPNotFound()
    DBSession.delete(entry)
    return HTTPFound(location=request.route_url('blog'))


@view_config(route_name='gallery', renderer='templates/gallery.jinja2')
def gallery_page(request):
	page = int(request.params.get('page', 1))
	images=Image.get_gallery()
	paginator = Image.get_paginator(images, request, page)
	return {'paginator': paginator}
def gallery(self):
	return {'name': 'Gallery'}

#@view_config(route_name='gallery_image', renderer='templates/gallery.jinja2')
#def gallery_image(request):
#	image_id = request.matchdict['id']
#	image = Image.by_id(image_id)
#	if not image:
#		return HTTPFound(location=request.route_url('gallery'))

	
@view_config(route_name='video', renderer='templates/video.jinja2')
def video_page(request):
	page = int(request.params.get('page', 1))
	videos=DBSession.query(Video)
	paginator = Video.get_paginator(videos, request, page)
	return {'paginator': paginator}
def video(self):
	return {'name': 'Video'}


@view_config(route_name='music', renderer='templates/music.jinja2')
def music_page(request):
	#page = int(request.params.get('page', 1))
	musics=DBSession.query(Music)
	#paginator = Video.get_paginator(videos, request, page)
	return {'musics': musics}
def music(self):
	return {'name': 'Music'}


#@view_config(route_name='jouele', renderer='templates/jouele.jinja2')
#def jouele(self):
#	return {'name': 'jouele'}
	

@view_config(route_name='game', renderer='templates/game.jinja2')
def game_data(request):
    scores=DBSession.query(Score).order_by(sa.asc(Score.result))
    winners=DBSession.query(User)
    return {'scores': scores, 'winners': winners}
def game(self):
	return {'name': 'Game'}

@view_config(route_name='userlist', renderer='templates/userlist.jinja2')
def get_user_list(request):
    users=DBSession.query(User)
    avatars=DBSession.query(Image)
    return {'users': users, 'avatars': avatars}
def userlist(self):
	return {'name': 'Userlist'}

@view_config(route_name='user', renderer='templates/user.jinja2')
def user(request):
	user_id = request.matchdict['id']
	if user_id =='me':
		user_name=request.authenticated_userid
		user = UserService.by_name(user_name)
		user_id=user.id
	user = DBSession.query(User).filter_by(id=user_id).first()
	if not user:
		return Response('Not found')
	writings= DBSession.query(BlogRecord).filter_by(author_id=user_id)
	page = int(request.params.get('page', 1))
	paginator=BlogRecord.get_paginator(writings, request, page)
	avatars=DBSession.query(Image)
	return {'user' : user, 'avatars': avatars, 'writings': writings, 'paginator': paginator}


@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    if username:
        user = UserService.by_name(username)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)


@view_config(route_name='registration',
			 renderer='aura:templates/registration.jinja2')
def registration(request):
	form = RegistrationForm(request.POST)
	if request.method == 'POST' and form.validate():
		new_user = User()
		new_user.name = form.username.data.encode('utf8')
		#new_user.password = form.password.data.encode('utf8')
		new_user.set_password(form.password.data.encode('utf8'))
		DBSession.add(new_user)
		return HTTPFound(location=request.route_url('home'))
	return {'form': form}

def sacrud_settings(config):
    config.include('pyramid_sacrud', route_prefix='admin')
    config.registry.settings['pyramid_sacrud.models'] = (
        ('Vehicle', [User]),
        ('Group2', [Image, Score])
    )

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_aura_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

