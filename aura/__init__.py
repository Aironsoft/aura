# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from models import (
	DBSession,
	Base,
	User,
	BlogRecord,
	Image,
	Score,
)


def sacrud_settings(config):
    config.include('pyramid_sacrud', route_prefix='admin')
    config.registry.settings['pyramid_sacrud.models'] = (
        ('Vehicle', [User, Score]),
        ('Group2', [Image])
    )


def database_settings(config):
    from sqlalchemy import create_engine
    config.registry.settings['sqlalchemy.url'] = db_url =\
        "sqlite:///example.db"
    engine = create_engine(db_url)
    Base.metadata.bind = engine
    Base.metadata.create_all()


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authentication_policy = AuthTktAuthenticationPolicy('somesecret',
                                                        hashalg='sha512')
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy
                          )
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('blog', '/blog')
    config.add_route('blog_entry', '/blog/{id:\d+}')
    config.add_route('blog_action', '/blog/{action}',
                     factory='aura.security.BlogRecordFactory')
    config.add_route('gallery', '/gallery')
    #config.add_route('gallery_image', '/gallery/{id}')
    config.add_route('video', '/video')
    config.add_route('music', '/music')
    #config.add_route('jouele', '/jouele')
    config.add_route('game', '/game')
    config.add_route('userlist', '/userlist')
    config.add_route('user', '/user/{id}')
    config.add_route('auth', '/sign/{action}')
    config.add_route('registration', '/registration')
    config.include('pyramid_sacrud',route_prefix='admin')
    settings = config.registry.settings
    config.include(database_settings)
    config.include(sacrud_settings)
    settings['pyramid_sacrud.models'] = (('Project',[User,Image,Score]))
    config.scan()
    return config.make_wsgi_app()
