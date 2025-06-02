from flask import Flask, render_template, request, redirect, url_for
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

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

    def __repr__(self):
        return f'<Item {self.item_number}>'

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    module = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    website = db.Column(db.String(120))
    address = db.Column(db.Text)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    pincode = db.Column(db.String(6))
    gst = db.Column(db.String(15))
    pan = db.Column(db.String(10))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Company {self.name}>'

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    gst = db.Column(db.String(15))
    address = db.Column(db.Text)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    pincode = db.Column(db.String(6))
    status = db.Column(db.String(20), default='active')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Supplier {self.name}>'

# Base View
class DashboardView(MethodView):
    def get(self):
        try:
            stats = {
                'total_items': db.session.query(func.count(Items.id)).scalar() or 0,
                'total_purchase': db.session.query(func.count(Purchase.id)).scalar() or 0,
                'total_sales': db.session.query(func.count(Sale.id)).scalar() or 0,
                'total_customers': db.session.query(func.count(Customer.id)).scalar() or 0
            }
            return render_template('dashboard.html', stats=stats)
        except Exception as e:
            print(f"Error in dashboard: {e}")
            return render_template('dashboard.html', stats={
                'total_items': 0,
                'total_purchase': 0,
                'total_sales': 0,
                'total_customers': 0
            })

# Admin Views
class UsersView(MethodView):
    def get(self):
        return render_template('admin/users.html')

class RolesView(MethodView):
    def get(self):
        roles = Role.query.all()
        return render_template('admin/roles.html', roles=roles)

    def post(self):
        try:
            data = request.get_json()
            new_role = Role(name=data['name'])
            db.session.add(new_role)
            db.session.commit()
            return {'success': True, 'message': 'Role added successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}, 400

class PermissionsView(MethodView):
    def get(self):
        permissions = Permission.query.all()
        return render_template('admin/permissions.html', permissions=permissions)

    def post(self):
        try:
            data = request.get_json()
            new_permission = Permission(
                name=data['name'],
                description=data['description'],
                module=data['module']
            )
            db.session.add(new_permission)
            db.session.commit()
            return {'success': True, 'message': 'Permission added successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}, 400

# Master Views
class CompanyView(MethodView):
    def get(self):
        company = Company.query.first()
        return render_template('master/company.html', company=company)

    def post(self):
        try:
            data = request.get_json()
            company = Company.query.first()
            if not company:
                company = Company()
                db.session.add(company)
            
            for key, value in data.items():
                setattr(company, key, value)
            
            db.session.commit()
            return {'success': True, 'message': 'Company details saved successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}, 400

class SuppliersView(MethodView):
    def get(self):
        suppliers = Supplier.query.all()
        return render_template('master/suppliers.html', suppliers=suppliers)

    def post(self):
        try:
            data = request.get_json()
            new_supplier = Supplier(**data)
            db.session.add(new_supplier)
            db.session.commit()
            return {'success': True, 'message': 'Supplier added successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}, 400

class CustomersView(MethodView):
    def get(self):
        customers = Customer.query.all()
        return render_template('master/customers.html', customers=customers)

    def post(self):
        try:
            data = request.get_json()
            new_customer = Customer(**data)
            db.session.add(new_customer)
            db.session.commit()
            return {'success': True, 'message': 'Customer added successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}, 400

    def delete(self, customer_id):
        try:
            customer = Customer.query.get_or_404(customer_id)
            db.session.delete(customer)
            db.session.commit()
            return {'success': True}, 200
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}, 400

# Items Views
class AddItemView(MethodView):
    def get(self):
        all_items = Items.query.order_by(Items.id.desc()).all()
        return render_template('items/add_item.html', items=all_items)

    def post(self):
        try:
            # Get form data
            data = request.form if request.form else request.get_json()
            
            # Get last item number
            last_item = Items.query.order_by(Items.id.desc()).first()
            item_number = last_item.item_number.split('-')[len(last_item.item_number.split('-'))] if last_item else 0
            item_number = (int(item_number) + 1) if last_item else 1

            new_item = Items(
                item_number=item_number,
                denier=data.get('denier'),
                item=data.get('item'),
                size=data.get('size'),
                colour=data.get('colour'),
                quantity=data.get('quantity'),
                unit=data.get('unit'),
                quantity1=data.get('quantity1'),
                unit1=data.get('unit1'),
                price=data.get('price', '0')
            )
            db.session.add(new_item)
            db.session.commit()
            sucess = {'success':True, 'message' :f"Item {new_item.item} added successfully with item number {new_item.item_number}"},200
            return redirect(url_for('add_item'),sucess=sucess)
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}, 400

    def put(self, item_id):
        try:
            item = Items.query.get_or_404(item_id)
            data = request.get_json()

            for key, value in data.items():
                setattr(item, key, value)

            db.session.commit()
            return {'success': True, 'message': 'Item updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}, 400

    def delete(self, item_id):
        try:
            item = Items.query.get_or_404(item_id)
            db.session.delete(item)
            db.session.commit()
            return {'success': True, 'message': 'Item deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}, 400

class ItemListView(MethodView):
    def get(self):
        return render_template('items/item_list.html')

class CategoriesView(MethodView):
    def get(self):
        return render_template('items/categories.html')

# Transaction Views
class PurchaseView(MethodView):
    def get(self):
        return render_template('transactions/purchase.html')

class SalesView(MethodView):
    def get(self):
        return render_template('transactions/sales.html')

class StockTransferView(MethodView):
    def get(self):
        return render_template('transactions/stock_transfer.html')

# Report Views
class StockReportView(MethodView):
    def get(self):
        return render_template('reports/stock_report.html')

class SalesReportView(MethodView):
    def get(self):
        return render_template('reports/sales_report.html')

class PurchaseReportView(MethodView):
    def get(self):
        return render_template('reports/purchase_report.html')

class TransactionReportView(MethodView):
    def get(self):
        return render_template('reports/transaction_report.html')

# Settings View
class SettingsView(MethodView):
    def get(self):
        return render_template('settings.html')

# Register URLs
app.add_url_rule('/', view_func=DashboardView.as_view('dashboard'))

# Admin URLs
app.add_url_rule('/users', view_func=UsersView.as_view('users'))
app.add_url_rule('/roles', view_func=RolesView.as_view('roles'))
app.add_url_rule('/permissions', view_func=PermissionsView.as_view('permissions'))

# Master URLs
app.add_url_rule('/company', view_func=CompanyView.as_view('company'))
app.add_url_rule('/suppliers', view_func=SuppliersView.as_view('suppliers'))
app.add_url_rule('/customers', view_func=CustomersView.as_view('customers'))

# Items URLs
app.add_url_rule('/add-item', view_func=AddItemView.as_view('add_item'))
app.add_url_rule('/add-item/<int:item_id>', view_func=AddItemView.as_view('edit_item'))
app.add_url_rule('/items', view_func=ItemListView.as_view('item_list'))
app.add_url_rule('/categories', view_func=CategoriesView.as_view('categories'))

# Transaction URLs
app.add_url_rule('/purchase', view_func=PurchaseView.as_view('purchase'))
app.add_url_rule('/sales', view_func=SalesView.as_view('sales'))
app.add_url_rule('/stock-transfer', view_func=StockTransferView.as_view('stock_transfer'))

# Report URLs
app.add_url_rule('/reports/stock', view_func=StockReportView.as_view('stock_report'))
app.add_url_rule('/reports/sales', view_func=SalesReportView.as_view('sales_report'))
app.add_url_rule('/reports/purchase', view_func=PurchaseReportView.as_view('purchase_report'))
app.add_url_rule('/reports/transactions', view_func=TransactionReportView.as_view('transaction_report'))

# Settings URL
app.add_url_rule('/settings', view_func=SettingsView.as_view('settings'))

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    app.run(debug=True)

