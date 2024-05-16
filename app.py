# BEGIN CODE HERE
from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
from numpy import dot
from numpy.linalg import norm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# END CODE HERE


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    return ""
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    return ""
    # END CODE HERE


# POST endpoint for filtering products based on a given product
@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE

    # Getting the product from the body of the request
    given_product = request.json
    # Creating a vector with its relevant attributes
    # The numeric attributes need to be normalized so that big numbers don't bias the result
    # Calculating the sum of the production years and prices from the stored products
    year_sum = 0
    price_sum = 0
    for product in mongo.db.products.find():
        year_sum += product["production_year"]
        price_sum += product["price"]
    # Normalizing the year and the price by dividing with the sums
    given_product_vector = [given_product["production_year"] / year_sum, given_product["price"] / price_sum]

    # The categorical attributes need to be expressed in distinct binary categories
    # There are 3 different colors, so we add 3 binary categories, one for each color.
    # We place 1 on the category of the corresponding color and 0 to the rest
    if given_product["color"] == 1:
        given_product_vector.extend([1, 0, 0])
    elif given_product["color"] == 2:
        given_product_vector.extend([0, 1, 0])
    elif given_product["color"] == 3:
        given_product_vector.extend([0, 0, 1])

    # There are 4 different sizes, so we add 4 binary categories, one for each size
    if given_product["size"] == 1:
        given_product_vector.extend([1, 0, 0, 0])
    elif given_product["size"] == 2:
        given_product_vector.extend([0, 1, 0, 0])
    elif given_product["size"] == 3:
        given_product_vector.extend([0, 0, 1, 0])
    elif given_product["size"] == 4:
        given_product_vector.extend([0, 0, 0, 1])

    # Creating a list for the filtered products
    filtered_products = []
    # Looping through the products in the database
    for product in mongo.db.products.find():
        # Creating a vector for each product like above
        # Normalizing numeric attributes
        product_vector = [product["production_year"] / year_sum, product["price"] / price_sum]

        # Creating binary categories for the categorical attributes
        if product["color"] == 1:
            product_vector.extend([1, 0, 0])
        elif product["color"] == 2:
            product_vector.extend([0, 1, 0])
        elif product["color"] == 3:
            product_vector.extend([0, 0, 1])

        if product["size"] == 1:
            product_vector.extend([1, 0, 0, 0])
        elif product["size"] == 2:
            product_vector.extend([0, 1, 0, 0])
        elif product["size"] == 3:
            product_vector.extend([0, 0, 1, 0])
        elif product["size"] == 4:
            product_vector.extend([0, 0, 0, 1])

        # Calculating the cosine similarity between the given product and each other product
        cosine_similarity = dot(given_product_vector, product_vector) / (norm(given_product_vector) * norm(product_vector))

        # Adding to the list the name of the products with a similarity over 70%
        if cosine_similarity > 0.7:
            filtered_products.append(product["name"])

    # Returning the filtered list
    return filtered_products

    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    semester_number = (request.args.get('semester'))
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    url = f"https://qa.auth.gr/el/x/studyguide/600000438/current/"
    driver.get(url)
    semester_element_id = f"sem-" + str(semester_number)
    semester_element = driver.find_element(By.ID, semester_element_id)
    courses_table = semester_element.find_element(By.XPATH,"./following-sibling::table[@class='sortable-datatable courses-per-orientation columns-4']")
    course_rows = courses_table.find_elements(By.TAG_NAME, "tr")[1:]  # Προσπερνάμε την πρώτη γραμμή (headers)

    courses_list = []
    for row in course_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        course_title = cells[1].text
        courses_list.append(course_title)

    driver.quit()
    return courses_list  # επιστρέφει τη λίστα με τα μαθήματα
    # END CODE HERE


if __name__ == "__main__":
    app.run(debug=True)

    # mongo.db.products.delete_many({})
    # mongo.db.products.insert_many(
    #    [
    #       {"name": "Egg", "production_year": 2000, "price": 3, "color": 1, "size": 1},
    #       {"name": "Milk", "production_year": 2001, "price": 5, "color": 1, "size": 2},
    #       {"name": "Toast", "production_year": 2000, "price": 5, "color": 2, "size": 3},
    #       {"name": "Juice", "production_year": 2002, "price": 10, "color": 3, "size": 3},
    #       {"name": "Meat", "production_year": 2003, "price": 20, "color": 3, "size": 4},
    #  ]
    # )
