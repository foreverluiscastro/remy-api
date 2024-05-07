#!/usr/bin/env python3

from app import app
import random
from models import db, User, Ingredient, Recipe, RecipeIngredient, SavedRecipe, Category, RecipeCategory

users_data = [
  {
    "username": "ChefMasterMatt",
    "password": "test",
  },
    {
    "username": "CulinaryQueen",
    "password": "test",
  },
  {
    "username": "FlavorFanatic",
    "password": "test",
  },
  {
    "username": "RecipeWizard",
    "password": "test",
  },
  {
    "username": "FoodieFred",
    "password": "test",
  },
]

recipes_data = [
  {
    "title": "Asian Chicken Stir Fry",
    "categories": [ "Asian", "Stir Fry"],
    "recipe_ingredients": [
      { "name": "Chicken", "amount": "2 boneless, skinless chicken breasts (about 300g)"},
      { "name": "Carrots", "amount": "2 medium carrots, sliced thinly"},
      { "name": "Onions", "amount": "1 small onion, sliced"},
      { "name": "Garlic", "amount": "2 cloves, minced"},
      { "name": "Soy Sauce", "amount": "3 tablespoons"},
      { "name": "Rice Vinegar", "amount": "1 tablespoon"},
      { "name": "Sesame Oil", "amount": "1 tablespoon"},
      { "name": "Cornstarch", "amount": "1 teaspoon"},
      { "name": "Salt", "amount": "1/2 teaspoon"},
      { "name": "Pepper", "amount": "1/4 teaspoon"},
      { "name": "Oil", "amount": "2 tablespoons for stir-frying"}
    ],
    "instructions": "Cut the chicken breasts into bite-sized pieces and place them in a bowl. Add soy sauce, rice vinegar, sesame oil, cornstarch, salt, and pepper. Mix well to coat the chicken evenly. Let it marinate for about 15 minutes. Heat 1 tablespoon of oil in a large skillet or wok over medium-high heat. Add minced garlic and stir-fry for about 30 seconds until fragrant. Add the marinated chicken to the skillet and spread it out into a single layer. Let it cook undisturbed for about 2-3 minutes until it starts to brown. Then, stir-fry until the chicken is cooked through and golden brown. Remove the chicken from the skillet and set it aside. In the same skillet, add the remaining tablespoon of oil if needed. Add sliced onions and carrots. Stir-fry for about 3-4 minutes until they're tender-crisp. Return the cooked chicken to the skillet and stir everything together until heated through. Serve the Asian chicken stir-fry hot over cooked rice or noodles. Enjoy!",
    "user_id": 1,
    "image_url": "https://www.allrecipes.com/thmb/yhGfpmse-RSLsZ4cE0sNHDaCr1o=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/223382_chicken-stir-fry_Rita-1x1-1-b6b835ccfc714bb6a8391a7c47a06a84.jpg",
  },
  {
    "title": "Italian Pasta Primavera",
    "categories": [ "Italian", "Pasta", "Vegetarian"],
    "recipe_ingredients": [
      { "name": "Penne Pasta", "amount": "250g"},
      { "name": "Zucchini", "amount": "1 medium, sliced"},
      { "name": "Bell Peppers", "amount": "1 red and 1 yellow, diced"},
      { "name": "Cherry Tomatoes", "amount": "1 cup, halved"},
      { "name": "Garlic", "amount": "3 cloves, minced"},
      { "name": "Olive Oil", "amount": "3 tablespoons"},
      { "name": "Italian Seasoning", "amount": "1 tablespoon"},
      { "name": "Salt", "amount": "1 teaspoon"},
      { "name": "Black Pepper", "amount": "1/2 teaspoon"}
    ],
    "instructions": "Cook penne pasta according to package instructions. In a large skillet, heat olive oil over medium heat. Add minced garlic and sauté until fragrant. Add sliced zucchini, diced bell peppers, and halved cherry tomatoes. Cook until vegetables are tender. Season with Italian seasoning, salt, and black pepper. Toss cooked pasta into the skillet with the vegetables. Stir until pasta is well coated. Serve hot and enjoy!",
    "user_id": 5,
    "image_url": "https://www.budgetbytes.com/wp-content/uploads/2023/05/Pasta-Primavera-V3-768x1024.jpg"
  },
  {
    "title": "Mexican Beef Tacos",
    "categories": [ "Mexican", "Tacos"],
    "recipe_ingredients": [
      { "name": "Beef", "amount": "500g, minced"},
      { "name": "Tortillas", "amount": "8 small, corn or flour"},
      { "name": "Onion", "amount": "1 large, diced"},
      { "name": "Tomato", "amount": "2 medium, diced"},
      { "name": "Lettuce", "amount": "1 head, shredded"},
      { "name": "Cheese", "amount": "1 cup, shredded"},
      { "name": "Cilantro", "amount": "1/4 cup, chopped"},
      { "name": "Lime", "amount": "2, cut into wedges"},
      { "name": "Cumin", "amount": "2 teaspoons"},
      { "name": "Chili Powder", "amount": "1 tablespoon"},
      { "name": "Salt", "amount": "1 teaspoon"},
      { "name": "Black Pepper", "amount": "1/2 teaspoon"}
    ],
    "instructions": "In a skillet, cook minced beef over medium heat until browned. Add diced onion and cook until softened. Stir in cumin, chili powder, salt, and black pepper. Warm tortillas on a separate skillet. Fill each tortilla with beef mixture, diced tomatoes, shredded lettuce, shredded cheese, and chopped cilantro. Squeeze fresh lime juice over the tacos. Serve hot.",
    "user_id": 3,
    "image_url": "https://kaynutrition.com/wp-content/uploads/2023/08/shredded-beef-tacos.jpg"
  },
  {
    "title": "Classic Spaghetti Bolognese",
    "categories": [ "Italian", "Pasta"],
    "recipe_ingredients": [
      { "name": "Spaghetti", "amount": "400g"},
      { "name": "Ground Beef", "amount": "500g"},
      { "name": "Onion", "amount": "1 large, diced"},
      { "name": "Carrot", "amount": "1 large, grated"},
      { "name": "Celery", "amount": "2 stalks, diced"},
      { "name": "Garlic", "amount": "3 cloves, minced"},
      { "name": "Canned Tomatoes", "amount": "800g, crushed"},
      { "name": "Tomato Paste", "amount": "2 tablespoons"},
      { "name": "Red Wine", "amount": "1/2 cup"},
      { "name": "Beef Stock", "amount": "1 cup"},
      { "name": "Olive Oil", "amount": "2 tablespoons"},
      { "name": "Salt", "amount": "1 teaspoon"},
      { "name": "Black Pepper", "amount": "1/2 teaspoon"},
      { "name": "Parmesan Cheese", "amount": "for serving"}
    ],
    "instructions": "Cook spaghetti according to package instructions. In a large pot, heat olive oil over medium heat. Add diced onion, grated carrot, diced celery, and minced garlic. Cook until vegetables are softened. Add ground beef and cook until browned. Stir in crushed tomatoes, tomato paste, red wine, and beef stock. Season with salt and black pepper. Simmer sauce for 30 minutes. Serve sauce over cooked spaghetti. Sprinkle with grated Parmesan cheese.",
    "user_id": 2,
    "image_url": "https://www.recipetineats.com/wp-content/uploads/2018/07/Spaghetti-Bolognese.jpg?resize=650,910"
  },
  {
    "title": "Indian Butter Paneer",
    "categories": [ "Indian", "Asian", "Vegetarian"],
    "recipe_ingredients": [
      { "name": "Paneer", "amount": "400g, cubed"},
      { "name": "Tomatoes", "amount": "4 large, pureed"},
      { "name": "Onion", "amount": "2 large, finely chopped"},
      { "name": "Ginger", "amount": "1-inch piece, grated"},
      { "name": "Garlic", "amount": "4 cloves, minced"},
      { "name": "Green Chilies", "amount": "2, finely chopped"},
      { "name": "Cumin Seeds", "amount": "1 teaspoon"},
      { "name": "Turmeric Powder", "amount": "1/2 teaspoon"},
      { "name": "Coriander", "amount": "1 tablespoon"},
      { "name": "Garam Masala", "amount": "1 teaspoon"},
      { "name": "Kasuri Methi", "amount": "1 tablespoon"},
      { "name": "Cream", "amount": "1/2 cup"},
      { "name": "Butter", "amount": "3 tablespoons"},
      { "name": "Salt", "amount": "1 teaspoon"}
    ],
    "instructions": "In a pan, heat butter and add cumin seeds. Once they splutter, add finely chopped onions, grated ginger, minced garlic, and chopped green chilies. Sauté until onions turn golden brown. Add pureed tomatoes and cook until the mixture thickens. Stir in turmeric powder, coriander powder, and salt. Add cubed paneer and simmer for 5 minutes. Add cream and garam masala. Crush kasuri methi between your palms and sprinkle over the dish. Serve hot with naan or rice.",
    "user_id": 4,
    "image_url": "https://www.vegrecipesofindia.com/wp-content/uploads/2020/01/paneer-butter-masala-1-1152x1536.jpg"
  },
  {
    "title": "Thai Green Curry with Shrimp",
    "categories": [ "Asian", "Curry", "Seafood"],
    "recipe_ingredients": [
      { "name": "Shrimp", "amount": "500g, peeled and deveined"},
      { "name": "Green Curry Paste", "amount": "3 tablespoons"},
      { "name": "Coconut Milk", "amount": "1 can (400ml)"},
      { "name": "Eggplant", "amount": "1 small, diced"},
      { "name": "Bell Pepper", "amount": "1, sliced"},
      { "name": "Bamboo Shoots", "amount": "1/2 cup"},
      { "name": "Fish Sauce", "amount": "2 tablespoons"},
      { "name": "Brown Sugar", "amount": "1 tablespoon"},
      { "name": "Thai Basil Leaves", "amount": "1/4 cup"},
      { "name": "Vegetable Oil", "amount": "2 tablespoons"},
      { "name": "Cooked Rice", "amount": "for serving"}
    ],
    "instructions": "Heat vegetable oil in a pan over medium heat. Add green curry paste and cook for a minute. Stir in coconut milk and bring to a simmer. Add diced eggplant, sliced bell pepper, and bamboo shoots. Cook until vegetables are tender. Add peeled and deveined shrimp to the curry. Stir in fish sauce and brown sugar. Simmer until shrimp are cooked through. Garnish with Thai basil leaves. Serve hot over cooked rice.",
    "user_id": 1,
    "image_url": "https://www.wenthere8this.com/wp-content/uploads/2020/12/thai-shrimp-curry-7.jpg"
  },
  {
    "title": "Mediterranean Falafel Wrap",
    "categories": [ "Mediterranean", "Greek", "Vegetarian"],
    "recipe_ingredients": [
      { "name": "Chickpeas", "amount": "1 can (400g), drained and rinsed"},
      { "name": "Onion", "amount": "1 small, chopped"},
      { "name": "Garlic", "amount": "2 cloves, minced"},
      { "name": "Fresh Parsley", "amount": "1/4 cup, chopped"},
      { "name": "Cumin", "amount": "1 teaspoon"},
      { "name": "Coriander", "amount": "1 teaspoon"},
      { "name": "Baking Powder", "amount": "1 teaspoon"},
      { "name": "Salt", "amount": "1 teaspoon"},
      { "name": "Black Pepper", "amount": "1/2 teaspoon"},
      { "name": "Olive Oil", "amount": "3 tablespoons"},
      { "name": "Tahini Sauce", "amount": "1/4 cup"},
      { "name": "Lemon Juice", "amount": "2 tablespoons"},
      { "name": "Pita Bread", "amount": "4 pieces"},
      { "name": "Lettuce", "amount": "1 cup, shredded"},
      { "name": "Tomato", "amount": "1, sliced"},
      { "name": "Cucumber", "amount": "1, sliced"},
      { "name": "Red Onion", "amount": "1/2, thinly sliced"}
    ],
    "instructions": "In a food processor, combine chickpeas, chopped onion, minced garlic, chopped fresh parsley, ground cumin, ground coriander, baking powder, salt, and black pepper. Pulse until mixture is well combined but still slightly chunky. Shape mixture into small patties. Heat olive oil in a skillet over medium-high heat. Fry falafel patties until golden brown and crispy on both sides. In a small bowl, mix tahini sauce with lemon juice. Warm pita bread in a toaster or on a skillet. Fill each pita bread with shredded lettuce, sliced tomato, sliced cucumber, thinly sliced red onion, and falafel patties. Drizzle with tahini sauce. Serve immediately.",
    "user_id": 5,
    "image_url": "https://cookingwithayeh.com/wp-content/uploads/2024/03/Falafel-Wrap-1.jpg"
  },
  {
    "title": "Japanese Ramen Noodle Soup",
    "categories": [ "Asian", "Ramen", "Soup"],
    "recipe_ingredients": [
      { "name": "Ramen Noodles", "amount": "200g"},
      { "name": "Chicken Broth", "amount": "4 cups"},
      { "name": "Chicken Breast", "amount": "2, boneless and skinless"},
      { "name": "Egg", "amount": "2, boiled and halved"},
      { "name": "Green Onion", "amount": "4, thinly sliced"},
      { "name": "Shiitake Mushrooms", "amount": "1 cup, sliced"},
      { "name": "Spinach", "amount": "2 cups"},
      { "name": "Soy Sauce", "amount": "2 tablespoons"},
      { "name": "Mirin", "amount": "1 tablespoon"},
      { "name": "Salt", "amount": "1/2 teaspoon"},
      { "name": "Black Pepper", "amount": "1/4 teaspoon"},
      { "name": "Toasted Sesame Seeds", "amount": "for garnish"}
    ],
    "instructions": "Cook ramen noodles according to package instructions. In a pot, bring chicken broth to a simmer. Add boneless, skinless chicken breasts and simmer until cooked through. Remove chicken from broth and shred using two forks. Return shredded chicken to the pot. Add sliced shiitake mushrooms, spinach, soy sauce, mirin, salt, and black pepper. Simmer for 5 minutes. Divide cooked ramen noodles among serving bowls. Ladle hot soup over the noodles. Garnish with halved boiled eggs, thinly sliced green onions, and toasted sesame seeds. Serve hot.",
    "user_id": 2,
    "image_url": "https://thehintofrosemary.com/wp-content/uploads/2020/02/ramen-cover-768x768.jpg"
  },
  {
    "title": "Greek Salad",
    "categories": [ "Greek", "Salad", "Vegetarian"],
    "recipe_ingredients": [
      { "name": "Cucumber", "amount": "1 large, diced"},
      { "name": "Tomatoes", "amount": "2 large, diced"},
      { "name": "Red Onion", "amount": "1/2, thinly sliced"},
      { "name": "Kalamata Olives", "amount": "1/2 cup"},
      { "name": "Feta Cheese", "amount": "1/2 cup, crumbled"},
      { "name": "Extra Virgin Olive Oil", "amount": "3 tablespoons"},
      { "name": "Red Wine Vinegar", "amount": "2 tablespoons"},
      { "name": "Dried Oregano", "amount": "1 teaspoon"},
      { "name": "Salt", "amount": "1/2 teaspoon"},
      { "name": "Black Pepper", "amount": "1/4 teaspoon"}
    ],
    "instructions": "In a large bowl, combine diced cucumber, diced tomatoes, thinly sliced red onion, and Kalamata olives. Crumble feta cheese over the top. In a small bowl, whisk together extra virgin olive oil, red wine vinegar, dried oregano, salt, and black pepper. Drizzle dressing over the salad and toss to combine. Serve immediately as a side dish or with crusty bread.",
    "user_id": 3,
    "image_url": "https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/08/Greek-Salad-6-1.jpg"
  },
  {
    "title": "Vegetable Paella",
    "categories": [ "Spanish", "Vegetarian"],
    "recipe_ingredients": [
      { "name": "Arborio Rice", "amount": "2 cups"},
      { "name": "Vegetable Broth", "amount": "4 cups"},
      { "name": "Bell Peppers", "amount": "1 red and 1 yellow, diced"},
      { "name": "Tomatoes", "amount": "2 large, diced"},
      { "name": "Green Beans", "amount": "1 cup, trimmed and halved"},
      { "name": "Onion", "amount": "1 large, diced"},
      { "name": "Garlic", "amount": "3 cloves, minced"},
      { "name": "Saffron Threads", "amount": "1/2 teaspoon, crushed"},
      { "name": "Paprika", "amount": "1 teaspoon"},
      { "name": "Frozen Peas", "amount": "1/2 cup"},
      { "name": "Lemon", "amount": "1, sliced"},
      { "name": "Olive Oil", "amount": "3 tablespoons"},
      { "name": "Salt", "amount": "1 teaspoon"},
      { "name": "Black Pepper", "amount": "1/2 teaspoon"}
    ],
    "instructions": "In a large skillet, heat olive oil over medium heat. Add diced onion and minced garlic. Sauté until softened. Add diced bell peppers, diced tomatoes, trimmed and halved green beans, saffron threads, and paprika. Cook until vegetables are slightly tender. Stir in Arborio rice and coat with the vegetable mixture. Pour in vegetable broth and season with salt and black pepper. Bring to a simmer and cook for 20 minutes, stirring occasionally. Add frozen peas during the last 5 minutes of cooking. Garnish with sliced lemon before serving.",
    "user_id": 2,
    "image_url": "https://veganhuggs.com/wp-content/uploads/2019/03/vegan-paella-2.jpg"
  }
]

# creating users
with app.app_context():
  print("Emptying Database...")
  User.query.delete()
  Ingredient.query.delete()
  RecipeIngredient.query.delete()
  Recipe.query.delete()
  SavedRecipe.query.delete()
  print("Database clear!")
  print("Seeding Users...")
  
  users = []
  for u in users_data:
    user = User(username=u["username"])
    user.password_hash = password=u["password"]
    users.append(user)
    
  db.session.add_all(users)
  db.session.commit()
  print("Users seeded! 🌱")
  
  for res in recipes_data:
    
    recipe = Recipe(
      title=res["title"],
      instructions=res["instructions"],
      user_id=res["user_id"],
      image_url=res["image_url"]
    )
    
    db.session.add(recipe)
    db.session.commit()
    
    print("Recipes seeded! 🌱")
    
    for ing in res["recipe_ingredients"]:
      # first seed the ingredients
      
      # check if ingredient exsist
      ingredient = Ingredient.query.filter(Ingredient.name == ing["name"]).first()
      if not ingredient:
        ingredient = Ingredient(name=ing['name'])
        db.session.add(ingredient)
        db.session.commit()
      
      recipe_ingredient = RecipeIngredient(
        recipe_id=recipe.id,
        ingredient_id=ingredient.id,
        amount=ing["amount"]
      )
      
      db.session.add(recipe_ingredient)
      db.session.commit()
      
    for cat in res["categories"]:
      # first seed the ingredients
      
      # check if ingredient exsist
      category = Category.query.filter(Category.name == cat).first()
      
      if not category:
        category = Category(name=cat)
        db.session.add(category)
        db.session.commit()
    
      
      recipe_category = RecipeCategory(
        recipe_id=recipe.id,
        category_id=category.id,
      )
      
      db.session.add(recipe_category)
      db.session.commit()
      
  print("Ingredients seeded! 🌱")
  print("Categories seeded! 🌱")
  print("Recipe ingredients seeded! 🌱")
  print("Recipe Categories seeded! 🌱")

  saved_recipes = []     
  for i in range(10):
    saved_recipe = SavedRecipe(
      recipe_id=random.randint(1, 10),
      user_id=random.randint(1, 5)
    )
    saved_recipes.append(saved_recipe)

  db.session.add_all(saved_recipes)
  db.session.commit()
  print("Saved recipes seeded! 🌱")