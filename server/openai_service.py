import os
import openai
import json
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_recipe(request):
  
  json_data = request
  # breakpoint()
  if json_data.get('recipe') != None:
    # breakpoint()
    prompt = f"""PROMPT
    Given this object of information: {json_data['recipe']} and this array of missing ingredients: {json_data['missing_ingredients']}, generate a recipe using the same exact object format while omitting those ingredients. The response format should adhere to the following structure: {{
      "title": Example Recipe Title,
      "recipe_ingredients": [
        {{
          "ingredient": {{"name": Example Ingredient}},
          "amount": Example Amount
        }},
        // Additional ingredient objects follow this format
      ],
      "instructions": Example instructions string detailing the cooking process. Do NOT make this a numbered list.,
      "categories": An array of strings describing the plate.,
    }}.
    """
    
    messages = [{"role": "user", "content": prompt}]
    # breakpoint()
    try:
      response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0
      )
      json_res = json.loads(response.choices[0].message['content'])
      return json_res
    except Exception as e:
      print(e)
  else:
    prompt = f"""PROMPT
    Generate a customized recipe based on the provided ingredients, cooking styles, and the number of guests. The ingredients array includes: {json_data['ingredients']}. The styles array includes: {json_data['styles']}. The number of guests is: {json_data["guests"]}. The response format should adhere to the following structure: {{
      "title": Example Recipe Title,
      "recipe_ingredients": [
        {{
          "ingredient": {{"name": Example Ingredient}},
          "amount": Example Amount
        }},
        // Additional ingredient objects follow this format
      ],
      "instructions": Example instructions string detailing the cooking process. Do NOT make this a numbered list.,
      "categories": An array of strings describing the plate.,
    }}. PROMPT"""
  
    messages = [{"role": "user", "content": prompt}]
  
    try:
      response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
      )
      json_res = json.loads(response.choices[0].message['content'])
    
    # testing
    # title = json_res.get('title')
    # instructions = json_res.get('instructions')
    # recipe_ingredients = json_res.get('recipe_ingredients')
    # breakpoint()
    
    # print(response.choices[0].message['content'])
      return json_res
    except Exception as e:
      print(e)
    
# generate_recipe({
#   "ingredients": [
#     "chicken",
#     "cherry tomatoes",
#     "penne",
#     "milk",
#     "provolone",
#     "garlic",
#     "parmesean",
#     "parsley",
#     "butter",
#     ],
#   "styles": [
#     "pasta",
#     "italian"
#   ],
#   "guests": 2  
# })