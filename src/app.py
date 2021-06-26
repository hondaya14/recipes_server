from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from models import *
import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)

DATABASE_URI = "mysql://root:0000@127.0.0.1/freee_test_web_db?charset=utf8"
engine = create_engine(DATABASE_URI, encoding='utf8')
SessionClass = sessionmaker(engine)
session = SessionClass()


def validation_request(body_field):
    must_body_field = ['title', 'making_time', 'serves', 'ingredients', 'cost']
    for must_key in must_body_field:
        if must_key not in body_field.keys():
            return False
    return True


class Recipes(Resource):
    def post(self):
        body_field = request.json

        if validation_request(body_field):
            new_recipe = RecipesModel().from_json(body_field)
            new_recipe.set_created_timestamp()
            new_recipe.set_updated_timestamp()
            session.add(new_recipe)
            session.commit()
            # title同じレシピをdbから取得
            added_recipe = session.query(RecipesModel).filter(RecipesModel.title == body_field['title']).all()
            added_recipe = [added_recipe[-1].to_dict()]
            response_json = {
                "message": "Recipe successfully created!",
                "recipe": added_recipe
            }
        else:
            response_json = {
                "message": "Recipe creation failed!",
                "required": "title, making_time, serves, ingredients, cost"
            }
        return jsonify(response_json)

    def get(self):
        # dbからレシピを取得
        get_recipes = session.query(RecipesModel).all()
        get_recipes = [get_recipe.to_dict() for get_recipe in get_recipes]
        response_json = {'recipes': get_recipes}
        return jsonify(response_json)


class RecipeID(Resource):
    def get(self, recipe_id):
        # dbからレシピを取得
        get_recipes = session.query(RecipesModel).filter(RecipesModel.id == recipe_id).all()
        if len(get_recipes) != 0:
            recipe_list = [recipe.to_dict() for recipe in get_recipes]
            response_json = {'message': 'Recipe details by id',
                             'recipe': recipe_list}
        else:
            response_json = {'message': 'No Recipe found'}
        return jsonify(response_json)

    def patch(self, recipe_id):
        body_field = request.json
        # 対象idのレシピを取得
        update_recipes = session.query(RecipesModel).filter(RecipesModel.id == recipe_id).all()
        if len(update_recipes) != 0:
            update_recipes[0].title = body_field['title']
            update_recipes[0].making_time = body_field['making_time']
            update_recipes[0].serves = body_field['serves']
            update_recipes[0].ingredients = body_field['ingredients']
            update_recipes[0].cost = body_field['cost']
            update_recipes[0].set_updated_timestamp()
            session.commit()
            # 変更したrecipeを取得
            added_recipe = session.query(RecipesModel).filter(RecipesModel.id == recipe_id).first()
            added_recipe = [added_recipe.to_dict()]

            response_json = {'message': 'Recipe successfully updated!',
                             'recipe': added_recipe}
        else:
            response_json = {'message': 'No Recipe found'}
        return jsonify(response_json)

    def delete(self, recipe_id):
        delete_recipes = session.query(RecipesModel).filter(RecipesModel.id == recipe_id).all()
        if len(delete_recipes) != 0:
            session.delete(delete_recipes[0])
            session.commit()
            response_json = {'message': 'Recipe successfully removed!'}
        else:
            response_json = {'message': 'No Recipe found'}
        return jsonify(response_json)


# endpoints
api.add_resource(Recipes, '/recipes')
api.add_resource(RecipeID, '/recipes/<recipe_id>')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
