from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from sqlalchemy.orm import validates

from config import db, bcrypt



class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-recipes', '-_password_hash', '-saved_recipes',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)

    recipes = db.relationship('Recipe', backref='user')
    saved_recipes = db.relationship('SavedRecipe', backref='user')
    
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username cannot be blank.")
        user = db.session.query(User).filter_by(username = username).first()
        if user is not None:
            raise ValueError("Username is taken.")
        return username

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username}>'

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String)
    image_url = db.Column(db.String)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    
    recipe_ingredients = db.relationship('RecipeIngredient', backref='recipe')
    
    recipe_categories = db.relationship('RecipeCategory', backref='recipe')
    
    # categories = db.relationship('Category', secondary=recipe_category_association, backref='recipe_categories', overlaps="recipe_categories")
    # reviews = db.relationship('Review', backref='reviews')
    
    
    serialize_rules = (
        '-user_id',
        
        # the recipe ingredients attr gave me some recursion issues
        '-recipe_ingredients.recipe',

        '-recipe_categories.recipe',
        # '-recipe_ingredients',
        
        '-saved_recipes',
        
        )

    def __repr__(self):
        return f'<Recipe {self.id}: {self.title}>'
    
class Ingredient(db.Model, SerializerMixin):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    
    serialize_rules = ('-recipe_ingredients',)
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'
    
class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    # recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    
    # recipes = db.relationship('Recipe', secondary=recipe_category_association, backref='recipe_categories', overlaps="recipe_categories")
    
    serialize_rules = ('-recipes',)
    
    def __repr__(self):
        return f'<Category {self.id}>'
    
#### JOINS TABLES ####

class SavedRecipe(db.Model, SerializerMixin):
    __tablename__ = 'saved_recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    recipe = db.relationship('Recipe', backref='saved_recipes')
    
    serialize_rules = ('-user_id','-recipe.saved_recipes',)
    
    def __repr__(self):
        return f'<SavedRecipe {self.id}>'
    
class RecipeIngredient(db.Model, SerializerMixin):
    __tablename__ = 'recipe_ingredients'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String)
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    
    ingredient = db.relationship("Ingredient", backref="recipe_ingredients")
    
    serialize_rules = ('-recipe', '-recipe_id', '-ingredient_id',)
        
    def __repr__(self):
        return f'<RecipeIngredient {self.id}>'
    
class RecipeCategory(db.Model, SerializerMixin):
    __tablename__ = 'recipe_category'
    
    id = db.Column(db.Integer, primary_key=True)
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    # recipe = db.relationship('Recipe', backref='recipe_categories')
    
    category = db.relationship('Category', backref='recipe_categories',)

    serialize_rules = ('-recipe', '-recipe_id', '-category_id', '-category.recipe_categories')

    
    def __repr__(self):
        return f'<RecipeCategory {self.id}>'

#### IDEAS ####

# class Like(db.Model, SerializerMixin):
#     __tablename__ = 'likes'
    
#     recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    
#     serialize_rules = ('-recipe', '-recipe_id', '-user_id',)
    
#     def __repr__(self):
#         return f'<Like {self.id}>'
    
    
    
    
    

# class Review(db.Model, SerializerMixin):
#     __tablename__ = 'reviews'
    
#     recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    
#     content = db.Column(db.String)
#     rating = db.Column(db.Integer)
    
#     serialize_rules = ('-recipe', '-recipe_id', '-user_id',)
    
#     def __repr__(self):
#         return f'<Review {self.id}>'
    
