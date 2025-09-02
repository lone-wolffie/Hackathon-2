from flask import Flask, request, jsonify, render_template
from db_config import get_db_connection
from hugging_face import enrich_ingredients
from spoonacular_api import get_recipes
from intasend import APIService  
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Initialize IntaSend service
INTASEND_SECRET_KEY = os.getenv("INTASEND_SECRET_KEY")   
service = APIService(token=INTASEND_SECRET_KEY, test=True)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Recommend recipes route
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    raw_input = data.get("ingredients", "")
    refined_input = enrich_ingredients(raw_input)
    recipes = get_recipes(refined_input)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for r in recipes:
        ingredients_text = "\n".join(r['ingredients'])
        steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(r['steps'])])
        description = f"Ingredients:\n{ingredients_text}\n\nSteps:\n{steps_text}"
        nutrition = f"{r['calories']} calories, Ready in {r['readyInMinutes']} minutes"

        cursor.execute(
            "INSERT INTO recipes (title, description, nutrition) VALUES (%s, %s, %s)",
            (r['title'], description, nutrition)
        )
    
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify(recipes)

# Pay route
@app.route("/pay", methods=["POST"])
def pay():
    try:
        data = request.get_json()
        amount = data.get("amount", 100)
        email = data.get("email", "customer@example.com")

        # Create checkout link
        response = service.collect.checkout(
            email=email,
            amount=amount,
            currency="KES",
            comment="Payment for services",
            redirect_url=""
        )

        return jsonify({"checkout_url": response.get("url")}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
