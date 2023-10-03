from flask import Flask,render_template,request,jsonify,make_response,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import json
from sqlalchemy import Date, cast, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import operators, extract
from flask import Blueprint
from flask_login import login_required,current_user,LoginManager,UserMixin,login_user, logout_user, login_required
from datetime import datetime
from datetime import date

from dbmodels import *
from addDataInDB import *

a=0

business = Blueprint('business', __name__)



@business.route('/goToViewMasterOrdersPage')
@login_required
def goToViewMasterOrdersPage():
    data = Master_Order_Detail.query.filter(Master_Order_Detail.Master_Id == int(current_user.id))
    return render_template("viewmasterorders.html",orders=data)

@business.route('/goToViewModifyOrdersPage')
@login_required
def goToViewModifyOrdersPage():
    data = Master_Order_Detail.query.filter(Master_Order_Detail.Master_Id == int(current_user.id))
    return render_template("modifyorder.html",orders=data)

@business.route('/goToViewMasterProfileInfo')
@login_required
def goToViewMasterProfileInfo():
    data = Master_Trade_Account.query.filter(Master_Trade_Account.Master_Id == (current_user.id))
    return render_template("viewmasterProfile.html",masters=data)

@business.route('/goToViewClientsOrdersPage')
@login_required
def goToViewClientsOrdersPage():
    data = Slave_Order_Detail.query.filter(Slave_Order_Detail.Master_Id == int(current_user.id))
    return render_template("viewclientsorders.html",orders=data)

@business.route('/goToReportsPage')
@login_required
def goToReportsPage():
    month = func.to_char(Expense_Detail.Created_Date, "FMMonth")
    allMonths=db.session.query(extract('month', Expense_Detail.Created_Date).label('mon'),extract('year', Expense_Detail.Created_Date).label('year'),func.to_char(Expense_Detail.Created_Date, "FMMonth").label('Month'))

    months =[]
    years =[]
    monthNum =[]
    a=0
    mnth=''

    for r in allMonths:
        yr = str(r.year)
        sep = '.'
        stripedYear = yr.split(sep, 1)[0]
        years.append(stripedYear)

    #     if a==0:
    #         mnth = r.Month
    #         y=r.year
    #     months.append( r.Month)
    #     monthNum.append( r.mon)
    # a=a+1

    alist = list(set(years))
    # print(alist)
    allYears =[]
    for a in alist:
        tmp_dict = {}
        tmp_dict['Years'] = a
        allYears.append((tmp_dict))

    # c=db.session.query(func.sum(Expense_Detail.Amount).label('total'))\
    # .filter(func.to_char(Expense_Detail.Created_Date, "FMMonth") == mnth)\
    # .filter(extract('year', Expense_Detail.Created_Date) == y)


    return render_template("Reports.html",months = list(set(allMonths)), years =  allYears )

@business.route('/getReportDataByYearandMonth')
@login_required
def getReportDataByYearandMonth():
    year=request.args.get('year', 0, type=str)
    month=request.args.get('month', 0, type=str)

    data=db.session.query(func.sum(Expense_Detail.Amount).label('total'))\
    .filter(func.to_char(Expense_Detail.Created_Date, "FMMonth") == month)\
    .filter(extract('year', Expense_Detail.Created_Date) == year)
    amount = 0
    for d in data:
        amount = amount + d.total
    if data:
        return jsonify({'Amount': str(amount)})
    else:
        return 'test'

@business.route('/goToDisplayExpensePage')
@login_required
def goToDisplayExpensePage():
    # data = Item_Master.query.all()
    allExpenses = db.session.query(Expense_Master.Created_Date,Expense_Detail.Expense_Req_Id, func.sum(Expense_Detail.Amount).label('total'))\
    .group_by(Expense_Detail.Expense_Req_Id).group_by(Expense_Master.Expense_Req_Id)\
    .join(Expense_Master, Expense_Detail.Expense_Req_Id==Expense_Master.Expense_Req_Id)\
    .order_by(Expense_Detail.Expense_Req_Id.desc()).all()
    print(type(allExpenses))
    month = func.date_trunc('month', Expense_Master.Created_Date)
    allExpenses1 = db.session.query(func.date_trunc('month', Expense_Master.Created_Date).label('month'), func.sum(Expense_Detail.Amount).label('total'))\
    .join(Expense_Master, Expense_Detail.Expense_Req_Id==Expense_Master.Expense_Req_Id)\
    .group_by(month).all()
    # print(allExpenses1)

    b = db.session.query(extract('month', Expense_Master.Created_Date).label('month'))
    a = db.session.query(func.to_char(Expense_Master.Created_Date, "FMMonth").label('month'))
    c=db.session.query(func.sum(Expense_Detail.Amount).label('total')).filter(func.to_char(Expense_Detail.Created_Date, "FMMonth") == "February")
    print(a)
    for s in c:
        print(s.total)


    # AmendObj = db.session.query(func.sum(Loan_Amendment.Amount).label('Amount'),
    #                         month).\
    # group_by(month).\
    # first()

    return render_template("ViewExpenses.html",expenses=allExpenses)

@business.route('/goToViewAllCustomers')
@login_required
def goToViewAllCustomers():
    data = Customer_Details.query.all()
    return render_template("ViewAllCustomers.html",customers=data)

@business.route('/goToViewAllPayments')
@login_required
def goToViewAllPayments():
    data = Payments_Received.query.all()
    data = Payments_Received.query\
    .join(Customer_Details, Payments_Received.Customer_Id==Customer_Details.Customer_ID)\
    .add_columns(Payments_Received.Payment_Req_Id, Payments_Received.Amount,Payments_Received.Payment_Details,
    Payments_Received.Request_Status_Id,Payments_Received.Created_Date,Customer_Details.Customer_ID,Customer_Details.Customer_Name
    ,Customer_Details.Customer_Address)\
    .all()
    return render_template("ViewAllPayments.html",payments=data)


@business.route('/goToViewAllMasterItems')
@login_required
def goToViewAllMasterItems():
    # data = Item_Master.query.all()
    data = Item_Master.query\
    .join(HSN_Details, Item_Master.HSN_Code==HSN_Details.HSN_Code)\
    .add_columns(Item_Master.Item_Code, Item_Master.HSN_Code,Item_Master.Item_Description, Item_Master.Rate,Item_Master.Created_Date,HSN_Details.HSN_Code, HSN_Details.HSN_Percentage )\
    .all()
    return render_template("ViewAllMItems.html",Items=data)


@business.route('/goToViewInventoryItems')
@login_required
def goToViewInventoryItems():
    # data = Item_Master.query.all()
    data = Inventory.query\
    .join(Item_Master, Inventory.Item_Code==Item_Master.Item_Code)\
    .join(HSN_Details, Inventory.HSN_Code==HSN_Details.HSN_Code)\
    .join(Unit_Of_Measure, Inventory.Units_Of_Measurement==Unit_Of_Measure.Unit_Id)\
    .join(Inventory_Status, Inventory.Item_Status_Id==Inventory_Status.Status_Id)\
    .add_columns(Inventory.Item_Code, Inventory.HSN_Code,Inventory.Quantity, Inventory.Created_Date,
    Inventory.Units_Of_Measurement,Unit_Of_Measure.Unit_Id,Inventory.Item_Status_Id,Inventory_Status.Status_Id,
    Unit_Of_Measure.Unit_Description,Inventory_Status.Status_Description,Inventory.Comments,
    Inventory.Rate,Item_Master.Item_Code,Item_Master.Item_Description,HSN_Details.HSN_Code, HSN_Details.HSN_Percentage )\
    .all()
    return render_template("ViewInventoryMItems.html",Items=data)

@business.route('/goToViewPurchaseOrders')
@login_required
def goToViewPurchaseOrders():
    # data = Item_Master.query.all()
    data = Purchase_Master.query\
    .join(Customer_Details, Purchase_Master.Customer_Id==Customer_Details.Customer_ID)\
    .add_columns(Purchase_Master.Purchase_Req_Id, Purchase_Master.Customer_Id,Purchase_Master.Created_Date,Purchase_Master.Comments,
    Customer_Details.Customer_ID,Customer_Details.Customer_Name)\
    .all()
    print(data)
    print(type(data))
    return render_template("ViewPurchaseOrder.html",Orders=data)

@business.route('/GetDetailsByPurReqID')
@login_required
def GetDetailsByPurReqID():
    purchase_Requedt_Id = request.args.get('query', False)
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
    .add_columns(Purchase_Master.Purchase_Req_Id, Purchase_Master.Customer_Id,Purchase_Master.Created_Date,Purchase_Master.Comments,
    Purchase_Detail.Purchase_Req_Id,Purchase_Detail.Item_Code,Purchase_Detail.HSN_Code,Purchase_Detail.Rate,
    Purchase_Detail.Quantity,Unit_Of_Measure.Unit_Id,HSN_Details.HSN_Code,HSN_Details.HSN_Percentage,
    Item_Master.Item_Code,Item_Master.HSN_Code,Item_Master.Item_Description,Purchase_Detail.Units_Of_Measurement,Unit_Of_Measure.Unit_Id,
    Unit_Of_Measure.Unit_Description,HSN_Details.HSN_Code,Customer_Details.Customer_ID,Customer_Details.Customer_Name)\
    .filter(Purchase_Detail.Purchase_Req_Id==purchase_Requedt_Id)\
    .all()
    result = [{col: getattr(d, col) for col in cols} for d in data]
    # print(data)
    print(result)
    print('type(result)')
    # print(type(result))
    Orders =[]
    for r in result:
            tmp_dict = {}
            tmp_dict['Item_Code'] = r['Item_Code']
            tmp_dict['Item_Description'] = r['Item_Description']
            tmp_dict['HSN_Percentage'] = str(r['HSN_Percentage'])
            tmp_dict['Rate'] =str (r['Rate'])
            Orders.append((tmp_dict))
    print(type(Orders))
    print('type(Orders)')
    return jsonify(Orders= Orders)
    # return Orders
    # return render_template("DisplayPurchaseReqByID.html",Orders=data)


@business.route('/GetDetailsBySalesReqID')
@login_required
def GetDetailsBySalesReqID():
    purchase_Request_Id = request.args.get('query', False)
    return jsonify(Orders= purchase_Request_Id)

@business.route('/GetExpenseByReqID')
@login_required
def GetExpenseByReqID():
    expense_Request_Id = request.args.get('query', False)
    return jsonify(Orders= expense_Request_Id)

@business.route('/goToViewSalesOrders')
@login_required
def goToViewSalesOrders():
    # data = Item_Master.query.all()
    data = Sales_Master.query\
    .join(Customer_Details, Sales_Master.Customer_Id==Customer_Details.Customer_ID)\
    .add_columns(Sales_Master.Sales_Req_Id, Sales_Master.Customer_Id,Sales_Master.Created_Date,Sales_Master.Comments,
    Customer_Details.Customer_ID,Customer_Details.Customer_Name)\
    .all()
    print(data)
    print(type(data))
    return render_template("ViewSalesOrder.html",Orders=data)




@business.route('/createMasterAccDetails')
@login_required
def createMasterAccDetails():
    try:
        message =''
        masteraccno   =request.args.get('masteraccno', 0, type=str)
        loginid =request.args.get('loginid', 0, type=str)
        passwrd =request.args.get('passwrd', 0, type=str)
        servername =request.args.get('servername', 0, type=str)
        brokername =request.args.get('brokername', 0, type=str)
        lotsize =request.args.get('lotsize', 0, type=str)
        equitycap =request.args.get('equitycap', 0, type=str)
        masterId =request.args.get('masterID', 0, type=str)
        active =request.args.get('active', 0, type=str)
        comments ='Master Details Created'
        createdBy   = masterId
        modifiedBy   = masterId
        createdDate =  datetime.now()
        modifiedDate =  datetime.now()
        if(masteraccno.strip() != '' and loginid.strip() != '' and passwrd.strip() != ''\
        and servername.strip() != '' and brokername.strip() != '' and lotsize.strip() != ''\
        and equitycap.strip() != ''
            ):
            masterDetailsData = Master_Trade_Account(masterId,masteraccno,loginid,passwrd,servername,brokername,
            lotsize,equitycap,True,comments,createdBy,createdDate,modifiedBy,modifiedDate)
            db.session.add(masterDetailsData)
            db.session.commit()
            message='Master Accounts Details Created with ID:  '+ str(masterDetailsData.Master_Trade_Id)
    except:
        message = 'Error in Creating Master Trade account in data base'
    finally:
        return jsonify({'result': message})
        db.session.close()



@business.route('/createCustomerDetails',methods=['POST'])
@login_required
def createClientDetails():
    try:
        message =''
        emailExists=''
        name   = request.form.get('name', 0, type=str)
        phno =request.form.get('phno', 0, type=str)
        email=request.form.get('email', 0, type=str)
        address=request.form.get('address', 0, type=str)
        bankname = request.form.get('bankname', 0, type=str)
        bankbranch = request.form.get('bankbranch', 0, type=str)
        accno = request.form.get('accno', 0, type=str)
        ifsccode =request.form.get('ifsccode', 0, type=str)
        gstno =request.form.get('gstno', 0, type=str)
        customerType =request.form.get('customerType', 0, type=str)
        # comments =request.form.get('comments', 0, type=str)
        comments = request.form["comments"]
        print(comments)
        # text = request.form.get("comments")
        #
        # # split the text to get each line in a list
        # # text2 = text.split('\n')
        # print(text)
        creatorId =request.form.get('loginUserID', 0, type=str)
        createdBy   = creatorId
        modifiedBy   = creatorId
        createdDate =  datetime.now()
        modifiedDate =  datetime.now()
        emailExists = Customer_Details.query.filter_by(Customer_Email=email).first()
        # print(emailExists)
        if emailExists:
            flash('Email address already exists')
            message='Email address already exists'
            return redirect(url_for('showCustomerEntry'))
        if not emailExists:
            customerDetailsData = Customer_Details(int(customerType),name, email, phno, address, gstno, bankname,
            bankbranch, accno, ifsccode, comments,createdBy,createdDate,modifiedBy,modifiedDate)
            db.session.add(customerDetailsData)
            db.session.commit()
            message='Customer Details Created with ID:  '+ str(customerDetailsData.Customer_ID)
    except Exception as ex:
        message = 'Error in Creating Customer Details in data base'
        print(ex)

    finally:
        # return jsonify({'result': message})
        if emailExists:
            flash('Email address already exists')
            message='Email address already exists'
            return redirect(url_for('showCustomerEntry'))
            db.session.close()
        else:
            return render_template("confirm.html",submitMessage =message)
            db.session.close()

@business.route('/searchCustomers')
def searchCustomers():
    searchString=request.args.get('customername', 0, type=str)
    cols = ['Customer_ID', 'Customer_Name', 'Customer_Email', 'Customer_Mobile_No', 'Customer_Address', 'Customer_Bank_Name','Customer_GST_No']
    data = Customer_Details.query\
    .add_columns(Customer_Details.Customer_ID, Customer_Details.Customer_Name,Customer_Details.Customer_Email, Customer_Details.Customer_Mobile_No, Customer_Details.Customer_Address, Customer_Details.Customer_Bank_Name,Customer_Details.Customer_GST_No)\
    .filter(Customer_Details.Customer_Name.ilike('%'+searchString+'%'))\
    .order_by(Customer_Details.Customer_ID.asc())
    result = [{col: getattr(d, col) for col in cols} for d in data]
    return jsonify(result=result)


@business.route('/createHSNData',methods=['POST'])
@login_required
def createHSNData():
    try:
        message =''
        hsndesc =request.form.get('hsndesc', 0, type=str)
        hsnPercent=request.form.get('hsnPercent', 0, type=str)
        comments =request.form.get('comments', 0, type=str)
        creatorId =request.form.get('loginUserID', 0, type=str)
        createdBy   = creatorId
        modifiedBy   = creatorId
        createdDate =  datetime.now()
        modifiedDate =  datetime.now()
        descExists = HSN_Details.query.filter_by(HSN_Description=hsndesc.strip()).first()
        print(descExists)
        if descExists:
            flash('HSN Item already exists')
            message='HSN Item address already exists'
            return redirect(url_for('showHSNEntry'))
        if not descExists:
            hsnDetailsData = HSN_Details(hsndesc,float(hsnPercent),
            comments,createdBy,createdDate,modifiedBy,modifiedDate)
            db.session.add(hsnDetailsData)
            db.session.commit()
            message='HSN Item Created with ID:  '+ str(hsnDetailsData.HSN_Code)
    except Exception as ex:
        message = 'Error in Creating HSN Item in data base'
        print(ex)

    finally:
        # return jsonify({'result': message})
        if descExists:
            flash('HSN Item already exists')
            message='HSN Item already exists'
            return redirect(url_for('showHSNEntry'))
            db.session.close()
        else:
            return render_template("confirm.html",submitMessage =message)
            db.session.close()

@business.route('/createItemsMasterData',methods=['POST'])
@login_required
def createItemsMasterData():
    try:
        message =''
        descExists=''
        hsncode =request.form.get('hsnDetails', 0, type=str)
        itemdesc=request.form.get('itemdesc', 0, type=str)
        comments =request.form.get('comments', 0, type=str)
        creatorId =request.form.get('loginUserID', 0, type=str)
        print(itemdesc)
        createdBy   = creatorId
        modifiedBy   = creatorId
        createdDate =  datetime.now()
        modifiedDate =  datetime.now()
        descExists = Item_Master.query.filter_by(Item_Description=itemdesc.strip()).first()
        print(descExists)
        if descExists:
            flash('HSN Item already exists')
            message='HSN Item address already exists'
            return redirect(url_for('showItemEntry'))
        if not descExists:
            Item_MasterData = Item_Master(int(hsncode),itemdesc,float('2'),2,
            comments,createdBy,createdDate,modifiedBy,modifiedDate)
            db.session.add(Item_MasterData)
            db.session.commit()
            message='Item Created with ID:  '+ str(Item_MasterData.Item_Code)
    except Exception as ex:
        message = 'Error in Creating Item in data base'
        print(ex)

    finally:
        # return jsonify({'result': message})
        if descExists:
            flash(' Item already exists')
            message='Item already exists'
            return redirect(url_for('showItemEntry'))
            db.session.close()
        else:
            return render_template("confirm.html",submitMessage =message)
            db.session.close()



@business.route('/tradelogic/business/createInventory')
@login_required
def createInventory():
    try:
        itemExists = ''
        message = ''
        selected_Request =''
        HSN_Code=request.args.get('hsncode', 0, type=str)
        Item_Code=request.args.get('itemCode', 0, type=str)
        Rate=request.args.get('rate', 0, type=str)
        Quantity=request.args.get('quantity', 0, type=str)
        Unit_Of_Measurement=request.args.get('uom', 0, type=str)
        Comments=request.args.get('comments', 0, type=str)
        creatorID =request.args.get('creatorID', 0, type=str)
        createdBy   = creatorID
        modifiedBy   = creatorID
        createdDate =  datetime.now()
        modifiedDate =  datetime.now()
        # print('XXXXXXXXXXXXXXX '+str(Unit_Of_Measurement))
        # print('YYYYYYYYYYYYYYY '+str(Item_Code)+' '+str(HSN_Code)+' '+str(Rate)+' '+str(Quantity)+' '+str(Unit_Of_Measurement)+' '+str(Comments)+' '+str(creatorID))
        selected_Request = Inventory.query.filter_by(Item_Code=int(Item_Code))
        if selected_Request.count() > 0:
            for req in selected_Request:
                req.Quantity= req.Quantity+int(Quantity)
                req.Comments= 'Stock Updated'
                req.Modified_By= creatorID
                req.Modified_Date = datetime.now()
                db.session.commit()
                message='Inventory Item Updated for item:  '+ str(Item_Code)

                InventoryDetailsData = Inventory_Detail(int(req.Inventory_Code),int(HSN_Code),int(Item_Code),
                float('2'),int(Quantity),int(Unit_Of_Measurement),int(3),Comments,createdBy,
                createdDate,modifiedBy,modifiedDate)
                db.session.add(InventoryDetailsData)
                db.session.commit()
        else:
            if (
                    HSN_Code.strip() != '' and Item_Code.strip() != '' and Rate.strip() != ''  and
                    Quantity.strip() != '' and Unit_Of_Measurement.strip() != ''
                ):

                print('XXXXXXXXXXXXXXX '+str(Unit_Of_Measurement))
                InventoryData = Inventory(int(HSN_Code),int(Item_Code),float('2'),int(Quantity),int(Unit_Of_Measurement),
                int(4),Comments,createdBy,createdDate,modifiedBy,modifiedDate)
                db.session.add(InventoryData)
                db.session.commit()

                InventoryDetailsData = Inventory_Detail(int(InventoryData.Inventory_Code),int(HSN_Code),int(Item_Code),
                float('2'),int(Quantity),int(Unit_Of_Measurement),int(4),Comments,createdBy,
                createdDate,modifiedBy,modifiedDate)
                db.session.add(InventoryDetailsData)
                db.session.commit()

                message='Inventory Item Created with ID:  '+ str(InventoryData.Inventory_Code)

    except Exception as ex:
        message = 'Error in Creating Inventory Item in data base'
        print(ex)
        db.session.close()

    finally:
        db.session.close()
        return jsonify({'result': message})

@business.route('/createPurchaseOrderFiles',methods=['POST'])
def attachFiles():
    # global attachmentID

    fileContent=request.files.get('file')


    ax=request.form.get('purchaseItemID')
    purchaseItemID = json.loads(json.dumps(request.form.get('purchaseItemID').split(',')))
    purchaseHsnID = json.loads(json.dumps(request.form.get('purchaseHsnID').split(',')))
    purchaseUom = json.loads(json.dumps(request.form.get('purchaseUom').split(',')))
    purchaseRate = json.loads(json.dumps(request.form.get('purchaseRate').split(',')))
    purchaseQty = json.loads(json.dumps(request.form.get('purchaseQty').split(',')))
    purchaseGstPercent = json.loads(json.dumps(request.form.get('purchaseGstPercent').split(',')))
    custid = request.form.get('custid')
    loginUserID = request.form.get('loginUserID')
    invoiceNo = request.form.get('invoiceno')
    commission = request.form.get('commission')
    comments = request.form.get('comments')
    # print(fileContent)
    # print(fileContent.filename)
    createdBy   = 'System'
    modifiedBy   = 'System'
    createdDate =  datetime.now()
    modifiedDate =  datetime.now()
    if not commission:
        commission = 0

    if (custid  and purchaseItemID and purchaseHsnID and purchaseUom and purchaseRate and purchaseQty and purchaseGstPercent):
        Purchase_MasterData = Purchase_Master(invoiceNo,Customer_Id=int(custid),Commission=commission,Request_Status_Id=int('1')
        , Comments=comments, Created_By=createdBy,
        Created_Date=createdDate,Modified_by=modifiedBy,Modified_Date=modifiedDate)
        db.session.add(Purchase_MasterData)
        db.session.commit()
        purchaseReq_Id = Purchase_MasterData.Purchase_Req_Id

        for (itemId,hsnId,uom,rate,qty,gstper) in zip(purchaseItemID, purchaseHsnID, purchaseUom, purchaseRate,purchaseQty,purchaseGstPercent):
            purchase_Request_Id   = purchaseReq_Id
            purItemId = itemId
            purhsnId = hsnId
            purUom = uom
            print('purUom '+str(purUom))
            purRate = rate
            purQty = qty
            purPercent = gstper
            createdBy   = loginUserID
            modifiedBy  = loginUserID
            createdDate =  datetime.now()
            modifiedDate =  datetime.now()
            purchaseDetailData =Purchase_Detail(purchase_Request_Id,purItemId,purhsnId,purQty,purRate,98,purPercent,int(purUom),
            'comments',createdBy,createdDate,modifiedBy,modifiedDate)
            db.session.add(purchaseDetailData)
            db.session.commit()
            selected_Request = Inventory.query.filter_by(Item_Code=int(purItemId))
            if selected_Request.count() > 0:
                for req in selected_Request:
                    req.Quantity= req.Quantity+int(purQty)
                    req.Comments= 'Stock Updated'
                    req.Modified_By= modifiedBy
                    req.Modified_Date = datetime.now()
                    db.session.commit()
                    # message='Inventory Item Updated for item:  '+ str(Item_Code)

                    InventoryDetailsData = Inventory_Detail(int(req.Inventory_Code),int(purhsnId),int(purItemId),
                    float('2'),int(purQty),int(purUom),int(5),'Purchase',createdBy,
                    createdDate,modifiedBy,modifiedDate)
                    db.session.add(InventoryDetailsData)
                    db.session.commit()

    if (fileContent ):
        fileName= fileContent.filename
        attachmentData = Attachments(fileName, request.files.get('file').read(), purchaseReq_Id, 'Purchase Request',createdBy,createdDate,modifiedBy,modifiedDate)
        db.session.add(attachmentData)
        db.session.commit()
        attachmentID= attachmentData.Attachment_Id
    return jsonify({'result': purchaseReq_Id})



@business.route('/createSalesOrder',methods=['POST'])
def createSalesOrder():
    # global attachmentID

    fileContent=request.files.get('file')
    saleItemID = json.loads(json.dumps(request.form.get('saleItemID').split(',')))
    saleHsnID = json.loads(json.dumps(request.form.get('saleHsnID').split(',')))
    saleUom = json.loads(json.dumps(request.form.get('saleUom').split(',')))
    saleRate = json.loads(json.dumps(request.form.get('saleRate').split(',')))
    saleQty = json.loads(json.dumps(request.form.get('saleQty').split(',')))
    saleGstPercent = json.loads(json.dumps(request.form.get('saleGstPercent').split(',')))
    custid = request.form.get('custid')
    loginUserID = request.form.get('loginUserID')
    comments = request.form.get('comments')
    # print(fileContent)
    # print(fileContent.filename)
    createdBy   = loginUserID
    modifiedBy   = loginUserID
    createdDate =  datetime.now()
    modifiedDate =  datetime.now()


    if (custid  and saleItemID and saleHsnID and saleUom and saleRate and saleQty and saleGstPercent):
        Sales_MasterData = Sales_Master(Customer_Id=int(custid), Request_Status_Id=int('2')
        , Comments=comments, Created_By=createdBy,
        Created_Date=createdDate,Modified_by=modifiedBy,Modified_Date=modifiedDate)
        db.session.add(Sales_MasterData)
        db.session.commit()
        salesReq_Id = Sales_MasterData.Sales_Req_Id


        for (itemId,hsnId,uom,rate,qty,gstper) in zip(saleItemID, saleHsnID, saleUom, saleRate,saleQty,saleGstPercent):
            totalSaleAmount = 0
            sales_Request_Id   = salesReq_Id
            sItemId = itemId
            shsnId = hsnId
            sUom = uom
            sRate = rate
            sQty = qty
            sPercent = gstper
            createdBy   = loginUserID
            modifiedBy  = loginUserID
            createdDate =  datetime.now()
            modifiedDate =  datetime.now()
            totalSaleAmount = totalSaleAmount + (int(sQty) * float(sRate)) + (float(sPercent)/100 * (int(sQty) * float(sRate)))
            Sales_DetailData =Sales_Detail(sales_Request_Id,sItemId,shsnId,sQty,sRate,totalSaleAmount,sPercent,sUom,
            'Sales',createdBy,createdDate,modifiedBy,modifiedDate)
            db.session.add(Sales_DetailData)
            db.session.commit()
            selected_Request = Inventory.query.filter_by(Item_Code=int(sItemId))
            if selected_Request.count() > 0:
                for req in selected_Request:
                    req.Quantity= req.Quantity - int(sQty)
                    req.Comments= 'Stock Updated'
                    req.Modified_By= modifiedBy
                    req.Modified_Date = datetime.now()
                    db.session.commit()
                    # message='Inventory Item Updated for item:  '+ str(Item_Code)

                    InventoryDetailsData = Inventory_Detail(int(req.Inventory_Code),int(shsnId),int(sItemId),
                    float('2'),int(sQty),int(sUom),int(6),'Sales',createdBy,
                    createdDate,modifiedBy,modifiedDate)
                    db.session.add(InventoryDetailsData)
                    db.session.commit()
            # else:
            #     addStockToInventory(shsnId,sItemId, '2',sQty,sUom,'4','Added from New ',Created_By,Created_Date,Modified_By,Modified_Date):
            #

    if (fileContent ):
        fileName= fileContent.filename
        salesAttachmentData = Sales_Attachments(fileName, request.files.get('file').read(), salesReq_Id, 'Sales Request',createdBy,createdDate,modifiedBy,modifiedDate)
        db.session.add(salesAttachmentData)
        db.session.commit()
        attachmentID= salesAttachmentData.Attachment_Id
    return jsonify({'result': salesReq_Id})

@business.route('/createPaymentRecieved',methods=['POST'])
def createPaymentRecieved():
    # global attachmentID

    fileContent=request.files.get('file')
    custid = request.form.get('custid')
    loginUserID = request.form.get('loginUserID')
    amount = request.form.get('amount')
    paymentDetails = request.form.get('paymentDetails')
    comments = request.form.get('comments')
    # print(fileContent)
    # print(fileContent.filename)
    createdBy   = loginUserID
    modifiedBy   = loginUserID
    createdDate =  datetime.now()
    modifiedDate =  datetime.now()


    if (custid  and amount):
        Payments_ReceivedData = Payments_Received(Customer_Id=int(custid),Amount =  amount,Request_Status_Id=int('3'),
        Payment_Details=paymentDetails, Comments=comments, Created_By=createdBy,
        Created_Date=createdDate,Modified_by=modifiedBy,Modified_Date=modifiedDate)
        db.session.add(Payments_ReceivedData)
        db.session.commit()
        paymentReq_Id = Payments_ReceivedData.Payment_Req_Id


    if (fileContent ):
        fileName= fileContent.filename
        paymentAttachmentData = Payment_Attachments(fileName, request.files.get('file').read(), paymentReq_Id, 'Payment Request',createdBy,createdDate,modifiedBy,modifiedDate)
        db.session.add(paymentAttachmentData)
        db.session.commit()
        attachmentID= paymentAttachmentData.Attachment_Id
    return jsonify({'result': paymentReq_Id})

@business.route('/createExpenseEntry',methods=['POST'])
def createExpenseEntry():
    # global attachmentID

    fileContent=request.files.get('file')
    expenseDescription = json.loads(json.dumps(request.form.get('expenseDescription').split(',')))
    expenseAmount = json.loads(json.dumps(request.form.get('expenseAmount').split(',')))
    loginUserID = request.form.get('loginUserID')
    comments = request.form.get('comments')
    createdBy   = loginUserID
    modifiedBy   = loginUserID
    createdDate =  datetime.now()
    modifiedDate =  datetime.now()


    if (comments  and expenseDescription and expenseAmount ):
        Expense_MasterData = Expense_Master(Request_Status_Id=int('4'), Comments=comments, Created_By=createdBy,
        Created_Date=createdDate,Modified_by=modifiedBy,Modified_Date=modifiedDate)
        db.session.add(Expense_MasterData)
        db.session.commit()
        expReq_Id = Expense_MasterData.Expense_Req_Id


        for (expenseDes,expAmount) in zip(expenseDescription, expenseAmount):
            totalSaleAmount = 0
            expDescriptionA   = expenseDes
            expAmountA = expAmount
            createdBy   = loginUserID
            modifiedBy  = loginUserID
            createdDate =  datetime.now()
            modifiedDate =  datetime.now()
            # totalSaleAmount = totalSaleAmount + (int(sQty) * float(sRate)) + (float(sPercent)/100 * (int(sQty) * float(sRate)))
            Expense_DetailData =Expense_Detail(expReq_Id,expDescriptionA,expAmountA,
            'Expense',createdBy,createdDate,modifiedBy,modifiedDate)
            db.session.add(Expense_DetailData)
            db.session.commit()


    if (fileContent ):
        fileName= fileContent.filename
        expenseAttachmentData = Expense_Attachments(fileName, request.files.get('file').read(), expReq_Id, 'Expense Entry',createdBy,createdDate,modifiedBy,modifiedDate)
        db.session.add(expenseAttachmentData)
        db.session.commit()
        attachmentID= expenseAttachmentData.Attachment_Id
    # return jsonify({'result': expReq_Id})
    return jsonify({'result': "expReq_Id"})


@business.route('/create_PurchaseOrder',methods=['POST'])
def create_PurchaseOrder():
    global attachmentID
    # details = request.args.get('sDetails')
    print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    result = []
    data = request.get_json()
    purchaseItemID = data['purchaseItemID'] #will give you array a
    purchaseHsnID = data['purchaseHsnID'] #will give you array b
    purchaseUom = data['purchaseUom'] #will give you array c
    purchaseRate = data['purchaseRate'] #will give you array d
    purchaseQty = data['purchaseQty'] #will give you array d
    purchaseGstPercent = data['purchaseGstPercent'] #will give you array e
    custid  = data['custid']
    loginUserID =  data['loginUserID']
    # file_data =  data['file_data']
    print('purchaseItemID SRRRRRRRRRRRRRRRRR  ARRAY ')
    print(purchaseItemID)
    print('custid = '+str(custid))

    # print(file_data)
    for ad in purchaseItemID:
        print(ad)
    newArray = [purchaseItemID, purchaseHsnID, purchaseUom, purchaseRate, purchaseGstPercent,custid,loginUserID]

    print(newArray)
    # custid              =   request.args.get('custid')
    # loginUserID         =   request.args.get('loginUserID')
    # purchaseItemID      =   json.loads(request.args.get('purchaseItemID'))
    # purchaseHsnID       =   json.loads(request.args.get('purchaseHsnID'))
    # purchaseUom         =   json.loads(request.args.get('purchaseUom'))
    # purchaseRate        =   json.loads(request.args.get('purchaseRate'))
    # purchaseQty         =   json.loads(request.args.get('purchaseQty'))
    # purchaseGstPercent  =   json.loads(request.args.get('purchaseGstPercent'))
    # file                =   request.args.files['fileinput'].read()
    # fileName            =   request.args.files['fileinput'].filename
    # print(purchaseItemID)
    createdBy   = loginUserID
    modifiedBy   = loginUserID
    createdDate =  datetime.now()
    modifiedDate =  datetime.now()
    createdBy   = loginUserID
    modifiedBy   = loginUserID
    createdDate =  datetime.now()
    modifiedDate =  datetime.now()



    if (custid  and purchaseItemID and purchaseHsnID and purchaseUom and purchaseRate and purchaseQty and purchaseGstPercent):
        # Invoice_No, Customer_Id, Attachment_Id, Request_Status_Id, Comments, Created_By, Created_Date, Modified_by, Modified_Date
        Purchase_MasterData = Purchase_Master(Invoice_No=int('106'),Customer_Id=int(custid),Attachment_Id = attachmentData.Attachment_Id,
        Request_Status_Id=int('1'), Comments="Comments", Created_By=createdBy,
        Created_Date=createdDate,Modified_by=modifiedBy,Modified_Date=modifiedDate)
        db.session.add(Purchase_MasterData)
        db.session.commit()
        purchaseReq_Id = Purchase_MasterData.Purchase_Req_Id

        for (itemId,hsnId,uom,rate,qty,gstper) in zip(purchaseItemID, purchaseHsnID, purchaseUom, purchaseRate,purchaseQty,purchaseGstPercent):
            purchase_Request_Id   = purchaseReq_Id
            purItemId = itemId
            purhsnId = hsnId
            purUom = uom
            print('purUom '+str(purUom))
            purRate = rate
            purQty = qty
            purPercent = gstper
            createdBy   = loginUserID
            modifiedBy  = loginUserID
            createdDate =  datetime.now()
            modifiedDate =  datetime.now()
            purchaseDetailData =Purchase_Detail(purchase_Request_Id,purItemId,purhsnId,purQty,purRate,98,purPercent,int(purUom),
            'comments',createdBy,createdDate,modifiedBy,modifiedDate)
            db.session.add(purchaseDetailData)
            db.session.commit()

    # return render_template("confirm.html",confirmMessage= 'Car Checkout created for Service Request ID :'+serviceRequest_id)
    return jsonify({'result': purchase_Request_Id})
    # return jsonify({'result': 'Car Checkout created for Service Request ID :'+serviceRequest_id})


@business.route('/getAllPaymentsByCustomerID')
def getAllPaymentsByCustomerID():
    customerId = request.args.get('customerId', False)
    salesOrderList = Sales_Master.query.filter_by(Customer_Id=int(customerId)).all()
    # paymentAmount = []
    paymentAmount=0
    payments = db.session.query(Payments_Received.Customer_Id, func.sum(Payments_Received.Amount).label('total')).group_by(Payments_Received.Customer_Id)\
    .filter_by(Customer_Id=int(customerId)).all()
    for r in payments:
        tmp_dict = {}
        tmp_dict['Total'] = str( r.total)
        paymentAmount = str( r.total)
    SalesInvoiceAmount = []
    nettTotal = 0
    for r in salesOrderList:
        ak = db.session.query(Sales_Detail.Sales_Req_Id, func.sum(Sales_Detail.Total).label('total')).group_by(Sales_Detail.Sales_Req_Id)\
        .filter_by(Sales_Req_Id=int(r.Sales_Req_Id)).all()
        for r in ak:
            tmp_dict = {}
            tmp_dict['Sales_Req_Id'] =  str(r.Sales_Req_Id)
            tmp_dict['Total'] = str( r.total)
            nettTotal = nettTotal + r.total
            SalesInvoiceAmount.append((tmp_dict))

    cols1 = ['Customer_ID', 'Customer_Name', 'Customer_Email', 'Customer_Mobile_No', 'Customer_Address', 'Customer_Bank_Name','Customer_GST_No']
    custData = Customer_Details.query\
    .add_columns(Customer_Details.Customer_ID, Customer_Details.Customer_Name,Customer_Details.Customer_Email, Customer_Details.Customer_Mobile_No, Customer_Details.Customer_Address, Customer_Details.Customer_Bank_Name,Customer_Details.Customer_GST_No)\
    .filter(Customer_Details.Customer_ID == int(customerId))
    custResult = [{col: getattr(d, col) for col in cols1} for d in custData]
    print(custResult)
    customerDetails1 = []
    c =0
    for d in custData:
        if c == 0:
            tmp_dict = {}
            tmp_dict['Customer_Id'] =  d.Customer_ID
            tmp_dict['Customer_Name'] = d.Customer_Name
            customerDetails1.append((tmp_dict))
        c=c+1

    # data = Sales_Master.query\
    # .join(Sales_Detail, Sales_Master.Sales_Req_Id==Sales_Detail.Sales_Req_Id)\
    # .join(Customer_Details, Sales_Master.Customer_Id==Customer_Details.Customer_ID)\
    # .add_columns(Sales_Master.Sales_Req_Id, Sales_Master.Customer_Id,Sales_Detail.Sales_Req_Id,\
    # Sales_Detail.Quantity,Sales_Detail.Rate,Sales_Detail.GST_Percent,Customer_Details.Customer_ID,Customer_Details.Customer_Name)\
    # .filter(Sales_Master.Customer_Id==customerId)\
    # .all()
    #
    # customerDetails = []
    # a =0
    # for r in data:
    #
    #     if a == 0:
    #         tmp_dict = {}
    #         tmp_dict['Customer_Id'] =  r.Customer_Id
    #         tmp_dict['Customer_Name'] = r.Customer_Name
    #         customerDetails.append((tmp_dict))
    #     a=a+1

    # cols = ['Sales_Req_Id', 'Customer_Id', 'Customer_Name', 'Quantity', 'Rate','GST_Percent']
    # result = [{col: getattr(d, col) for col in cols} for d in data]
    # Orders =[]
    # totalSaleAmount = 0
    # salesDetails =[]
    # for r in result:
    #     totalSaleAmount = totalSaleAmount + (r['Quantity'] * r['Rate']) + (r['GST_Percent']/100 * (r['Quantity'] * r['Rate']))
    #     tmp_dict = {}
    #     tmp_dict['Sales_Req_Id'] =  str(r['Sales_Req_Id'])
    #     tmp_dict['Customer_Id'] = str(r['Customer_Id'])
    #     tmp_dict['Quantity'] = str(r['Quantity'])
    #     tmp_dict['Rate'] =str (r['Rate'])
    #     tmp_dict['GST_Percent'] =str (r['GST_Percent'])
    #     salesDetails.append((tmp_dict))


    return jsonify({'SalesInvoiceAmount':SalesInvoiceAmount, 'customerDetails' :customerDetails1, 'nettTotal': str(nettTotal),'paymentAmount':str(paymentAmount)})
    # return jsonify({'salesDetails':salesDetails, 'customerDetails' :customerDetails, 'totalSaleAmount' : str(totalSaleAmount)})
    # return render_template("DisplaySaleReqByID.html",SalesDetails=SalesDetails, customerDetails = customerDetails, totalSaleAmount = totalSaleAmount)




@business.route('/createClientAccountDetails',methods=['POST'])
@login_required
def createClientAccountDetails():
    try:
        message =''
        clientaccno   =request.form.get('clientaccno', 0, type=str)
        loginid =request.form.get('loginid', 0, type=str)
        passwrd =request.form.get('passwrd', 0, type=str)
        servername =request.form.get('servername', 0, type=str)
        brokername =request.form.get('brokername', 0, type=str)
        lotsize =request.form.get('lotsize', 0, type=str)
        equitycap =request.form.get('equitycap', 0, type=str)
        masterId =request.form.get('loginUserID', 0, type=str)
        clientID =request.form.get('clientID', 0, type=str)
        active =request.form.get('active', 0, type=str)
        comments ='Client Account Details Created'
        createdBy   = masterId
        modifiedBy   = masterId
        createdDate =  datetime.now()
        modifiedDate =  datetime.now()
        clientAccountsData = Client_Trade_Account(clientID,clientaccno,loginid,passwrd,servername,brokername,
        lotsize,equitycap,True,comments,createdBy,createdDate,modifiedBy,modifiedDate)
        db.session.add(clientAccountsData)
        db.session.commit()
        message='Clients Accounts Details Created with ID:  '+ str(clientAccountsData.Client_Trade_Id)

    except:
        message = 'Error in Creating Client Accounts Details in data base'
    finally:
        return render_template("confirm.html",submitMessage =message)
        db.session.close()


@business.route('/tradelogic/business/getSymbolInfo')
@login_required
def getSymbolInfo():
    symbol=request.args.get('symbol', 0, type=str)
    userId= 235181
    userPassword= "b61d8c2S"
    serverName ="FidelisCapitalMarkets-Demo"
    tickData,ask=getSymbolDetails(symbol, userId, userPassword, serverName)
    return jsonify({'bid': str(tickData),'ask': str(ask) })

@business.route('/tradelogic/business/getSymbolAB')
@login_required
def getSymbolAB():
    symbol=request.args.get('symbol', 0, type=str)
    userId= 235181
    userPassword= "b61d8c2S"
    serverName ="FidelisCapitalMarkets-Demo"
    bid,ask,askhigh,asklow,bidhigh,bidlow=getSymbolAskBid(symbol, userId, userPassword, serverName)
    return jsonify({'bid': str(bid),'ask': str(ask),'askhigh': str(askhigh),'asklow': str(asklow),'bidhigh': str(bidhigh),'bidlow': str(bidlow) })



def AllclientsTradeAccounts():
    try:
        result=[]
        cols = ['Client_Trade_Id', 'Client_Id', 'Client_Mt5_Account_No', 'Client_Mt5_Login_Id',\
         'Client_Mt5_Login_Password','Client_Mt5_Server_Name','Client_Mt5_Broker_Name',\
         'Client_Mt5_Lot_Size','Client_Mt5_Equity_Capital', 'Client_Mt5_Account_Status',\
         'Created_Date']
        allAccounts = Client_Trade_Account.query.filter(Client_Trade_Account.Created_By == str('1'))

        result = [{col: getattr(d, col) for col in cols} for d in allAccounts]
    except:
        print('No Records fetched from table Client_Trade_Account ')
    finally:
        return result
        session.close()

@business.route('/tradelogic/business/placeTradeInExchange')
@login_required
def placeTradeInExchange():
    symbol=request.args.get('symbol', 0, type=str)
    mainTypeId=request.args.get('mainTypeId', 0, type=str)
    OrderTypeId=request.args.get('OrderTypeId', 0, type=str)
    tradeVolume=request.args.get('tradeVolume', 0, type=str)
    tradePrice=request.args.get('tradePrice', 0, type=str)
    tradeStopLoss=request.args.get('tradeStopLoss', 0, type=str)
    tradeTakeProfit=request.args.get('tradeTakeProfit', 0, type=str)
    Master_Id=request.args.get('masterID', 0, type=str)
    createdDate =  datetime.now()
    modifiedDate =  datetime.now()
    print('symbol=============== '+symbol)
    # if (symbol.strip() != '' and mainTypeId.strip() != '' and OrderTypeId.strip() != ''  and tradeVolume.strip() != '' and tradeStopLoss.strip() != '' and tradeStopLoss.strip() != '' and tradeTakeProfit.strip() != '') :
    if (
            symbol.strip() != '' and mainTypeId.strip() != '' and OrderTypeId.strip() != ''  and
            tradeVolume.strip() != '' and tradeStopLoss.strip() != '' and
            tradeStopLoss.strip() != '' and tradeTakeProfit.strip() != ''
        ):
        print('mainTypeId '+mainTypeId)
        print('tradePrice-------------> '+tradePrice)
        print(type(OrderTypeId))

        instrument = symbol
        tradeOrder_Type = 'short'
        entryPrice = tradePrice
        stopLoss = tradeStopLoss
        takeProfit = tradeTakeProfit
        userId= 235181
        userPassword= "b61d8c2S"
        serverName ="FidelisCapitalMarkets-Demo"

        Trade_Type = '1'
        Order_Type = '1'
        Status = False
        Message_Id = '100'
        Order_Owner_Id = '235181'
        Order_Login_Id = '235181'
        Trade_Field = 'Test Field'
        Comments = 'Order Created'
        if mainTypeId == '1':
            entryPrice = 1.2000
        message=''
        tradeOrder_Type=''
        currMarketPrice = getCurrentMarketPrice(instrument, userId, userPassword, serverName)

        if mainTypeId == '1' and  OrderTypeId == '1'  and  float(stopLoss) < currMarketPrice:
            tradeOrder_Type = 'BUY'
        if mainTypeId == '1' and  OrderTypeId == '2'  and  float(stopLoss) > currMarketPrice:
            tradeOrder_Type = 'SELL'


        if mainTypeId == '2' and  OrderTypeId == '5'  and  float(entryPrice) > currMarketPrice:
            tradeOrder_Type = 'BUY_STOP'
        if mainTypeId == '2' and  OrderTypeId == '4' and  float(entryPrice) > currMarketPrice:
            tradeOrder_Type = 'SELL_LIMIT'

        if mainTypeId == '2' and  OrderTypeId == '3' and float(entryPrice) < currMarketPrice:
            tradeOrder_Type = 'BUY_LIMIT'
        if  mainTypeId == '2' and  OrderTypeId == '6' and float(entryPrice) < currMarketPrice:
            tradeOrder_Type = 'SELL_STOP'

        if   (mainTypeId == '1' or mainTypeId == '2') and tradeOrder_Type != '':
            orderId,tradeStatus=executePendingOrder(instrument, tradeOrder_Type, entryPrice, takeProfit, stopLoss, userId, userPassword, serverName)
        # orderId,tradeStatus=executeOrder(instrument, tradeOrder_Type, entryPrice, takeProfit, stopLoss, userId, userPassword, serverName)
            Trade_Type = mainTypeId
            Order_Type = OrderTypeId
            print(type(orderId))
            print('tradeStatus '+tradeStatus)
            print('orderId '+str(orderId))
            if int(orderId) > 0:
                createMasterOrder(orderId, int(Trade_Type), int(Order_Type),Master_Id,
                instrument,float(entryPrice),float(takeProfit),float(stopLoss),Status,int(Message_Id),
                int(Order_Owner_Id),int(Order_Login_Id),Trade_Field,Comments,Master_Id,
                createdDate,Master_Id,modifiedDate )

            allclients = AllclientsTradeAccounts()
        # print(allclients)
            for clientInfo in allclients:
                clientId = clientInfo['Client_Id']
                userId = clientInfo['Client_Mt5_Login_Id']
                userPassword = clientInfo['Client_Mt5_Login_Password']
                serverName = clientInfo['Client_Mt5_Server_Name']
                # print(str(userId)+" "+str(serverName))
                if  mainTypeId == '1' or mainTypeId == '2':
                    # orderId,tradeStatus=executePendingOrder(instrument, tradeOrder_Type, entryPrice, takeProfit, stopLoss, userId, userPassword, serverName)
                    slaveOrderId,slaveTrdStatus=executePendingOrder(instrument, tradeOrder_Type, entryPrice, takeProfit, stopLoss, userId, userPassword, serverName)
                    print(type(slaveOrderId))
                    print('orderId '+str(slaveOrderId))
                    if int(slaveOrderId) > 0:
                        print('slaveOrderId-----------------------')
                        createSlaveOrder(slaveOrderId, orderId,int(Trade_Type), int(Order_Type),Master_Id,
                        clientId,instrument,float(entryPrice),float(takeProfit),float(stopLoss),Status,int(Message_Id),
                        int(userId),int(userId),Trade_Field,Comments,Master_Id,createdDate,Master_Id,modifiedDate)
                if tradeStatus == 'Market Closed':
                    message =  'The Market is closed'
                if tradeStatus == 'Invalid Price':
                    message =   'Invalid Price in the trade request'
                if tradeStatus == 'Invalid Stops':
                    message =   'Invalid Stops in the trade request'
                if tradeStatus == 'Invalid Stops':
                    message =   'Invalid Stops in the trade request'
                if tradeStatus == 'Order Executed':
                    message =  'The order no: ( '+str(orderId)+' ) has been placed for the symbol '+instrument
            # return jsonify({'result': 'The order no: ( '+str(orderId)+' ) has been placed for the symbol '+instrument})
        return jsonify({'result': message})
    else:
        return jsonify({'result': 'Request cant be processed now'})

@business.route('/tradelogic/business/getMarketPrice')
@login_required
def getMarketPrice():
    instrument = request.args.get('symbol', 0, type=str)
    print('instrument '+instrument)
    userId= 235181
    userPassword= "b61d8c2S"
    serverName ="FidelisCapitalMarkets-Demo"
    currMarketPrice = getCurrentMarketPrice(instrument, userId, userPassword, serverName)
    print('currMarketPrice '+str(currMarketPrice))
    return jsonify({'CurrentMarketPrice': str(currMarketPrice) })
