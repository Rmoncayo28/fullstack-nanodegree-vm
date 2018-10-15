from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/categories/')
def index():
    return render_template('index.html', categories=session.query(Category).all())


@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/')
def category_route(category_id):
    current_category = session.query(Category).get(category_id)
    current_items = session.query(Item).filter_by(category_id=category_id)
    return render_template('index.html', categories=session.query(Category).all(), sel_cat_id=category_id,
                           items=current_items)


@app.route('/items/create', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['category_id']:
            created_item = Item(name=request.form['name'], description=request.form['description'],
                                category=session.query(Category).get(request.form['category_id']))
            session.add(created_item)
            session.commit()
            return redirect(url_for('category_route', category_id=request.form['category_id']), 200)
        else:
            return redirect(url_for('category_route', category_id=request.form['category_id']), 400)
    else:
        cats = session.query(Category).all()
        return render_template('create_item.html', categories=cats)


@app.route('/categories/<int:category_id>/items/<int:item_id>/', methods=['GET', 'POST'])
def item_route(category_id, item_id):
    if request.method == 'POST':
        return do_the_login()
    else:
        current_item = session.query(Item).get(item_id)
        return render_template('item.html', categories=session.query(Category).all(), item=current_item)


@app.route('/categories/<int:category_id>/items/<int:item_id>/update', methods=['GET', 'POST'])
def update_item(category_id, item_id):
    item_to_update = session.query(Item).get(item_id)
    if request.method == "POST":
        new_name = request.form['name']
        new_description = request.form['description']
        new_category = request.form['category_id']
        item_to_update.name = new_name
        item_to_update.description = new_description
        item_to_update.category = session.query(Category).get(new_category)
        session.add(item_to_update)
        session.commit()
        redirect_url = request.url.replace('update', '')
        return redirect(redirect_url, 200)
    else:
        categories = session.query(Category).all()
        return render_template("update_item.html", item=item_to_update, categories=categories)


@app.route('/categories/<int:category_id>/items/<int:item_id>/delete', methods=['POST'])
def delete_item(category_id, item_id):
    item_to_delete = session.query(Item).get(item_id)
    session.delete(item_to_delete)
    session.commit()
    redirect_url = request.url.replace('item_id/delete', '')
    return redirect(url_for('category_route', category_id=category_id), 200)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
