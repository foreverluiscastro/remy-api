#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe, Ingredient, RecipeIngredient, SavedRecipe
from openai_service import generate_recipe

@app.before_request
def check_if_logged_in():
    open_access_list = [
        'signup',
        'login',
        'check_session'
    ]

    if (request.endpoint) not in open_access_list and (not session.get('user_id')):
        return {'error': '401 Unauthorized'}, 401


class Signup(Resource):
    
    def post(self):

        request_json = request.get_json()

        username = request_json.get('username')
        password = request_json.get('password')
        # image_url = request_json.get('image_url')
        # bio = request_json.get('bio')
        # breakpoint()
        # breakpoint()
        try:
            user = User(
                username=username,
                # image_url=image_url,
                # bio=bio
            )
            # the setter will encrypt this
            user.password_hash = password
        except ValueError as err:
            # breakpoint()
            return {'message': str(err)}, 400

        try:

            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            return user.to_dict(), 201

        except IntegrityError:

            return {'error': '422 Unprocessable Entity'}, 422

class CheckSession(Resource):

    def get(self):
        # breakpoint()
        
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict(), 200
        
        return {'error': "Unauthorized."}, 401

class Login(Resource):
    
    def post(self):

        request_json = request.get_json()

        username = request_json.get('username')
        password = request_json.get('password')
        # breakpoint()
        user = User.query.filter(User.username == username).first()
        # breakpoint()

        if user:
            if user.authenticate(password):

                session['user_id'] = user.id
                return user.to_dict(), 200

        return {'message': 'Username or password is incorrect.'}, 401

class Logout(Resource):

    def delete(self):

        session['user_id'] = None
        
        return {}, 204
        
class GenerateRecipe(Resource):
    
    def post(self):
        # get request JSON
        # breakpoint()
        data = request.get_json()
        generated_recipe = generate_recipe(data)
        # breakpoint()
        return generated_recipe, 200
        
        
        
        
class RecipeIndex(Resource):

    def get(self):
        # breakpoint()
        user = User.query.get(session.get('user_id'))
        recipes = Recipe.query.all()
        saved_recipes_ids = [saved_recipe.recipe_id for saved_recipe in user.saved_recipes]
        
        if request.args.get("query") == "featured_recipes":
            
            response = []
            for recipe in recipes:
                recipe_dict = recipe.to_dict()
                recipe_dict['is_saved'] = recipe.id in saved_recipes_ids or recipe.user.id == user.id
                response.append(recipe_dict)
            # breakpoint()
            return response, 200
        
        elif request.args.get("query") == "saved_recipes":
            # user = User.query.filter(User.id == session['user_id']).first()
            # breakpoint()
            # return [saved_recipe.recipe.to_dict() for saved_recipe in user.saved_recipes],200
            response = []
            for saved_recipe in user.saved_recipes:
                saved_recipe_dict = saved_recipe.to_dict()
                saved_recipe_dict['recipe']['is_saved'] = True
                response.append(saved_recipe_dict['recipe'])
            
            return response, 200
        
        elif request.args.get("query") == "my_recipes":
            # user = User.query.filter(User.id == session['user_id']).first()
            
            # return [recipe.to_dict() for recipe in user.recipes], 200
            response = []
            for recipe in user.recipes:
                recipe_dict = recipe.to_dict()
                recipe_dict['is_saved'] = True
                response.append(recipe_dict)
            
            return response, 200
        
        
    def post(self):
        request_json = request.get_json()

        title = request_json['title']
        recipe_ingredients = request_json['recipe_ingredients']
        instructions = request_json['instructions']
        image_url = request_json.get('image_url')

        try:
            # Create the recipe
            recipe = Recipe(
                title=title,
                instructions=instructions,
                image_url=image_url,
                user_id=session['user_id'],
            )

            db.session.add(recipe)
            db.session.commit()

            # Create recipe ingredients
            for ingredient_data in recipe_ingredients:
                # breakpoint()
                ingredient_name = ingredient_data['ingredient']['name']
                ingredient_amount = ingredient_data['amount']

                # Check if the ingredient already exists
                ingredient = Ingredient.query.filter_by(name=ingredient_name).first()

                # If not, create a new ingredient
                if not ingredient:
                    ingredient = Ingredient(name=ingredient_name)
                    db.session.add(ingredient)
                    db.session.commit()  # Commit new ingredient before associating

                # Create recipe ingredient association
                recipe_ingredient = RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    amount=ingredient_amount
                )
                db.session.add(recipe_ingredient)

            db.session.commit()

            return recipe.to_dict(), 201

        except IntegrityError:
            db.session.rollback()  # Rollback changes if an error occurs
            return {'error': '422 Unprocessable Entity'}, 422
        
class RecipeShow(Resource):
    def delete(self, id):
        # pass
        # breakpoint()
        user = User.query.get(session.get('user_id'))
        recipes = user.recipes
        
        # breakpoint()
        
        recipe = next((recipe for recipe in recipes if recipe.id == id), None)
        # use a find method to find the element in the list that has a recipe.id equal to the argument id
        # breakpoint()
        db.session.delete(recipe)
        db.session.commit()
        
        return {}, 200
        
class SavedRecipeIndex(Resource):
        
    def post(self):
        json_data = request.get_json()
        user_id = json_data["user_id"]
        recipe_id = json_data["recipe_id"]
            
            
        saved_recipe = SavedRecipe(
            user_id=user_id,
            recipe_id=recipe_id
        )
        db.session.add(saved_recipe)
        db.session.commit()
        return saved_recipe.to_dict(), 201
    
class SavedRecipeShow(Resource):
    
    def delete(self, id):
        # user = "luis"
        user = User.query.get(session.get('user_id'))
        recipes = user.saved_recipes
        
        # breakpoint()
        
        saved_recipe = next((recipe for recipe in recipes if recipe.recipe_id == id), None)
        # use a find method to find the element in the list that has a recipe_id equal to the argument id
        # breakpoint()
        db.session.delete(saved_recipe)
        db.session.commit()
        
        return {}, 200
        
    
    # def get(self, recipe_id):
    #     saved_recipe = SavedRecipe.query.get(recipe_id)
    #     if saved_recipe:
    #         return saved_recipe.to_dict(), 200
    #     else:
    #         return {'error': '404 Not Found'}, 404
        
        

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/me', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes_index')
api.add_resource(RecipeShow, '/recipes/<int:id>', endpoint='recipes_show')
api.add_resource(SavedRecipeIndex, '/saved_recipes', endpoint='saved_recipes_index')
api.add_resource(SavedRecipeShow, '/saved_recipes/<int:id>', endpoint='saved_recipes_show')
api.add_resource(GenerateRecipe, '/generate_recipe', endpoint='generate_recipe')

if __name__ == '__main__':
    app.run(port=5555, debug=True)