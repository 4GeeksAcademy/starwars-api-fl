import os
from flask_admin import Admin
from models import db, User, Favorites, Character, Planets, Starships
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')
    
    
    class FavoritesView(ModelView):
        column_list = ('user_id', 'character_id', 'planets_id','startships_id')
        form_columns = ('user_id', 'character_id', 'planets_id','startships_id')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(FavoritesView(Favorites, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(Starships, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))