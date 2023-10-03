from flask import Flask,render_template,request,jsonify,make_response,redirect,url_for,flash,send_file
from flask_login import login_required,current_user,LoginManager,UserMixin,login_user, logout_user, login_required
from sqlalchemy import desc
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Numeric, String, DateTime, Date, Integer, Boolean, ForeignKey
from flask_migrate import Migrate
import json
import itertools
import psycopg2

from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# @app.context_processor
# def inject_stage_and_region():
#     allRoles = System_Authorization.query.all()
#     rolesAssignedToUser = ''
#     loggedInUser = current_user.id
#     for r in allRoles:
#         role = r.Role
#         users = r.Users
#         if any(str(loggedInUser) in s for s in r.Users):
#             rolesAssignedToUser = role
#
#     return dict(stage=rolesAssignedToUser, region="NA")

# app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SECRET_KEY'] = '67LWxND5o21j1K7iazpO'
app.config ['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:ibrahim9999@localhost:5432/innovatif'
# app.config ['SQLALCHEMY_DATABASE_URI']='postgres://postgres:ibrahim9999@localhost:5432/innovatif'

# app.config ['SQLALCHEMY_----DATABASE_URI']='postgres://egnryascfzveop:c4adc06e060463802bd7f6535e437a2043b790497cc5ac8c8b23fefd4f8c0a66@ec2-52-86-116-94.compute-1.amazonaws.com:5432/dfm91mg3u25t66?sslmode=require'


from dbmodels import *
from addDataInDB import *

from tradelogic.business import business
# from business import business



db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

app.register_blueprint(business)

createdDate =  datetime.now()
modifiedDate =  datetime.now()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @app.route('/')
# def homePage():
#     return render_template("home.html")
def roleAssignedToUser():
    allRoles = System_Authorization.query.all()
    rolesAssignedToUser = ''
    loggedInUser = current_user.id
    for r in allRoles:
        role = r.Role
        users = r.Users
        if any(str(loggedInUser) in s for s in r.Users):

        # if loggedInUser in r.Users:
            rolesAssignedToUser = role
    return  rolesAssignedToUser

@app.route('/')
def homePage():
    return render_template("login.html")


@app.route('/show_map')
def show_map():
    return send_file('/custdata.html')

@app.route('/showHSNEntry')
def showHSNEntry():
    return render_template('HSNEntryForm.html')



@app.route('/showCustomerEntry')
def showCustomerEntry():
    data = Customer_Type.query.all()
    return render_template('CustomerDetails.html',customerType=data)

@app.route('/showItemEntry')
def showItemEntry():
    data = HSN_Details.query.all()
    return render_template('ItemDetails.html',HsnData=data)

@app.route('/showInventoryEntry')
def showInventoryEntry():
    data = Item_Master.query.all()
    uom = Unit_Of_Measure.query.all()
    return render_template('InventoryDetails.html',itemCodes=data, uom = uom)

@app.route('/get_customer_info')
def get_customer_info():
    name = request.args.get('query', False)
    customer = {}
    if name:
        selected_customer = Customer_Details.query.filter(Customer_Details.Customer_Name.like('%'+name+'%')).all()
    return jsonify({'custidj': selected_customer[0].Customer_ID,'custnamej': selected_customer[0].Customer_Name,
                    'custemailj': selected_customer[0].Customer_Email,'custmobilej': selected_customer[0].Customer_Mobile_No,
                    'custaddressj': selected_customer[0].Customer_Address})

@app.route('/login')
# @login_required
def login():
    return render_template("login.html")

@app.route('/changePassword')
@login_required
def changePassword():
    return render_template("forceChngpassword.html")

@app.route('/goToSearchCustomersPage')
@login_required
def goToSearchCustomersPage():
    return render_template("ViewCustomers.html")

@app.route('/signupForm')
def signupForm():
    return render_template("signup.html")

@app.route('/goToForgotPage')
# @login_required
def goToForgotPage():
    return render_template("forgotpassword.html")

@app.route('/profile')
@login_required
def profile():
    print('roleAssigned-----------------')
    test = current_user.id
    role = roleAssigned(test)
    app.jinja_env.globals['acs'] = role
    return render_template("profile.html",role = role,name=current_user.firstname+" "+current_user.lastname)

@app.route('/goToadminPage')
@login_required
def goToadminPage():
    return render_template("admin.html",name=current_user.id)

@app.route('/goToDisplayPaymentPage')
@login_required
def goToDisplayPaymentPage():
    return render_template("DisplayPayments.html",name=current_user.id)

@app.route('/goToCockpitPage')
@login_required
def goToCockpitPage():
    return render_template("cockpit.html",name=current_user.id)

@app.route('/goToPurchaseOrderPage')
@login_required
def goToPurchaseOrderPage():

    data = Item_Master.query.all()
    uom = Unit_Of_Measure.query.all()
    return render_template("PurchaseRequest.html",itemCodes=data, uom = uom)

@app.route('/goToSalesOrderPage')
@login_required
def goToSalesOrderPage():
    data = Item_Master.query\
    .join(Inventory, Item_Master.Item_Code==Inventory.Item_Code)\
    .join(HSN_Details, Item_Master.HSN_Code==HSN_Details.HSN_Code)\
    .add_columns(Item_Master.Item_Code, Item_Master.HSN_Code,Item_Master.Item_Description, Item_Master.Rate,
    Item_Master.Created_Date,Inventory.Item_Code,HSN_Details.HSN_Code, HSN_Details.HSN_Percentage )\
    .all()
    # data = Item_Master.query.all()
    uom = Unit_Of_Measure.query.all()
    return render_template("SalesOrder.html",itemCodes=data, uom = uom)

@app.route('/goToPaymentsReceivedPage')
@login_required
def goToPaymentsReceivedPage():
    return render_template("PaymentsRecvd.html",name=current_user.id)

@app.route('/goToExpensePage')
@login_required
def goToExpensePage():
    return render_template("Expense.html",name=current_user.id)

@app.route('/goToClientDetailPage')
@login_required
def goToClientDetailPage():
    return render_template("clientdetailMain.html",name=current_user.id)

@app.route('/goToMasterProfilePage')
@login_required
def goToMasterProfilePage():
    return render_template("masterprofile.html")

@app.route('/resetPassword',methods=['POST'])
def resetPassword():
    email   = request.form.get('email')
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    print(email)
    print(user)
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        user.password= generate_password_hash('xyz1234', method='sha256')
        user.firstTimeLogin = True
        user.Modified_By= 'System'
        user.Modified_Date = datetime.now()
        db.session.commit()
        return redirect(url_for('login'))
    else:
        flash('Email address does not exists')
        return render_template("forgotpassword.html")

@app.route('/setNewLoginPassword',methods=['POST'])
def setNewLoginPassword():
    userid   = request.form.get('loginUserID')
    password = request.form.get('password')

    user = User.query.filter_by(id=int(userid)).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        user.password= generate_password_hash(password, method='sha256')
        user.firstTimeLogin = False
        user.Modified_By= 'System'
        user.Modified_Date = datetime.now()
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        flash('Email address does not exists')
        return render_template("login.html")



@app.route('/signup_post',methods=['POST'])
def signup_post():
    email   = request.form.get('email')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    username = request.form.get('username')
    password = request.form.get('password')
    firstTimeLogin = False
    createdBy   = 'System'
    modifiedBy   = 'System'
    createdDate =  datetime.now()
    modifiedDate =  datetime.now()
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    uniqueUserName = User.query.filter_by(username=username).first()
    if uniqueUserName: # if a user is found, we want to redirect back to signup page so user can try again
        flash('User Name '+ username +' address already exists')
        return redirect(url_for('signupForm'))
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('signupForm'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, firstname=firstname, lastname=lastname, username=username, firstTimeLogin= firstTimeLogin, password=generate_password_hash(password, method='sha256'),Created_By=createdBy,Created_Date=createdDate,Modified_by=modifiedBy,Modified_Date=modifiedDate)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return render_template("login.html")



# @business.route('/login_post', methods=['POST'])
@app.route('/login_post', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    # user = User.query.filter_by(username=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if user doesn't exist or password is wrong, reload the page
    # print(current_user.name)
    if user and check_password_hash(user.password, password) and user.firstTimeLogin:
        print('ok')
        login_user(user, remember=remember)
        return redirect(url_for('changePassword'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('profile'))
    # return redirect(url_for('myShoppingList'))

@app.route('/logout')
def logout():
    logout_user()
    return render_template("login.html")

@app.route('/createSymbolEntry',methods=['POST'])
def success():
    if request.method == 'POST':
        symbolName   = request.form['symbol']
        symbolExtension = request.form['symbolext']
        comments ='Test comments'
        createdBy   = 'System'
        modifiedBy   = 'System'
        createdDate =  datetime.now()
        modifiedDate =  datetime.now()
        SymbolTableData =Trade_Symbols(Symbol_Description=symbolName,Symbol_Suffix=symbolExtension,Comments=comments,Created_By=createdBy,Created_Date=createdDate,Modified_by=modifiedBy,Modified_Date=modifiedDate)
        db.session.add(SymbolTableData)
        db.session.commit()
        return render_template("confirm.html",submitMessage ='Symbol '+ str(SymbolTableData.Symbol_Description)+'  is created with ID : '  +str(SymbolTableData.Symbol_Id))

@app.route('/createCustomer',methods=['POST'])
def createCustomer():
    if request.method == 'POST':
        symbolName   = request.form['name']
        symbolExtension = request.form['mobileno']
        comments ='Test comments'
        # createdBy   = 'System'
        # modifiedBy   = 'System'
        # createdDate =  datetime.now()
        # modifiedDate =  datetime.now()
        # SymbolTableData =Trade_Symbols(Symbol_Description=symbolName,Symbol_Suffix=symbolExtension,Comments=comments,Created_By=createdBy,Created_Date=createdDate,Modified_by=modifiedBy,Modified_Date=modifiedDate)
        # db.session.add(SymbolTableData)
        # db.session.commit()
        return render_template("confirm.html",submitMessage ='Symbol   is created with ID : ' )


@app.route('/getHSNCodePercentage')
@login_required
def getHSNCodePercentage():
    ItemId=request.args.get('ItemId', 0, type=str)
    hsnData = []
    cols = ['HSN_Code', 'HSN_Percentage']
    data = Item_Master.query.filter_by(Item_Code=ItemId).first()
    itemDesc = data.Item_Description
    if data:
        hd=data.HSN_Code
        data = HSN_Details.query.filter_by(HSN_Code=int(hd)).first()
        return jsonify({'code': str(data.HSN_Code),'percent': str(data.HSN_Percentage) , 'ItemDescription': itemDesc})
    else:
        return 'test'
    # return 'test'

@app.route('/getAllSymbols')
def getAllSymbols():
    allSymbols = []
    cols = ['Symbol_Id', 'Symbol_Description','Symbol_Suffix']
    data = Trade_Symbols.query.all()
    allSymbols = [{col: getattr(d, col) for col in cols} for d in data]
    return jsonify(tradeSymbols=allSymbols)

@app.route('/getOrderTypes')
@login_required
def getOrderTypes():
    typesOfTrades = []
    cols = ['Type_Id', 'Trade_Type_Description']
    data = Trade_Type.query.all()
    typesOfTrades = [{col: getattr(d, col) for col in cols} for d in data]
    return jsonify(typesOfOrders=typesOfTrades)

@app.route('/populateOrderTypes')
@login_required
def populateOrderTypes():
    TypeID=request.args.get('mainTypeId', 0, type=str)
    cols = ['Order_Type_ID', 'Type_Id', 'Order_Description']
    data = Trade_Order_Type.query\
    .add_columns(Trade_Order_Type.Order_Type_ID, Trade_Order_Type.Type_Id,Trade_Order_Type.Order_Description)\
    .filter(Trade_Order_Type.Type_Id == int(TypeID)).order_by(Trade_Order_Type.Order_Type_ID.asc())
    # data = Customer.query.filter(Customer.name.ilike('%'+searchString+'%'))
    results = [{col: getattr(d, col) for col in cols} for d in data]
    allRecords = []

    for r in results:
            tmp_dict = {}
            tmp_dict['Order_Type_ID'] = r['Order_Type_ID']
            tmp_dict['Type_Id'] = r['Type_Id']
            tmp_dict['Order_Description'] = r['Order_Description']
            allRecords.append((tmp_dict))
    return jsonify(result= allRecords)



@app.route('/display_SubmitConfirm')
def display_SubmitConfirm():
    displayMessage = request.args.get('submitMessage')
    return render_template("confirm.html",submitMessage=displayMessage)

@app.route('/displayPurchaseRequest')
def displayPurchaseRequest():
    purchase_Requedt_Id = request.args.get('request_Id', False)
    cols = ['Purchase_Req_Id', 'Customer_Id', 'Item_Code', 'HSN_Code',\
         'Units_Of_Measurement','HSN_Percentage','Rate','Quantity',\
         'Item_Description','Unit_Description', 'Customer_Name',\
         'Created_Date']
    data = Purchase_Master.query.filter(Purchase_Master.Purchase_Req_Id==purchase_Requedt_Id)\
    .join(Customer_Details, Purchase_Master.Customer_Id==Customer_Details.Customer_ID)\
    .join(Purchase_Detail, Purchase_Master.Purchase_Req_Id==Purchase_Detail.Purchase_Req_Id)\
    .join(Item_Master, Purchase_Detail.Item_Code==Item_Master.Item_Code)\
    .join(HSN_Details, Purchase_Detail.HSN_Code==HSN_Details.HSN_Code)\
    .join(Unit_Of_Measure, Purchase_Detail.Units_Of_Measurement==Unit_Of_Measure.Unit_Id)\
    .add_columns(Purchase_Master.Purchase_Req_Id, Purchase_Master.Customer_Id,Purchase_Master.Created_Date,Purchase_Master.Commission,
    Purchase_Master.Comments,Purchase_Detail.Purchase_Req_Id,Purchase_Detail.Item_Code,Purchase_Detail.HSN_Code,
    Purchase_Detail.Rate, Purchase_Detail.Quantity,Unit_Of_Measure.Unit_Id,HSN_Details.HSN_Code,HSN_Details.HSN_Percentage,
    Item_Master.Item_Code,Item_Master.HSN_Code,Item_Master.Item_Description,Purchase_Detail.Units_Of_Measurement,Unit_Of_Measure.Unit_Id,
    Unit_Of_Measure.Unit_Description,HSN_Details.HSN_Code,Customer_Details.Customer_ID,Customer_Details.Customer_Name)\
    .filter(Purchase_Detail.Purchase_Req_Id==purchase_Requedt_Id)\
    .all()
    result = [{col: getattr(d, col) for col in cols} for d in data]
    # print(data)
    # print(result)
    print(type(data))
    purchaseDetails =[]
    a=0

    totalAmount = 0
    for r in data:
        totalAmount = totalAmount + ((r.Rate * r.Quantity) + (r.HSN_Percentage/100 *(r.Rate * r.Quantity)))
        # totalAmount = totalAmount + (r.Rate * r.Quantity)
        if a == 0:
            tmp_dict = {}
            tmp_dict['Purchase_Req_Id'] =  r.Purchase_Req_Id
            tmp_dict['Customer_Id'] =  r.Customer_Id
            tmp_dict['Customer_Name'] = r.Customer_Name
            tmp_dict['Commission'] = r.Commission
            tmp_dict['Created_Date'] = r.Created_Date
            purchaseDetails.append((tmp_dict))

        a=a+1

    print('purchaseDetails--------------')
    print(purchaseDetails)
    print(type(purchaseDetails))
    Orders =[]
    for r in result:
            tmp_dict = {}
            tmp_dict['Item_Code'] = r['Item_Code']
            tmp_dict['Item_Description'] = r['Item_Description']
            tmp_dict['HSN_Percentage'] = str(r['HSN_Percentage'])
            tmp_dict['Rate'] =str (r['Rate'])
            Orders.append((tmp_dict))
    # return jsonify(Orders= Orders)


    return render_template("DisplayPurchaseReqByID.html",Orders=data, purchaseData = purchaseDetails, totalAmount = totalAmount)

@app.route('/displaySalesRequest')
def displaySalesRequest():
    purchase_Requedt_Id = request.args.get('request_Id', False)
    cols = ['Sales_Req_Id', 'Customer_Id', 'Item_Code', 'HSN_Code',\
         'Units_Of_Measurement','HSN_Percentage','Rate','Quantity',\
         'Item_Description','Unit_Description', 'Customer_Name',\
         'Created_Date']
    data = Sales_Master.query.filter(Sales_Master.Sales_Req_Id==purchase_Requedt_Id)\
    .join(Customer_Details, Sales_Master.Customer_Id==Customer_Details.Customer_ID)\
    .join(Sales_Detail, Sales_Master.Sales_Req_Id==Sales_Detail.Sales_Req_Id)\
    .join(Item_Master, Sales_Detail.Item_Code==Item_Master.Item_Code)\
    .join(HSN_Details, Sales_Detail.HSN_Code==HSN_Details.HSN_Code)\
    .join(Unit_Of_Measure, Sales_Detail.Units_Of_Measurement==Unit_Of_Measure.Unit_Id)\
    .add_columns(Sales_Master.Sales_Req_Id, Sales_Master.Customer_Id,Sales_Master.Created_Date,
    Sales_Master.Comments,Sales_Detail.Sales_Req_Id,Sales_Detail.Item_Code,Sales_Detail.HSN_Code,
    Sales_Detail.Rate, Sales_Detail.Quantity,Unit_Of_Measure.Unit_Id,HSN_Details.HSN_Code,HSN_Details.HSN_Percentage,
    Item_Master.Item_Code,Item_Master.HSN_Code,Item_Master.Item_Description,Sales_Detail.Units_Of_Measurement,Unit_Of_Measure.Unit_Id,
    Unit_Of_Measure.Unit_Description,HSN_Details.HSN_Code,Customer_Details.Customer_ID,Customer_Details.Customer_Name)\
    .filter(Sales_Detail.Sales_Req_Id==purchase_Requedt_Id)\
    .all()
    result = [{col: getattr(d, col) for col in cols} for d in data]
    # print(data)
    # print(result)
    print(type(data))
    salesDetails =[]
    a=0

    totalAmount = 0
    for r in data:
        totalAmount = totalAmount + ((r.Rate * r.Quantity) + (r.HSN_Percentage/100 *(r.Rate * r.Quantity)))

        if a == 0:
            tmp_dict = {}
            tmp_dict['Sales_Req_Id'] =  r.Sales_Req_Id
            tmp_dict['Customer_Id'] =  r.Customer_Id
            tmp_dict['Customer_Name'] = r.Customer_Name
            tmp_dict['Created_Date'] = r.Created_Date
            salesDetails.append((tmp_dict))

        a=a+1

    print('SalesDetails--------------')
    print(salesDetails)
    print(type(salesDetails))
    Orders =[]
    for r in result:

        tmp_dict = {}
        tmp_dict['Item_Code'] = r['Item_Code']
        tmp_dict['Item_Description'] = r['Item_Description']
        tmp_dict['HSN_Percentage'] = str(r['HSN_Percentage'])
        tmp_dict['Rate'] =str (r['Rate'])
        Orders.append((tmp_dict))
    # return jsonify(Orders= Orders)


    return render_template("DisplaySaleReqByID.html",Orders=data, saleData = salesDetails, totalAmount = totalAmount)

@app.route('/displayPaymentRequest')
def displayPaymentRequest():
    exp_Request_Id = request.args.get('request_Id', False)
    cols = ['Expense_Req_Id', 'Expense_Description', 'Amount', 'Created_Date']
    data = Expense_Master.query.filter(Expense_Master.Expense_Req_Id==exp_Request_Id)\
    .join(Expense_Detail, Expense_Master.Expense_Req_Id==Expense_Detail.Expense_Req_Id)\
    .add_columns(Expense_Master.Expense_Req_Id, Expense_Master.Created_Date,
    Expense_Detail.Expense_Description,Expense_Detail.Amount)\
    .filter(Expense_Detail.Expense_Req_Id==exp_Request_Id)\
    .all()
    result = [{col: getattr(d, col) for col in cols} for d in data]
    # print(data)
    # print(result)
    print(type(data))
    expenseMasterDetails =[]
    a=0

    totalAmount = 0
    for r in data:
        totalAmount = totalAmount + (r.Amount)
        if a == 0:
            tmp_dict = {}
            tmp_dict['Expense_Req_Id'] =  r.Expense_Req_Id
            tmp_dict['Created_Date'] = r.Created_Date
            expenseMasterDetails.append((tmp_dict))

        a=a+1

    print('expenseMasterDetails--------------')
    print(expenseMasterDetails)

    expDetails=[]
    for r in result:

        tmp_dict = {}
        tmp_dict['Expense_Description'] = r['Expense_Description']
        tmp_dict['Amount'] = str(r['Amount'])
        expDetails.append((tmp_dict))
    # return jsonify(Orders= Orders)


    return render_template("DisplayPaymentReqByID.html",Expense=data, masterData = expenseMasterDetails, totalAmount = totalAmount)



@app.route('/getSymbolInfo')
@login_required
def getSymbolInfo():
    symbol=request.args.get('symbol', 0, type=str)
    print('symbol===== '+symbol)
    userId= 235181
    userPassword= "b61d8c2S"
    serverName ="FidelisCapitalMarkets-Demo"


    tickData,ask=getSymbolDetails(symbol, userId, userPassword, serverName)
    print('tickData')
    print(str(tickData))
    print(str(ask))
    return jsonify({'bid': str(tickData),'ask': str(ask) })

@app.route('/', methods=['GET', 'POST'])
def getClientsName():
    cols = ['Client_Id', 'Client_Name']
    data = Client_Details.query.all()
    return render_template("viewmasterorders.html",orders=data)

@app.route('/getItemQuantity')
@login_required
def getItemQuantity():
    itemId=request.args.get('itemId')
    selected_Request = Inventory.query.filter_by(Item_Code=int(itemId))
    if selected_Request.count() >0:
        return jsonify({'Quantity': selected_Request[0].Quantity})
    else:
        return jsonify({'Quantity': '0'})





if __name__ =='__main__':
    app.run(debug=True)
