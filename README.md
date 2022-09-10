# RECIPES

## ToDo:
## LOGIN | REGISTRATION 
### Registration Validations
- [x] 1 First and Last name must be at least 2 characters
- [x] 2 Email must have valid email format
- [x] 3 Password and Confirm Password must match
- [x] 4 User must not already exist in the DB
### Login Validations
- [x] 1 Email must already exist in the database
    - [x] 1.1 Password must be checked against the hashed password in the DB for the existing user
## SUCCESS PAGE
### Functionality Requirements
- [x] 1 Create link: renders the create page
- [x] 2 Logout link: clears the user session, redirects to the login page
- [x] 3 User must be logged in to view this page
- [x] 4 Only show the edit and delete links if the recipe was created by the logged in user
- [x] 5 Delete link: removes the recipe and redirects back to this page
- [x] 6 Edit link: renders the edit page for that recipe
- [x] 7 View recipe link: renders the recipe details page for that recipe
## CREATE RECIPE
### Functionality Requirements
- [x] 1 Redirect back to create page to show any errors in form validation
- [x] 2 User must be logged in to see this page
- [x] 3 Name, description, and instructions must be at least 3 characters
- [x] 4 Submit: after creation, redirect to the dashboard
## EDIT RECIPE
### Functionality Requirements
- [x] 1 Redirect back to edit page and show error messages
- [x] 2 User must be logged in to view this page
- [x] 3 Same validations as create
- [x] 4 Pre-populate the fields
- [x] 5 Submit: after update, redirect to recipes dashboard
## VIEW RECIPE
### Functionality Requirements
- [x] 1 Display recipe selected
- [x] 2 User must be logged in to view this page
# recipes_deployed
