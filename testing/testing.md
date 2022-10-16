# Testing 

## CooknRide - recipes to fuel your ride

<br>

[View live website here!](https://flask-recipe-project-sian.herokuapp.com/get_recipes)

[View README.md here!](https://github.com/ictwise/pp3/blob/822cd2ee0cf43314c8418a4bfc19066ad8d21767/README.md)

<br>

## Contents Table

1. [**Testing User Stories from UX Design Section**](#testing-user-stories-from-ux-design-section)
    - **First Time Visitor Goals**
    - **Returning Visitor Goals**
    - **Frequent User Goals**

2. [**Testing**](#testing)
  * Automated Testing
      - **W3C Markup Validator Results**
      - **W3C CSS Validator Results**
      - **JSHint Results**
      - **PEP8 Online Validator Results**
  * Manual Testing

3. [**Bugs Discovered**](#bugs-discovered)

<br>

# Testing User Stories from UX Design Section

<br>

### First Time Visitor Goals

<br>

    * As a first time visitor, I want to easily understand the main purpose of the site.
    * As a first time visitor, I want the site navigation to be intutive, user friendly and over all ease-of-use.
    * As a first time visitor, I want to find recipes that will improve my cycling performance.
    * As a first time visitor, I want to easily access the recipes. 
    * As a first time visitor, I want to be able to create, read, update, delete and search for recipes.
    * As a first time visitor, I want to be able to take part of this community/recipe bank by be able to register. 



![Home Page view](/documentation_testing/img_testing/testing_home.png)

### Returning Visitor Goals

<br>

* Returning Visitor Goals

    * As a returning visitor, I want to be able to easily register if I didn't last time visiting. 
    * As a returning visitor, I want to be able to easily log in, if I registered last time visiting. 
    * As a returning visitor, I want to be able to create, read, update, delete and search for recipes.
    * As a returning visitor, I want to be able to reach out to siteowner for any possible questions.

<br>

![Log In page with contact information](/documentation_testing/img_testing/testing_login.png)



# Testing

<br>

### Automated Testing

<br>

I used https://validator.w3.org/ to test all pages, no errors found. One warning was found I checked base.html and was satisfied that the lack of heading styles wasn't a problem.

<br>

Returning error:
![Returning "Error"](html_validator/error_in_validator.png)

Profile Page errors due to jinja template language as well:
<br>
![Returning "Error"](html_validator/error_profilepage_1.png)
![Returning "Error"](html_validator/error_profilepage_2.png)

<br>

<details><summary><b>Click here for HTML Validator results</b></summary>

- __Home__
<p align="center">
  <img src="html_validator/html_home.png" >
</p>


- __Recipe__
<p align="center">
  <img src="html_validator/html_recipe.png" >
</p>

- __Shop__
<p align="center">
  <img src="html_validator/html_shop.png" >
</p>

- __Log In__
<p align="center">
  <img src="html_validator/html_login.png" >
</p>

- __Register__
<p align="center">
  <img src="html_validator/html_register.png" >
</p>

- __Add Recipes__
<p align="center">
  <img src="html_validator/html_addrecipe.png" >
</p>

- __Profile__
<p align="center">
  <img src="html_validator/html_profile.png" >
</p>

- __Edit Recipe__
<p align="center">
  <img src="html_validator/html_editrecipe.png" >
</p>

- __View Recipe__
<p align="center">
  <img src="html_validator/html_viewrecipe.png" >
</p>

</details>

<details><summary><b>Click here for CSS Validator results</b></summary>

- __CSS Validator Results__
<p align="center">
  <img src="css_validator/css.png" >
</p>
</details>

<details><summary><b>Click here for JSHint results</b></summary>

- __JSHint Results__
<p align="center">
  <img src="jshint/jshint_result.png" >
</p>
</details>

<details><summary><b>Click here for PEP8 Online results</b></summary>

- __PEP8 Online Results__
<p align="center">
  <img src="pep8_validator/pep8.png" >
</p>
</details>

<br>

<br>

### Manual Testing

<br>

#### Responsive Design - PASS

 - All pages were tested locally, and on Heroku using Chrome, Firefox, IE, and Safari. 
 - All pages tested for responsiveness in different device using Google Chrome Developer Tools and Am I Responsive
   - Desktop 
   - iPhone 5/6/7/8/X 
   - iPad 1/2/3/Pro 
   - Galaxy Android phones
- All the pages were also tested manually using;
  - iPhone 5s/6s/8/X/XS/11/
  - Samsung Galaxy S8/Note 10+
  - iPad Air 2 
  - iPad Pro 3
  
<br>

### Functionality Testing

<br>
  
#### Navbar - PASS
  
- All links are working and redirect the user to where they want to go next.
- Hamburger bar at smaller devices works.
- Logo works as link to home page.
  
#### Home Page - PASS
  
- Registration button works.
- All buttons on "popular recipes" works.

#### Recipe Page - PASS 
  
- Search bar is working, and lets user search through recipe name. If user input match any recipe, the recipe in question shows.
- Search button works and starts a search function. 
- Reset button works.
- All recipe cards buttons "View Recipe" works and get the visitor to the recipe visitor wanted to view. 

#### Shop Page - PASS
  
  - All product cards buttons "Buy Now" works and redirects visitor to the product in question page in a new tab outside Lazy Vegan website. 

#### Login - PASS
  
- Form inputs works. 
- Form validations work as expected and gives feedback regarding unmatched format, incorrect username, incorrect password, or if user doesn't exist in the database.
- Log In button works as expected and submits data successfully, and redirects user to Profile page.
- Register account link works.
- Contact email address-link works.

#### Profile - PASS
  
- All recipes added by current user are displayed in cards as it should.
- All recipe cards buttons "View Recipe" (users own added recipes) works and get the visitor to the recipe visitor wanted to view.
- If current user hasn't added any recipes, "Add a Recipe" button shows along with encouraging text.
- "Add a Recipe" button shown when user hasn't added any recipes works.
- Edit button on recipe card works and allows user to easily edit their recipe. 
- Edit button redirects to edit page where all prior added conten is pre-filled as it should.
- All editing works fine and generates a success message. 
- Cancel button works as expected.
- Delete button works as expected and deletes the recipe and generates a success message.
- Back to Recipe button works. 

#### Add Recipe - PASS
  
- All form inputs works, and stores the data in the database.
- Choose category dropdown works.
- Min and max length for text input works.
- Image preview works and show image before uploadadding the recipe. Preview image function on the form is responsive and all images fits all devices sizes.
- Gluten Free switch works (on/off).
- Add Recipe button works and submits data and generate a successfull message.
- The added recipe ends up in Recipe Page as it should.  
  
#### Register - PASS
  
- Form inputs works. 
- Form validations work as expected and gives feedback regarding unmatched format, incorrect username, incorrect password, or if user doesn't exist in the database.
- Register button works as expected and submits data successfully, and redirects user to Profile page.
- Log In link works.
- Contact email address-link works.
  
#### Logout - PASS
  
- Logout functionality works = logs out user, and removes session cookies.
    
#### Footer - PASS
  
- Footer is present on all pages. 
- Social link (Pinterest) in footer works as expected, and open Pinterest in new tab. 
- Email address links to mail function. 
- Back to top button works througout all pages.
  
  
### Security Testing
  
- Tested against users seeing Edit and Delete buttons at other users added Recipes. **PASS**
- Tested Add Recipe page, not to choose category or fill the inputs fields with less text than min length. As well as for the max lenght or skip one or more input fields. **PASS**
- Tested register with a taken username. **PASS**
- Tested register with unallowed character and to few characters. **PASS**
  
### Google Lighthouse Testing 
  
  - All pages were tested using Google's Lighthouse.
  
  <details><summary><b>Click here for Lighthouse results</b></summary>
  
  - __Homepage__
<p align="center">
  <img src="lighthouse/lighthouse_home_page.png" >
</p>

  - __Recipes__
<p align="center">
  <img src="lighthouse/lighthouse_recipe_page.png" >
</p>
  
  - __Shop__
<p align="center">
  <img src="lighthouse/lighthouse_shop_page.png" >
</p>

  - __Log In__
<p align="center">
  <img src="lighthouse/lighthouse_login_page.png" >
</p>

  - __Register__
<p align="center">
  <img src="lighthouse/lighthouse_register_page.png" >
</p>

  - __Profile__
<p align="center">
  <img src="lighthouse/lighthouse_profile_page.png" >
</p>

  - __Add Recipe__
<p align="center">
  <img src="lighthouse/lighthouse_addrecipe_page.png" >
</p>

  - __Edit Recipe__
<p align="center">
  <img src="lighthouse/lighthouse_editrecipe_page.png" >
</p>
</details>

<br>

# Bugs Discovered

**Solved Bugs**

The developer ran into several issues during the development of the site. The most memorable, along with the solution:

MongoDB has been updated since the combined walkthrough was created. 

    mongo.db.tasks.update({"_id": ObjectId(task_id)}, submit) 

no longer worked and had to be replaced with

    mongo.db.recipes.update_one({'_id': ObjectId(_id)}, {'$set': submit})


<br>

#### __[Back to Contents Table](#contents-table)__ 