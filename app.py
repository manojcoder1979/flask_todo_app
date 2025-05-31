from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from utilities import Utilities 
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)





# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# Define the database model
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_number = db.Column(db.Integer, unique=True, nullable=False)
    denier = db.Column(db.String(100), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Text, nullable=False)
    colour = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)  
    unit = db.Column(db.String(100), nullable=False)
    quantity1 = db.Column(db.String(100), nullable=False)
    unit1 = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)



# Create the database with application context
with app.app_context():
    if not os.path.exists('site.db'):
        db.create_all()
# Define the home route
@app.route('/') 
def index():
    all_items = Items.query.all()  # Changed from items to Items
    
    return render_template('index.html', all_items=all_items)

# Define the add item route
@app.route('/add_item', methods=['POST'])

def add_item():
    last_item = (Items.query.order_by(Items.id.desc()).first())
    # Extract the item number from the last item, or set it to 1 if no items exist
    if last_item is None:
        raw_number = 1
    else:
        try:
            raw_number = int(last_item.item_number.split('-')[-1]) + 1
        except Exception:
            raw_number = 1  # fallback if format is off

    item_number = Utilities(raw_number).get_item_number(
    prefix_format=f"{datetime.now().strftime('%b-%y')}"
)

    try:
        new_item = Items(
            item_number=Utilities(raw_number).get_item_number(
        prefix_format=f"{datetime.now().strftime('%b-%y')}"
    ),
            denier=request.form.get('denier', ''),
            item=request.form.get('item', ''),
            size=request.form.get('size', ''),
            colour=request.form.get('colour', ''),
            quantity=request.form.get('quantity', ''),
            unit=request.form.get('unit', ''),
            quantity1=request.form.get('quantity1', ''),
            unit1=request.form.get('unit1', ''),
            price=request.form.get('price', '0')
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index', highlight=new_item.id))
    except Exception as e:
        db.session.rollback()
        import traceback
        print("Error adding item:")
        traceback.print_exc()
    return redirect(url_for('index'))
# Define the delete item route
@app.route('/delete/<int:item_id>', methods=['GET', 'POST'])
def delete(item_id):
    try:
        item_to_delete = Items.query.get_or_404(item_id)
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting item: {e}")
        return redirect(url_for('index'))
# Define the update item route
@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    item_to_update = Items.query.get_or_404(item_id)
    item_to_update.denier = request.form.get('denier')
    item_to_update.item = request.form.get('item')
    item_to_update.size = request.form.get('size')
    item_to_update.colour = request.form.get('colour')
    item_to_update.quantity = request.form.get('nos')
    item_to_update.unit = request.form.get('unit')
    item_to_update.quantity1 = request.form.get('quantity1')
    item_to_update.unit1 = request.form.get('unit1')
    item_to_update.price = request.form.get('price')

    db.session.commit()
    return redirect(url_for('index'))
# Define the edit item route
@app.route('/edit/<int:item_id>')
def edit_item(item_id):
    item_to_edit = Items.query.get_or_404(item_id)
    return render_template('edit.html', item=item_to_edit)
# Define the search route
@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query')
    all_items = Items.query.filter(Items.item.contains(search_query)).all()
    return render_template('index.html', all_items=all_items)
# Define the sort route
@app.route('/sort', methods=['POST'])
def sort():
    sort_by = request.form.get('sort_by')
    if sort_by == 'item':
        all_items = Items.query.order_by(Items.item).all()
    elif sort_by == 'size':
        all_items = Items.query.order_by(Items.size).all()
    elif sort_by == 'colour':
        all_items = Items.query.order_by(Items.colour).all()
    elif sort_by == 'quantity':
        all_items = Items.query.order_by(Items.quantity).all()
    elif sort_by == 'unit':
        all_items = Items.query.order_by(Items.unit).all()
    elif sort_by == 'price':
        all_items = Items.query.order_by(Items.price).all()
    else:
        all_items = Items.query.all()

    return render_template('index.html', all_items=all_items)
# Define the main function


if __name__ == '__main__':
    import threading as trheading
    from waitress import serve
    def run_server():
        environment = os.getenv('FLASK_ENV', 'production')
        if environment == 'development':
            serve(app.app, host='0.0.0.0', port=5000)
        else:
            serve(app, host='0.0.0.0', port=5000)

    trheading.Thread(target=run_server).start()

