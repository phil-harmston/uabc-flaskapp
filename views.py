from flask import Blueprint

main = Blueprint('main', __name__)

#register routes for our program
@main.route('/')
def main_index():
    return "Blueprint Views.py Hello"

