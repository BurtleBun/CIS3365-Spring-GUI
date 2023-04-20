import flask
from flask import jsonify
from flask import request, make_response
import creds
from sql import create_connection
from sql import execute_read_query
from sql import execute_query 
# pip instal flask_cors
from flask_cors import CORS

# Set up application
app = flask.Flask(__name__) 
app.config["DEBUG"] = True

# Enable CORS
CORS(app)

# db info
myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName) 
cursor = conn.cursor(dictionary = True)

# authorized user login
masterPassword = "strongpassword123"
masterUsername = "username"

################################################################################################################
# COMMON APIs
################################################################################################################

# Show all customers
@app.route("/customer", methods=["GET"])
def show_customers():
    sql = "SELECT * FROM Customer"
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Show all employees
@app.route("/employees", methods=["GET"])
def show_employees():
    sql = "SELECT * FROM Employee"
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Show all services
@app.route("/services", methods=["GET"])
def show_service():
    sql = "SELECT * FROM Service"
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Show all Customer Statuses
@app.route("/custStatus", methods=["GET"])
def show_customer_status():
    sql = "SELECT * FROM CustomerStatus"
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Show all States
@app.route("/state", methods=["GET"])
def state():
    sql = "SELECT * FROM State"
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Show all Countries
@app.route("/country", methods=["GET"])
def country():
    sql = "SELECT * FROM Country"
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)


################################################################################################################
# BUSINESS REPORTS
################################################################################################################
# Steven"s Reports
# Show last month"s revenue
@app.route("/showMonthRevenue", methods=["GET"])
def show_month_revenue():
    sql = """
    SELECT
    ServiceOrderLine.ServiceID,
    Payment.PaymentID AS "Payment ID",
    PaymentTransaction.OverallTotal AS "Transaction Total",
    PaymentTransaction.PaymentDate AS "Pay Date",
    Payment.Tip,
    PaymentMethod.PaymentMethod,
    CardNetwork.Name AS "Card Type",
    ServiceOrderStatus.Status AS "Service Order Status"
    FROM
    Payment
    JOIN PaymentTransaction ON Payment.PaymentID = PaymentTransaction.PaymentID
    JOIN PaymentMethod ON Payment.PaymentMethodID = PaymentMethod.PaymentMethodID
    LEFT JOIN CardNetwork ON Payment.CardID = CardNetwork.CardID
    JOIN ServiceOrder ON Payment.ServiceOrderID = ServiceOrder.ServiceOrderID
    JOIN ServiceOrderLine ON ServiceOrder.ServiceOrderLineID = ServiceOrderLine.ServiceOrderLineID
    JOIN ServiceOrderStatus ON ServiceOrder.StatusCode = ServiceOrderStatus.StatusCode
    WHERE
    PaymentTransaction.PaymentDate BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND NOW()
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Show employees with social media account
@app.route("/showEmpSocial", methods=["GET"])
def show_employee_social():
    sql = """
    SELECT 
    Employee.EmployeeID, 
    CONCAT(Employee.FirstName, " ", Employee.LastName) AS "Full Name", 
    EmploymentType.Type AS "Employment Type", 
    EmployeeStatus.Status AS "Employee Status",
    SocialMedia.WebsiteName AS "Social Media Website", 
    SocialMediaAccount.Username AS "Social Media Username"
    FROM 
    Employee 
    INNER JOIN EmploymentType ON Employee.EmploymentCode = EmploymentType.EmploymentCode
    INNER JOIN EmployeeStatus ON Employee.StatusCode = EmployeeStatus.StatusCode
    LEFT JOIN SocialMediaAccount ON Employee.AccountID = SocialMediaAccount.AccountID
    LEFT JOIN SocialMedia ON SocialMediaAccount.SocialMediaID = SocialMedia.SocialMediaID
    WHERE
    SocialMediaAccount.Username IS NOT NULL;
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Show the most popular service for the past year
@app.route("/showPopularService", methods=["GET"])
def show_popular_service():
    sql = """
    SELECT 
    Service.Name AS "Service Name", 
    COUNT(*) AS "NumOrders",
    ServiceType.ServiceType,
    Service.Abbreviation AS "Abbreviation",
    ServiceStatus.Status
    FROM 
    Service
    JOIN ServiceOrderLine ON Service.ServiceID = ServiceOrderLine.ServiceID
    JOIN ServiceOrder ON ServiceOrderLine.ServiceID = ServiceOrder.ServiceOrderLineID
    JOIN ServiceStatus ON Service.StatusCode = ServiceStatus.StatusCode
    JOIN ServiceType ON Service.ServiceTypeID = ServiceType.ServiceTypeID
    WHERE
    ServiceOrder.CreationDate >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
    GROUP BY 
    Service.ServiceID
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Show service order lines by employee
@app.route("/SOLEmp", methods=["GET"])
def show_SOL_Emp():
    sql = """
    SELECT 
    Service.Name AS "Service Name", 
    COUNT(*) AS "NumOrders",
    ServiceType.ServiceType,
    Service.Abbreviation AS "Abbreviation",
    ServiceStatus.Status
    FROM 
    Service
    JOIN ServiceOrderLine ON Service.ServiceID = ServiceOrderLine.ServiceID
    JOIN ServiceOrder ON ServiceOrderLine.ServiceID = ServiceOrder.ServiceOrderLineID
    JOIN ServiceStatus ON Service.StatusCode = ServiceStatus.StatusCode
    JOIN ServiceType ON Service.ServiceTypeID = ServiceType.ServiceTypeID
    WHERE
    ServiceOrder.CreationDate >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
    GROUP BY 
    Service.ServiceID
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

#Thanh"s Reports
# Service Order Line by employee in a month
@app.route("/EmpSOLMonth", methods=["GET"])
def show_Emp_SOL():
    sql = """
    SELECT
    DB.ServiceOrder.ServiceOrderID as "Order Number",
    DB.ServiceOrderLine.ServiceOrderLineID as "Order Line Number", 
    DB.Employee.FirstName as "Employee Frist Name", 
    DB.Employee.LastName as "Employee Last Name",
    DB.Service.Name as "Service Name",
    DB.ServiceOrderStatus.Status as "Service Order Status"
    FROM DB.ServiceOrder
    join DB.ServiceOrderLine ON DB.ServiceOrderLine.ServiceOrderLineID=ServiceOrder.ServiceOrderLineID
    Join DB.Employee ON DB.ServiceOrderLine.EmployeeID=Employee.EmployeeID
    Join DB.Service ON DB.Service.ServiceID=ServiceOrderLine.ServiceID
    Join DB.ServiceOrderStatus ON DB.ServiceOrderStatus.StatusCode=ServiceOrder.StatusCode
    WHERE
    DB.Employee.EmployeeID= 3 And month(ServiceOrder.CreationDate)=3;
    SELECT
    DB.Employee.FirstName as "Employee Name", COUNT(DB.ServiceOrderLine.ServiceOrderLineID) as "Number of Order Line"
    FROM DB.ServiceOrderLine
    Left Join DB.Employee ON DB.ServiceOrderLine.EmployeeID=DB.Employee.EmployeeID
    Group By Employee.FirstName
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Employee"s Experience with service
@app.route("/EmpExperience", methods=["GET"])
def employee_experience():
    sql = """
    Select
    DB.Employee.FirstName as "Employee Frist Name", 
    DB.Employee.LastName as "Employee Last Name",
    DB.Service.Name as "Service Name",
    DB.EmployeeExperience.ExperienceLevel As "Experience Level",
    DB.EmploymentType.Type as "Employee Type",
    DB.EmployeeStatus.Status as "Employee Status"
    FROM
    DB.EmployeeExperience
    Join DB.Employee ON DB.EmployeeExperience.EmployeeID=Employee.EmployeeID
    Join DB.Service ON DB.Service.ServiceID=EmployeeExperience.ServiceID
    Join DB.EmployeeStatus ON DB.EmployeeStatus.StatusCode=Employee.StatusCode
    Join DB.EmploymentType ON DB.EmploymentType.EmploymentCode=Employee.EmploymentCode
    WHERE
    DB.EmployeeExperience.ExperienceLevel= "Advanced" or DB.EmployeeExperience.ExperienceLevel= "Beginner"
    Order by DB.EmployeeExperience.ExperienceLevel;
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Service Order Lines in a month
@app.route("/SOLMonth", methods=["GET"])
def SOL_Month():
    sql = """
    SELECT 
    DB.ServiceOrder.ServiceOrderID as "Order Number",
    DB.ServiceOrderLine.ServiceOrderLineID as "Order Line Number", 
    DB.Customer.FirstName as "Customer First Name",
    DB.Customer.LastName as "Customer Last Name",
    DB.ServiceOrder.CreationDate as "Order Date",
    DB.PaymentTransaction.PaymentDate "Payment Date",
    DB.ServiceOrderLine.Price as "Order Line Price", 
    DB.PaymentTransaction.OverallTotal as "Overall Total",
    DB.PaymentMethod.PaymentMethod as "Payment Method",
    DB.ServiceOrderStatus.Status as "Service Order Status"
    FROM
    DB.ServiceOrder
    Join DB.Customer ON DB.Customer.CustomerID=ServiceOrder.CustomerID
    join DB.ServiceOrderLine ON DB.ServiceOrderLine.ServiceOrderLineID=ServiceOrder.ServiceOrderLineID
    Join DB.Payment ON DB.ServiceOrder.ServiceOrderID=Payment.ServiceOrderID
    join DB.PaymentTransaction ON DB.Payment.PaymentID=PaymentTransaction.PaymentID
    Join DB.PaymentMethod ON DB.PaymentMethod.PaymentMethodID=Payment.PaymentMethodID
    Join DB.ServiceOrderStatus ON DB.ServiceOrderStatus.StatusCode=ServiceOrder.StatusCode
    WHERE
    month(ServiceOrder.CreationDate)=2
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Chris"s Reports
# All service order lines by an employee
@app.route("/SOLEmp", methods=["GET"])
def SOL_Emp():
    sql = """
    SELECT
    DB.ServiceOrderLine.ServiceOrderLineID as "Service Order Line ID",
    DB.ServiceOrderLine. EmployeeID as "Employee ID",
    DB.Employee.FirstName as "First Name",
    DB.Employee.LastName as "Last Name",
    DB.ServiceOrderLine.ServiceID as "Service ID",
    DB.ServiceOrderLine.Price as "Service Line Price",
    DB.ServiceOrder.CreationDate as "Order Creation Date"
    FROM
    DB.ServiceOrderLine
    join DB.Employee ON DB.ServiceOrderLine.EmployeeID=Employee.EmployeeID
    join DB.Service ON DB.ServiceOrderLine.Price=Service.Price
    join DB.ServiceOrder ON DB.ServiceOrderLine.ServiceOrderLineID=ServiceOrder.ServiceOrderLineID
    WHERE
    DB.ServiceOrderLine.EmployeeID= 1 AND DB.ServiceOrderLine.ServiceOrderLineID=49
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Service Incidents of an employee
@app.route("/SOLEmp", methods=["GET"])
def SOL_Employee():
    sql = """
    SELECT 
    DB.ServiceIncident.ServiceIncidentID as "Service Incident ID",
    DB.ServiceIncident.ServiceOrderID as "Service Order ID",
    DB.Employee.FirstName as "First Name",
    DB.Employee.LastName as "Last Name",
    DB.ServiceIncident.Description,
    DB.ServiceIncident.RedoService as "Redo Service",
    DB.ServiceIncident.StatusCode as "Status Code"
    FROM
    DB.ServiceIncident
    join DB.ServiceOrderStatus ON DB.ServiceIncident.StatusCode=ServiceOrderStatus.StatusCode
    join DB.Employee ON DB.ServiceIncident.EmployeeID=Employee.EmployeeID
    join DB.ServiceOrder ON DB.ServiceIncident.ServiceOrderID=ServiceOrder.ServiceOrderID
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Customers Retention in a month
@app.route("/CustRetention", methods=["GET"])
def Customer_Retention():
    sql = """
    SELECT
    DB.ServiceOrder.ServiceOrderID as "Service Order ID",
    DB.ServiceOrderLine.ServiceOrderLineID as "Service Line ID",
    DB.Customer.FirstName as "Customer First Name",
    DB.Customer.LastName as "Customer Last Name",
    DB.ServiceOrderLine.ServiceID as "Service ID",
    DB.Service.Name as "Service Name",
    DB.ServiceOrder.CreationDate as "Order Creation Date",
    DB.Customer.StatusCode as "Customer Status"
    FROM
    DB.ServiceOrder
    join DB.Customer ON DB.ServiceOrder.CustomerID=Customer.CustomerID
    join DB.ServiceOrderLine ON DB.ServiceOrder.ServiceOrderLineID=ServiceOrderLine.ServiceOrderLineID
    join DB.Service ON DB.ServiceOrderLine.ServiceID=Service.ServiceID
    WHERE
    DB.Customer.CustomerID=11 AND MONTH(ServiceOrder.CreationDate)=2
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Ismael's Reports
# Customer Base Location
@app.route("/CustLocation", methods=["GET"])
def Customer_Location():
    sql = """
    SELECT
    CustomerStatus.`Status` AS "Status",
    Customer.CustomerID AS "CustomerID",
    Customer.FirstName AS "First Name",
    Customer.LastName AS "Last Name",
    CustomerType.`Type` AS "Customer Type",
    PostalCode.PostalCode AS "Postal Code",
    PostalCode.City AS "City",
    PostalCode.StateAbbreviation AS "State"
    FROM
    Customer
    JOIN CustomerStatus ON Customer.StatusCode = CustomerStatus.StatusCode 
    JOIN CustomerType ON Customer.CustomerCode = CustomerType.CustomerCode
    JOIN PostalCode ON Customer.PostalCode = PostalCode.PostalCode
    WHERE
    Customer.StatusCode != 3 AND Customer.StatusCode <> 4
    ORDER BY
    State ASC;
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Last Month's Service Order Report
@app.route("/SOReportMonth", methods=["GET"])
def SO_Report_Month():
    sql = """
SELECT
    ServiceOrderStatus.Status AS "Status",
    ServiceOrder.ServiceOrderID AS "ServiceOrderID",
    ServiceOrder.CreationDate AS "Creation Date",
    Customer.FirstName AS "First Name",
    Customer.LastName AS "Last Name",
    CustomerType.`Type` AS "Customer Type",
    ServiceOrder.AppointmentTime AS "Appointment",
    Service.`Name` AS "Service",
    ServiceType.ServiceType AS "Type",
    ServiceOrderLine.Price AS "Price"
FROM
    ServiceOrder
JOIN ServiceOrderLine ON ServiceOrder.ServiceOrderLineID = ServiceOrderLine.ServiceOrderLineID    
JOIN ServiceOrderStatus ON ServiceOrder.StatusCode = ServiceOrderStatus.StatusCode
JOIN Customer ON ServiceOrder.CustomerID = Customer.CustomerID
JOIN Service ON ServiceOrderLine.ServiceID = Service.ServiceID
JOIN CustomerType ON Customer.CustomerCode = CustomerType.CustomerCode
JOIN ServiceType ON Service.ServiceTypeID = ServiceType.ServiceTypeID

WHERE ServiceOrder.CreationDate >= date_sub(curdate(), interval 1 MONTH)
ORDER BY `Creation Date` DESC;
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Last Month's Referrals Service Order Revenue
@app.route("/RefferalsRevenue", methods=["GET"])
def SO_Report_Month():
    sql = """
SELECT
    PaymentTransaction.TransactionID AS "TransactionID",
    ServiceOrder.ServiceOrderID AS "ServiceOrderID",
	PaymentTransaction.OrderDate AS "Service Date",
    Customer.FirstName AS "First Name",
    Customer.LastName AS "Last Name",
    CustomerType.`Type` AS "Customer Type",
    Service.`Name` AS "Service",
    Payment.Tip AS "Tip Amount",
    PaymentTransaction.OverallTotal AS "Service Order Amount",
    (PaymentTransaction.OverallTotal + Payment.Tip) AS "Total Order Revenue"
    
FROM
	PaymentTransaction
 
JOIN Payment ON PaymentTransaction.PaymentID = Payment.PaymentID
JOIN Customer ON Payment.CustomerID = Customer.CustomerID
JOIN ServiceOrder ON PaymentTransaction.ServiceOrderID = ServiceOrder.ServiceOrderID
JOIN ServiceOrderLine ON ServiceOrder.ServiceOrderLineID = ServiceOrderLine.ServiceOrderLineID
JOIN Service ON ServiceOrderLine.ServiceID = Service.ServiceID
JOIN CustomerType ON Customer.CustomerCode = CustomerType.CustomerCode
JOIN ServiceType ON Service.ServiceTypeID = ServiceType.ServiceTypeID

WHERE PaymentTransaction.PaymentDate >= date_sub(curdate(), interval 1 MONTH) AND CustomerType.`Type` = 'Referral'
GROUP BY PaymentTransaction.TransactionID

ORDER BY `Service Date` DESC;"""

    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)


#Mary's Reports
#Employee Incidents in a month
@app.route("/EmpIncidentMonth", methods=["GET"])
def Employee_incident_Month():
    sql = """
Select
CONCAT(DB.Employee.FirstName, " ", DB.Employee.LastName) AS "Full Name",
DB.EmployeeIncident.IncidentID AS "Incident No.",
DB.EmployeeIncident.Description AS "Description",
DB.EmployeeIncident.Date AS "Date Occurred",
DB.IncidentStatus.StatusCode AS "Incident Status No.",
DB.IncidentStatus.Status AS "Incident Status",
DB.EmployeeIncident.EmployeeID AS "Employee No.",
DB.EmployeeStatus.StatusCode AS "Employee Status No.",
DB.EmployeeStatus.Status AS "Employee Status"

FROM DB.EmployeeIncident
JOIN DB.Employee ON DB.EmployeeIncident.EmployeeID = DB.Employee.EmployeeID
JOIN DB.IncidentStatus ON DB.EmployeeIncident.StatusCode = DB.IncidentStatus.StatusCode
JOIN DB.EmployeeStatus ON DB.Employee.StatusCode = DB.EmployeeStatus.StatusCode


WHERE month(DB.EmployeeIncident.Date)=2
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Specific Services done in a month
@app.route("/MarchServices", methods=["GET"])
def MarchServices():
    sql = """
SELECT
DB.Service.ServiceID AS "Service No.",
DB.Service.Name AS "Service Name",
DB.Service.Abbreviation AS "Abbreviation",
DB.ServiceStatus.Status AS "Service Status",
DB.ServiceType.ServiceType AS "Type"

 

FROM DB.Service
JOIN DB.ServiceStatus ON DB.Service.StatusCode = DB.ServiceStatus.StatusCode
JOIN DB.ServiceType ON DB.Service.ServiceTypeID = DB.ServiceType.ServiceTypeID
JOIN DB.ServiceOrder ON DB.Service.StatusCode = DB.ServiceOrder.StatusCode
JOIN DB.ServiceOrderLine ON DB.Service.ServiceID = DB.ServiceOrderLine.ServiceID

 

WHERE month(DB.ServiceOrder.CreationDate) = 3
GROUP BY DB.ServiceType.ServiceType
ORDER BY DB.Service.ServiceID ASC;
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

# Completed Service Order Appointments for the Month


#Gabe's Reports


app.run()