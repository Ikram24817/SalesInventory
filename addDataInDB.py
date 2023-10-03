from sqlalchemy import Column,Numeric, String, DateTime, Date, Integer, Boolean, ForeignKey, update
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import datetime
from dbmodels import  *

def roleAssigned(userid):
    allRoles = System_Authorization.query.all()
    rolesAssignedToUser = ''
    loggedInUser = userid
    for r in allRoles:
        role = r.Role
        users = r.Users
        if any(str(loggedInUser) in s for s in r.Users):

        # if loggedInUser in r.Users:
            rolesAssignedToUser = role
    return  rolesAssignedToUser


def createMasterOrder(Order_Id, Trade_Type, Order_Type,Master_Id,Instrument,\
Entry_Point,Take_Profit,Stop_Loss,Status,Message_Id,Order_Owner_Id,\
Order_Login_Id,Trade_Field,Comments,Created_By,Created_Date,Modified_By,Modified_Date):
    try:
        create_Order = Master_Order_Detail(Order_Id, Trade_Type, Order_Type,Master_Id,Instrument,
        Entry_Point,Take_Profit,Stop_Loss,Status,Message_Id,Order_Owner_Id,
        Order_Login_Id,Trade_Field,Comments,Created_By,Created_Date,Modified_By,Modified_Date )
        db.session.add(create_Order)
        db.session.commit()
        # db.session.close()

    except Exception as e:
        print(e)
    finally:
        db.session.close()

def createSlaveOrder(Order_Id, Master_Order_Id,Trade_Type, Order_Type,Master_Id,\
Client_Id,Instrument,Entry_Point,Take_Profit,Stop_Loss,Status,Message_Id,Order_Owner_Id,\
Order_Login_Id,Trade_Field,Comments,Created_By,Created_Date,Modified_By,Modified_Date):
    try:
        create_Order = Slave_Order_Detail(Order_Id,Master_Order_Id, Trade_Type, Order_Type,Master_Id,
        Client_Id, Instrument, Entry_Point,Take_Profit,Stop_Loss,Status,Message_Id,Order_Owner_Id,
        Order_Login_Id,Trade_Field,Comments,Created_By,Created_Date,Modified_By,Modified_Date )
        db.session.add(create_Order)
        db.session.commit()


    # except:
    except Exception as e:
        print(e)
        # print('Error in Create Order for message id : '+str(Message_Id))
    finally:
        db.session.close()


def addStockToInventory(HSN_Code,Item_Code, rate,Quantity,Unit_Of_Measurement,status\
,comments,Created_By,Created_Date,Modified_By,Modified_Date):
    try:
        InventoryData = Inventory(int(HSN_Code),int(Item_Code),float('2'),int(Quantity),int(Unit_Of_Measurement),
        int(4),comments,Created_By,Created_Date,Modified_By,Modified_Date)
        db.session.add(InventoryData)
        db.session.commit()

        InventoryDetailsData = Inventory_Detail(int(InventoryData.Inventory_Code),int(HSN_Code),int(Item_Code),
        float('2'),int(Quantity),int(Unit_Of_Measurement),int(4),Comments,Created_By,Created_Date,Modified_By,Modified_Date)
        db.session.add(InventoryDetailsData)
        db.session.commit()

    except Exception as e:
        print(e)
    finally:
        db.session.close()
