from flask import render_template,request,redirect,url_for,flash,jsonify
from flask_login import login_user,logout_user,current_user,login_required
from models import User,Transaction,Budget


def register_routes(app,db,bcrypt):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/signup' ,methods =['GET','POST'])
    def signup():
        if request.method=='GET':
            return render_template('signup.html')
        elif request.method=='POST':
            username = request.form.get('username')
            password = request.form.get('password')

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            user = User(username=username,password=hashed_password)

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
             

    @app.route('/login' ,methods =['GET','POST'])
    def login():
        if request.method=='GET':
            return render_template('login.html')
        elif request.method=='POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter(User.username == username).first()

            if bcrypt.check_password_hash(user.password,password):
                login_user(user)
                return redirect(url_for('set_budget'))
            else:
                return('failed')
            
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))        
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        transactions = Transaction.query.filter_by(user_id=current_user.id).all()
        total_spent = sum(t.amount for t in transactions if t.type == "expense")
        total_income = sum(t.amount for t in transactions if t.type == "income")

        budget_obj = Budget.query.filter_by(user_id=current_user.id).first()
        budget = budget_obj.amount if budget_obj else 0
        balance = budget + total_income - total_spent

        chart_data = {
            'labels': ['Budget Remaining', 'Total Spent'],
            'values': [max(balance, 0), abs(total_spent)]
        }

        return render_template(
            'dashboard.html',
            transactions=transactions,
            budget=budget,
            total_spent=total_spent,
            total_income=total_income,
            balance=balance,
            chart_data=chart_data
        )

    
    @app.route('/set_budget', methods=['GET', 'POST'])
    @login_required
    def set_budget():
        if request.method == 'GET':
            return render_template('budget.html')

        elif request.method == 'POST':
            amount = float(request.form.get('amount'))
            month = request.form.get('month')

            existing = Budget.query.filter_by(user_id=current_user.id).first()

            if existing:
                existing.amount = amount
                existing.month = month
                flash('Budget updated', 'success')
            else:
                budget = Budget(amount=amount, month=month, user_id=current_user.id)
                db.session.add(budget)
                flash('Budget set', 'success')

            db.session.commit()
            return redirect(url_for('dashboard'))

    
    @app.route('/add_transaction',methods=['GET','POST'])
    @login_required
    def add_transaction():
        if request.method=='GET':
            return render_template('add_transaction.html')
        elif request.method=='POST':
            amount = request.form.get('amount')
            type = request.form.get('type')
            description = request.form.get('description')
            

            transaction = Transaction(amount= amount, type = type,description=description,user_id=current_user.id)
            
            db.session.add(transaction)
            db.session.commit()
            return redirect(url_for('dashboard'))
        return render_template('add_transaction.html')
    