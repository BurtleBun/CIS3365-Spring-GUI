# CIS3365-Spring-GUI
This is a GUI created for the CIS3365 Spring course's final project.

For this project, we worked with LV Nail Salon to digitally transform their manual record-keeping system with a sophisticated SQL database hosted on an AWS server.The frontend and backend components were developed using a stack that included Python, JavaScript, CSS, HTML, and EJS.

## Sample Photos
*Unfortunately, the AWS server was shut down, and so not all rendered pages can be shown here, but the code and scripts still reside in the repository.*

![CustomerSignupForm](Prjoect%20Images/FrontendHomePage)
>Landing Page

![Customer Signup Form](Prjoect%20Images/CustomerSignUpForm.png)
>Signup Form where new customers register

![Employee Login](Prjoect%20Images/EmployeeLogin.png)
>Employee login page to access employee dashboard


# How it works
When entering, users are met with the home page, where they have the option to sign in as a customer, or sign up as one. The top navigation bar also has the option for the user to sign in as an employee. Aside from a customer account, there are 2 levels to an employee account: a standard employee and a manager. When a standard employee logs in, they are met with a dashboard showing all the current customers and their information in a chart. Managers have the same dashboard, but also get an overview of all employees and their information, as well as the ability to change customer & employee information through the web browser. When a change is made and the employee clicks off of the chart, a click event listener applies those changes directly to the database. Finally, there is a reports page that runs SQL scripts to print out reports organized as a chart on the EJS page.
