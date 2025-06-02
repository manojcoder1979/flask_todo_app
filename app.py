from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
from flask.views import MethodView

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

class IndexView(MethodView):
    def get(self):
        all_items = Items.query.all()
        return render_template('index.html', all_items=all_items)

class DashboardView(MethodView):
    def get(self):
        result = (
            db.session.query(
                Items.item,
                Items.colour,
                Items.size,
                func.sum(Items.quantity).label('bag'),
                func.sum(Items.quantity1).label('wt')
            )
            .group_by(Items.item, Items.colour, Items.size)
            .all()
        )
        return render_template('dashboard.html', result=result)

class AddItemView(MethodView):
    def post(self):
        try:
            last_item = Items.query.order_by(Items.id.desc()).first()
            if last_item is None:
                raw_number = 1
            else:
                try:
                    raw_number = int(last_item.item_number) + 1
                except Exception:
                    raw_number = 1

            new_item = Items(
                item_number=raw_number,
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
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            print(f"Error adding item: {e}")
            return redirect(url_for('index'))

class EditItemView(MethodView):
    def get(self, item_id):
        item_to_edit = Items.query.get_or_404(item_id)
        return render_template('edit.html', item=item_to_edit)

    def post(self, item_id):
        try:
            item_to_update = Items.query.get_or_404(item_id)
            item_to_update.denier = request.form.get('denier')
            item_to_update.item = request.form.get('item')
            item_to_update.size = request.form.get('size')
            item_to_update.colour = request.form.get('colour')
            item_to_update.quantity = request.form.get('quantity')
            item_to_update.unit = request.form.get('unit')
            item_to_update.quantity1 = request.form.get('quantity1')
            item_to_update.unit1 = request.form.get('unit1')
            item_to_update.price = request.form.get('price')
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            print(f"Error updating item: {e}")
            return redirect(url_for('index'))

class DeleteItemView(MethodView):
    def post(self, item_id):
        try:
            item_to_delete = Items.query.get_or_404(item_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting item: {e}")
            return redirect(url_for('index'))

# Register the views
app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))
app.add_url_rule('/add_item', view_func=AddItemView.as_view('add_item'))
app.add_url_rule('/edit/<int:item_id>', view_func=EditItemView.as_view('edit_item'))
app.add_url_rule('/delete/<int:item_id>', view_func=DeleteItemView.as_view('delete'))

# Define the main function
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

