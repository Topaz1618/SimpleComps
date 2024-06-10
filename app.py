import os
import logging
from flask import Flask, render_template, session, send_from_directory, request, jsonify

from config import Config
from models import Session, Category, Product


app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
# app.config['SESSION_COOKIE_DOMAIN'] = '.tototales.online'
app.config['IMAGE_FOLDER'] = "static/publisher/img"
app.secret_key = Config.get_secret_key()
app.logger.setLevel(logging.DEBUG)


@app.route('/')
def index():
    return render_template('manage_category.html')  # 假设您的 Vue 应用文件名为 index.html


@app.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'GET':
        session = Session()
        categories = session.query(Category).all()
        result = [{'id': c.id, 'name': c.name} for c in categories]
        session.close()
        return jsonify(result)

    elif request.method == 'POST':
        session = Session()
        name = request.json.get('name')
        if name:
            new_category = Category(name=name)
            session.add(new_category)
            session.commit()
            response = {'id': new_category.id, 'name': new_category.name}
            session.close()
            return jsonify(response), 201
        session.close()
        return jsonify({'error': 'Name is required'}), 400


@app.route('/delete_categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    session = Session()
    category = session.query(Category).filter_by(id=id).first()
    if category:
        session.delete(category)
        session.commit()
        session.close()
        return jsonify({'success': True}), 200
    session.close()
    return jsonify({'error': 'Category not found'}), 404


@app.route('/products/<int:id>', methods=['GET', 'POST'])
def products(id):
    if request.method == 'GET':
        session = Session()
        category = session.query(Category).filter(Category.id == id).one()


        products = [{'id': p.id, 'name': p.name, 'url': p.url, 'description': p.description} for p in category.products]
        session.close()
        return render_template('manage_product.html',  products=products)

    elif request.method == 'POST':
        session = Session()
        name = request.json.get('name')
        url = request.json.get('url')
        description = request.json.get('description')
        category_id = request.json.get('category_id')

        new_product = Product(
            name=name,
            url=url,  # Provide a default or make it required in your request
            description=description,
            category_id=category_id  # Make sure this id is passed in or handle accordingly
        )
        session.add(new_product)
        session.commit()

        response = {'id': new_product.id, 'name': new_product.name}
        session.close()
        return jsonify(response), 201


@app.route('/delete_product/<int:id>', methods=['DELETE'])
def delete_product(id):
    session = Session()
    product = session.query(Product).filter_by(id=id).first()
    if product:
        session.delete(product)
        session.commit()
        session.close()
        return jsonify({'success': True}), 200
    session.close()
    return jsonify({'error': 'Category not found'}), 404




@app.route('/categories/<category_name>', methods=['GET'])
def get_category_products(category_name):
    category = Category.query.filter_by(name=category_name).first()
    if category:
        products = Product.query.filter_by(category_id=category.id).all()
        product_data = [{'name': product.name, 'url': product.url, 'description': product.description,
                         'added_time': product.added_time} for product in products]
        return jsonify(product_data)
    else:
        return jsonify({'error': 'Category not found'}), 404



if __name__ == '__main__':
    app.run(debug=True, port=8010)
