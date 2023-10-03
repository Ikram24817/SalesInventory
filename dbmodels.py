from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Numeric, String, DateTime, Date, Integer, Boolean, ForeignKey
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(500))
    firstname=db.Column(db.String(300))
    lastname = db.Column(db.String(300))
    username = db.Column(db.String(300),unique=True)
    firstTimeLogin = db.Column(Boolean)
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)

    def __init__(self, email, password,firstname,lastname,username,firstTimeLogin,Created_By,Created_Date,
                Modified_by,Modified_Date):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.firstTimeLogin = firstTimeLogin
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Attachments(db.Model):
    __tablename__="attachments"
    Attachment_Id = db.Column(db.Integer,primary_key=True)
    Attachment_Name=db.Column(db.String(300))
    File_Content=db.Column(db.LargeBinary)
    Purchase_Req_Id= db.Column(db.Integer,db.ForeignKey("purchase_master.Purchase_Req_Id"))
    Comments=db.Column(db.String(300))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)

    def __init__(self, Attachment_Name, File_Content, Purchase_Req_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Attachment_Name = Attachment_Name
        self.File_Content = File_Content
        self.Purchase_Req_Id = Purchase_Req_Id
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Sales_Attachments(db.Model):
    __tablename__="sales_attachments"
    Attachment_Id = db.Column(db.Integer,primary_key=True)
    Attachment_Name=db.Column(db.String(300))
    File_Content=db.Column(db.LargeBinary)
    Sales_Req_Id= db.Column(db.Integer,db.ForeignKey("sales_master.Sales_Req_Id"))
    Comments=db.Column(db.String(300))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)

    def __init__(self, Attachment_Name, File_Content, Sales_Req_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Attachment_Name = Attachment_Name
        self.File_Content = File_Content
        self.Sales_Req_Id = Sales_Req_Id
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Payment_Attachments(db.Model):
    __tablename__="payment_attachments"
    Attachment_Id = db.Column(db.Integer,primary_key=True)
    Attachment_Name=db.Column(db.String(300))
    File_Content=db.Column(db.LargeBinary)
    Payment_Id= db.Column(db.Integer,db.ForeignKey("payments_received.Payment_Req_Id"))
    Comments=db.Column(db.String(300))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)

    def __init__(self, Attachment_Name, File_Content, Payment_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Attachment_Name = Attachment_Name
        self.File_Content = File_Content
        self.Payment_Id = Payment_Id
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Expense_Attachments(db.Model):
    __tablename__="expense_attachments"
    Attachment_Id = db.Column(db.Integer,primary_key=True)
    Attachment_Name=db.Column(db.String(300))
    File_Content=db.Column(db.LargeBinary)
    Expense_Req_Id= db.Column(db.Integer,db.ForeignKey("expense_master.Expense_Req_Id"))
    Comments=db.Column(db.String(300))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)

    def __init__(self, Attachment_Name, File_Content, Expense_Req_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Attachment_Name = Attachment_Name
        self.File_Content = File_Content
        self.Expense_Req_Id = Expense_Req_Id
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class System_Authorization(db.Model):
    __tablename__="system_authorization"
    id = db.Column(db.Integer, primary_key=True)
    Role=db.Column(db.String(50))
    Users=db.Column(db.String(500))

    def __init__(self, Role, Users ):
        self.key=Role
        self.value = Users

class System_Settings(db.Model):
    __tablename__="system_settings"
    id = db.Column(db.Integer, primary_key=True)
    key=db.Column(db.String(50))
    value=db.Column(db.String(300))

    def __init__(self, key, value ):
        self.key=key
        self.value = value

class System_Readings(db.Model):
    __tablename__="system_readings"
    id = db.Column(db.Integer, primary_key=True)
    key=db.Column(db.String(50))
    value=db.Column(db.String(300))

    def __init__(self, key, value ):
        self.key=key
        self.value = value


class HSN_Details(db.Model):
    __tablename__="hsn_details"
    HSN_Code = db.Column(Integer, primary_key=True)
    HSN_Description=db.Column(db.String(300))
    HSN_Percentage=db.Column(Numeric(15,2))
    Comments=db.Column(db.String(300))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, HSN_Description, HSN_Percentage, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.HSN_Description=HSN_Description
        self.HSN_Percentage = HSN_Percentage
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Customer_Details(db.Model):
    __tablename__="customer_details"
    Customer_ID=db.Column(db.Integer, primary_key=True)
    Customer_Type_Id = db.Column(db.Integer,db.ForeignKey("customer_type.Cust_Type_Id"))
    Customer_Name=db.Column(db.String(300))
    Customer_Email=db.Column(db.String(300), unique=True)
    Customer_Mobile_No=db.Column(db.String(300))
    Customer_GST_No=db.Column(db.String(300))
    Customer_Bank_Name=db.Column(db.String(300))
    Customer_Bank_Branch=db.Column(db.String(300))
    Customer_Account_No=db.Column(db.String(300))
    Customer_IFSC_Code=db.Column(db.String(300))
    Customer_Address=db.Column(db.String(400))
    Comments=db.Column(db.String(500))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)

    def __init__(self, Customer_Type_Id, Customer_Name, Customer_Email, Customer_Mobile_No, Customer_Address, Customer_GST_No, Customer_Bank_Name,
    Customer_Bank_Branch, Customer_Account_No, Customer_IFSC_Code, Comments, Created_By,Created_Date,Modified_by,Modified_Date):
        self.Customer_Type_Id=Customer_Type_Id
        self.Customer_Name=Customer_Name
        self.Customer_Email = Customer_Email
        self.Customer_Mobile_No = Customer_Mobile_No
        self.Customer_Address = Customer_Address
        self.Customer_GST_No = Customer_GST_No
        self.Customer_Bank_Name = Customer_Bank_Name
        self.Customer_Bank_Branch = Customer_Bank_Branch
        self.Customer_Account_No = Customer_Account_No
        self.Customer_IFSC_Code = Customer_IFSC_Code
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Customer_Type(db.Model):
    __tablename__="customer_type"
    Cust_Type_Id = db.Column(db.Integer, primary_key=True)
    Type_Description=db.Column(db.String(100))
    Comments=db.Column(db.String(300))

    def __init__(self, Type_Description, Comments):
        self.Status_Description=Status_Description
        self.Comments = Comments


class Item_Master(db.Model):
    __tablename__="item_master"
    Item_Code = db.Column(Integer, primary_key=True)
    HSN_Code = db.Column(db.Integer,db.ForeignKey("hsn_details.HSN_Code"))
    Item_Description=db.Column(db.String(300))
    Rate=db.Column(Numeric(15,2))
    Quantity=db.Column(db.Integer)
    Comments=db.Column(db.String(300))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, HSN_Code, Item_Description, Rate, Quantity, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.HSN_Code=HSN_Code
        self.Item_Description=Item_Description
        self.Rate = Rate
        self.Quantity = Quantity
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Inventory(db.Model):
    __tablename__="inventory"
    Inventory_Code = db.Column(Integer, primary_key=True)
    HSN_Code = db.Column(db.Integer,db.ForeignKey("hsn_details.HSN_Code"))
    Item_Code = db.Column(db.Integer,db.ForeignKey("item_master.Item_Code"),unique=True)
    Rate=db.Column(Numeric(15,2))
    Quantity=db.Column(db.Integer)
    Units_Of_Measurement =  db.Column(db.Integer,db.ForeignKey("Unit_Of_Measure.Unit_Id"))
    Item_Status_Id=db.Column(db.Integer,db.ForeignKey("inventory_status.Status_Id"))
    Comments=db.Column(db.String(500))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, HSN_Code, Item_Code, Rate, Quantity, Units_Of_Measurement, Item_Status_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.HSN_Code=HSN_Code
        self.Item_Code=Item_Code
        self.Rate = Rate
        self.Quantity = Quantity
        self.Units_Of_Measurement = Units_Of_Measurement
        self.Item_Status_Id = Item_Status_Id
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Inventory_Detail(db.Model):
    __tablename__="inventory_details"
    Inventory_Det_Code = db.Column(Integer, primary_key=True)
    Inventory_Code = db.Column(db.Integer,db.ForeignKey("inventory.Inventory_Code"))
    HSN_Code = db.Column(db.Integer,db.ForeignKey("hsn_details.HSN_Code"))
    Item_Code = db.Column(db.Integer,db.ForeignKey("item_master.Item_Code"))
    Rate=db.Column(Numeric(15,2))
    Quantity=db.Column(db.Integer)
    Units_Of_Measurement =  db.Column(db.Integer,db.ForeignKey("Unit_Of_Measure.Unit_Id"))
    Item_Status_Id=db.Column(db.Integer,db.ForeignKey("inventory_status.Status_Id"))
    Comments=db.Column(db.String(500))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, Inventory_Code,HSN_Code, Item_Code, Rate, Quantity, Units_Of_Measurement, Item_Status_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Inventory_Code=Inventory_Code
        self.HSN_Code=HSN_Code
        self.Item_Code=Item_Code
        self.Rate = Rate
        self.Quantity = Quantity
        self.Units_Of_Measurement = Units_Of_Measurement
        self.Item_Status_Id = Item_Status_Id
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date



class Purchase_Master(db.Model):
    __tablename__="purchase_master"
    Purchase_Req_Id = db.Column(Integer, primary_key=True)
    Invoice_No= db.Column(db.String(100), unique=True)
    Customer_Id=db.Column(db.Integer,db.ForeignKey("customer_details.Customer_ID"))
    Commission=db.Column(Numeric(5,2))
    # Attachment_Id=db.Column(db.Integer,db.ForeignKey("attachments.Attachment_Id"))
    Request_Status_Id=db.Column(db.Integer,db.ForeignKey("request_status.Status_Id"))
    Comments=db.Column(db.String(500))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, Invoice_No, Customer_Id, Commission, Request_Status_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Invoice_No=Invoice_No
        self.Customer_Id=Customer_Id
        self.Commission=Commission
        self.Request_Status_Id = Request_Status_Id
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Purchase_Detail(db.Model):
    __tablename__="purchase_detail"
    Purchase_Det_Id = db.Column(Integer, primary_key=True)
    Purchase_Req_Id= db.Column(db.Integer,db.ForeignKey("purchase_master.Purchase_Req_Id"))
    Item_Code= db.Column(db.Integer,db.ForeignKey("item_master.Item_Code"))
    HSN_Code = db.Column(db.Integer,db.ForeignKey("hsn_details.HSN_Code"))
    Quantity=db.Column(db.Integer)
    Rate=db.Column(Numeric(15,2))
    Total=db.Column(Numeric(15,2))
    GST_Percent=db.Column(Numeric(10,2))
    Units_Of_Measurement =  db.Column(db.Integer,db.ForeignKey("Unit_Of_Measure.Unit_Id"))
    Comments=db.Column(db.String(500))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, Purchase_Req_Id,Item_Code, HSN_Code, Quantity, Rate, Total, GST_Percent, Units_Of_Measurement,
      Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Purchase_Req_Id=Purchase_Req_Id
        self.Item_Code=Item_Code
        self.HSN_Code=HSN_Code
        self.Quantity=Quantity
        self.Rate = Rate
        self.Total = Total
        self.GST_Percent = GST_Percent
        self.Units_Of_Measurement = Units_Of_Measurement
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Sales_Master(db.Model):
    __tablename__="sales_master"
    Sales_Req_Id = db.Column(Integer, primary_key=True)
    Customer_Id=db.Column(db.Integer,db.ForeignKey("customer_details.Customer_ID"))
    Request_Status_Id=db.Column(db.Integer,db.ForeignKey("request_status.Status_Id"))
    Comments=db.Column(db.String(500))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, Customer_Id, Request_Status_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Customer_Id=Customer_Id
        self.Request_Status_Id=Request_Status_Id
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Sales_Detail(db.Model):
    __tablename__="sales_detail"
    Sales_Det_Id = db.Column(Integer, primary_key=True)
    Sales_Req_Id= db.Column(db.Integer,db.ForeignKey("sales_master.Sales_Req_Id"))
    Item_Code= db.Column(db.Integer,db.ForeignKey("item_master.Item_Code"))
    HSN_Code = db.Column(db.Integer,db.ForeignKey("hsn_details.HSN_Code"))
    Quantity=db.Column(db.Integer)
    Rate=db.Column(Numeric(15,2))
    Total=db.Column(Numeric(15,2))
    GST_Percent=db.Column(Numeric(10,2))
    Units_Of_Measurement =  db.Column(db.Integer,db.ForeignKey("Unit_Of_Measure.Unit_Id"))
    Comments=db.Column(db.String(500))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, Sales_Req_Id, Item_Code, HSN_Code, Quantity, Rate, Total, GST_Percent, Units_Of_Measurement,
      Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Sales_Req_Id=Sales_Req_Id
        self.Item_Code=Item_Code
        self.HSN_Code=HSN_Code
        self.Quantity=Quantity
        self.Rate = Rate
        self.Total = Total
        self.GST_Percent = GST_Percent
        self.Units_Of_Measurement = Units_Of_Measurement
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Payments_Received(db.Model):
    __tablename__="payments_received"
    Payment_Req_Id = db.Column(Integer, primary_key=True)
    Customer_Id=db.Column(db.Integer,db.ForeignKey("customer_details.Customer_ID"))
    Amount=db.Column(Numeric(15,2))
    Payment_Details= db.Column(db.String(500))
    Request_Status_Id=db.Column(db.Integer,db.ForeignKey("request_status.Status_Id"))
    Comments=db.Column(db.String(500))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, Customer_Id, Amount, Payment_Details, Request_Status_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Customer_Id=Customer_Id
        self.Amount=Amount
        self.Payment_Details=Payment_Details
        self.Request_Status_Id=Request_Status_Id
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Payments_Given(db.Model):
    __tablename__="payments_given"
    Payment_Req_Id = db.Column(Integer, primary_key=True)
    Customer_Id=db.Column(db.Integer,db.ForeignKey("customer_details.Customer_ID"))
    Amount=db.Column(Numeric(15,2))
    Payment_Details= db.Column(db.String(500))
    Attachment_Id=db.Column(db.Integer,db.ForeignKey("attachments.Attachment_Id"))
    Request_Status_Id=db.Column(db.Integer,db.ForeignKey("request_status.Status_Id"))
    Comments=db.Column(db.String(500))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, Customer_Id, Payment_Details, Attachment_Id, Request_Status_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Customer_Id=Customer_Id
        self.Payment_Details=Payment_Details
        self.Attachment_Id=Attachment_Id
        self.Request_Status_Id=Request_Status_Id
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Invested_Capital(db.Model):
    __tablename__="invested_capital"
    Invest_Req_Id = db.Column(Integer, primary_key=True)
    Amount=db.Column(Numeric(15,2))
    Investment_Details= db.Column(db.String(500))
    Attachment_Id=db.Column(db.Integer,db.ForeignKey("attachments.Attachment_Id"))
    Request_Status_Id=db.Column(db.Integer,db.ForeignKey("request_status.Status_Id"))
    Comments=db.Column(db.String(500))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, Customer_Id, Payment_Details, Attachment_Id, Request_Status_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Customer_Id=Customer_Id
        self.Payment_Details=Payment_Details
        self.Attachment_Id=Attachment_Id
        self.Request_Status_Id=Request_Status_Id
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Expense_Master(db.Model):
    __tablename__="expense_master"
    Expense_Req_Id = db.Column(Integer, primary_key=True)
    Request_Status_Id=db.Column(db.Integer,db.ForeignKey("request_status.Status_Id"))
    Comments=db.Column(db.String(500))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, Request_Status_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date):

        self.Request_Status_Id=Request_Status_Id
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Expense_Detail(db.Model):
    __tablename__="expense_detail"
    Expense_Det_Id = db.Column(Integer, primary_key=True)
    Expense_Req_Id= db.Column(db.Integer,db.ForeignKey("expense_master.Expense_Req_Id"))
    Expense_Description=db.Column(db.String(500))
    Amount=db.Column(Numeric(15,2))
    Comments=db.Column(db.String(500))
    Created_By=db.Column(db.String(300))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)


    def __init__(self, Expense_Req_Id, Expense_Description, Amount,
      Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Expense_Req_Id=Expense_Req_Id
        self.Expense_Description=Expense_Description
        self.Amount = Amount
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date


class Request_Status(db.Model):
    __tablename__="request_status"
    Status_Id = db.Column(db.Integer, primary_key=True)
    Status_Description=db.Column(db.String(100))
    Comments=db.Column(db.String(300))

    def __init__(self, Status_Description, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Status_Description=Status_Description
        self.Comments = Comments


class Inventory_Status(db.Model):
    __tablename__="inventory_status"
    Status_Id = db.Column(db.Integer, primary_key=True)
    Status_Description=db.Column(db.String(100))
    Comments=db.Column(db.String(300))
    Created_By=db.Column(db.String(50))
    Created_Date=db.Column(db.DateTime)
    Modified_by=db.Column(db.String(300))
    Modified_Date=db.Column(db.DateTime)

    def __init__(self, Status_Description, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Status_Description=Status_Description
        self.Comments = Comments
        self.Created_By = Created_By
        self.Created_Date = Created_Date
        self.Modified_by = Modified_by
        self.Modified_Date = Modified_Date

class Unit_Of_Measure(db.Model):
    __tablename__="Unit_Of_Measure"
    Unit_Id = db.Column(db.Integer, primary_key=True)
    Unit_Description=db.Column(db.String(100))
    Comments=db.Column(db.String(300))

    def __init__(self, Unit_Description, Comments, Created_By, Created_Date, Modified_by, Modified_Date):
        self.Unit_Description=Unit_Description
        self.Comments = Comments
