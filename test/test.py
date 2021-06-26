import urllib.request
import urllib.parse
import requests

BASE_URL = 'http://localhost:5000'
POST_RECIPE_PATH = "/recipes"
GET_ALL_RECIPE_PATH = "/recipes"
GET_ONE_RECIPE_PATH = "/recipes/"
UPDATE_RECIPE_PATH = "/recipes/"
DELETE_RECIPE_PATH = "/recipes/"


def main():
    # get_base()
    get_all_recipes_test()

    post_new_recipe_test()
    get_recipe(3)
    update_recipe(3)
    get_recipe(3)
    delete_recipe(3)
    get_recipe(3)

    get_all_recipes_test()


def get_base():
    request = urllib.request.Request(BASE_URL)
    response = urllib.request.urlopen(request)
    print(response.getcode())


def get_all_recipes_test():
    request = urllib.request.Request(BASE_URL+GET_ALL_RECIPE_PATH)
    response = urllib.request.urlopen(request)
    print(response.getcode())
    html = response.read()
    print(html.decode('utf-8'))


def post_new_recipe_test():
    new_recipe = {
        "title": "トマトスープ",
        "making_time": "15分",
        "serves": "5人",
        "ingredients": "玉ねぎ, トマト, スパイス, 水",
        "cost": 450
    }
    response = requests.post(BASE_URL+POST_RECIPE_PATH, json=new_recipe)
    print(response.status_code)
    print(response.text)


def get_recipe(recipe_id):
    response = requests.get(BASE_URL+POST_RECIPE_PATH+f'/{recipe_id}')
    print(response.status_code)
    print(response.text)


def update_recipe(recipe_id):
    recipe = {
        "title": "オムライス",
        "making_time": "20分",
        "serves": "7人",
        "ingredients": "玉ねぎ,卵,スパイス,醤油",
        "cost": 400
    }
    response = requests.patch(BASE_URL+POST_RECIPE_PATH+f'/{recipe_id}', json=recipe)
    print(response.status_code)
    print(response.text)


def delete_recipe(recipe_id):
    response = requests.delete(BASE_URL+POST_RECIPE_PATH+f'/{recipe_id}')
    print(response.status_code)
    print(response.text)


if __name__ == '__main__':
    main()
