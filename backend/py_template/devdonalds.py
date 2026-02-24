from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here! 
# note: this was motified from 'None' to '{}'
cookbook = {}

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	# TODO: implement me

	# initialise result variable
	res = ""

	# pass over input string
	for i, c in enumerate(recipeName):
		# check if normal character
		if c.isalpha():
			# check if needs capitalisation
			if i == 0 or recipeName[i - 1] in {' ', '-', '_'}:
				c = c.upper()
			else:
				c = c.lower()
			
			# add to results variable
			res += c
			
		# if space, dash, or underscore and not consecutive
		if c in {' ', '-', '_'} and recipeName[i - 1] not in {' ', '-', '_'}:
			res += ' '
		
	# handle null case
	if not res:
		return None

	recipeName = res.strip()

	# return parsed string
	return recipeName


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	# TODO: implement me

	# get post request
	data = request.get_json()

	'''Post Request Verification whilst Creating Relevant Objects'''
	# if recipe
	if data.get("type") == "recipe":
		# check if duplicate recipe name in cookbook
		name = data.get("name")

		for entry in cookbook.values():
			if entry.name == name:
				return 'duplicate name', 400

		
		# check if duplicate required items
		requiredItems = []

		for item in data.get("requiredItems"):
			for current in requiredItems:
				if current.name == item["name"]:
					return 'duplicate required item', 400

			required_item = RequiredItem(
				name=item["name"],
				quantity=item["quantity"]
			)
			
			requiredItems.append(required_item)

		# create recipe object
		recipe = Recipe(
			name=name,
			required_items=requiredItems
		)

		# append final object to cookbook
		cookbook[recipe.name] = recipe


	# if ingredient
	elif data.get("type") == "ingredient":
		# check if duplicate ingredient name
		name = data.get("name")

		for entry in cookbook.values():
			if entry.name == name:
				return 'duplicate name', 400

		# check if valid cooktime
		cook_time = int(data.get("cookTime"))
		
		if cook_time < 0:
			return 'invalid cooktime', 400
		
		# create ingredient object
		ingredient = Ingredient(
			name=name,
			cook_time=cook_time
		)

		cookbook[ingredient.name] = ingredient

	# if invalid
	else:
		return 'invalid type', 400
	

	# return 200 OK
	return 'cookbook updated', 200


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	# TODO: implement me
	
	return 'not implemented', 500


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
