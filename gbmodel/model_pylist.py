"""
Python list model
"""
from datetime import date
from .Model import Model

class model(Model):
    def __init__(self):
        """
        Create an empty dictionary and then calls the populateDict function to insert hardcoded recipes
        """
        self.recipes = {}
        self.populateDict()
                

    def select(self):
        """
        Returns recipeentries list of lists
        Each list in recipeentries contains: title, author, ingredients, time, skill, description
        :return: List of Dict
        """
        return self.recipes
    
    def populateDict(self):
        """
        Function to populate hardcoded recipes into a dictionary
        """
        self.recipes["Italian Grilled Cheese Sandwiches"] = {
            "title": "Italian Grilled Cheese Sandwiches",
            "author": "NYCDAVE",
            "ingredients": "1/4 cup of butter, 12 slices of white bread, 8 ounces of mozzarella cheese, 1 stick butter",
            "time": "8",
            "skill": "2",
            "description": "Preheat your oven's broiler. Place 6 slices of bread into a baking sheet. Spread mozzarella cheese over each slice. Top with the remaining 6 slices of brea. Mix together garlic and butter and then brush over the top of the sandwiches. Place baking sheet under the broiler for 2 to 3 minutes, until golden brown, then flip. Brush butter and return to broiler for another 2 to 3 minutes. Enjoy!",
            "img": "https://thenypost.files.wordpress.com/2017/05/shutterstock_291466391.jpg?quality=90&strip=all&w=618&h=410&crop=1",
            }
        self.recipes["Salmon with Brown Sugar Glaze"] = {
            "title": "Salmon with Brown Sugar Glaze",
            "author": "Tamara",
            "ingredients": "1/4 cup packed light brown sugar, 2 tbsp dijon mustard, 4 (6 ounces) boneless salmon fillets",
            "time": "15",
            "skill": "3",
            "description": "Preheat the oven's broiler and set the oven rack at about 6 inches from the heat source, prepare the rack of a broiler pan with cooking spray. Season the salmon with salt and pepper and arrange onto the prepared broiler pan. Whisk together the brown sugar and Dijon mustard in a small bowl; spoon mixture evenly onto top of salmon fillets. Cook under the preheated broiler until the fish flakes easily with a fork, 10 to 15 minutes.",
            "img" : "https://assets.marthastewart.com/styles/wmax-750/d37/med106601_0411_eas_salmon_brown_sugar/med106601_0411_eas_salmon_brown_sugar_horiz.jpg?itok=G0AJf5R8",
        }
        return True
