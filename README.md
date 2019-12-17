1. Project Type : Plan A

2. Group Members Name : Abhishek Sahoo

3. Link to live Application : https://limitless-dusk-24664.herokuapp.com/home

4. Link to Github Code Repository : https://github.com/abhisheksahoo91/csci4131

5. List of Technologies/API's Used: 
   Deezer Developer API
    
6. Detailed Description of the project : 
    
   The name of the project is Music Cloud, which is a music search and stream service provider. The app is designed with a user session management feature. The user is required to create a personal profile in order to access the services. Once, the user is verified and logged in, he/she can query for a music based on albums, artists, playlists or tracks. The web page returns a list of items as per the user request. The basic details of the items with pictures are displayed, which can be selected individually. If the individual item is selected from the list then that would display a detailed information and all the available tracks in a meaningful way. The user can click on any of the entities to start streaming music. The user can interact with the player to pause music, play the next in queue, increase/decrease the volume as needed. There is a complicated network of link redirection which lets the user move around the website to find what he/she wants with little effort. For an example, if the user has searched for an album then he is also presented with the list of authors and the list of tracks in the album. Similar experience applies to other pages as well. The user is also allowed to mark any of the entities as his/her favorite so that it can be made available easily, the next time he/she wants. Similarly any of the entities can be removed from the favorite list any time it is needed. Apart from functional features, the user also has some administrative controls in order to update the account details whenever needed. 

7. List of Controllers and their short description :

	a) home – Home page. Displays data conditionally depending on user has logged or not.
  
	b) register – Implements logic for user registration.
  
	c) login - Implements logic for logging in the user.
  
	d) profile - Implements logic for updating user account information.
  
	e) logout - Implements logic for logging out the user of the current session.
  
	f) searched – This controller is called when the user enters a text and searched for music. Depending on the entity the data is formatted and the respective html file is rendered to display the information in a more presentable way.
  
	g) selected – This controller is called when the user selects a particular entity. It leads to an API call to get all relevant information of the selected entity. The data is formatted before it could be rendered on the webpage. 
  
	h) update_favorite – The origin of this controller lies in the above two rendered webpages. The user can either add to or remove from the favorite list while interacting with the individual objects. This is designed to go back to the original webpage after updating the database.
  
	i) favorite – This controller retrieves the list of the favorite entities in order to display on the webpage as per the user selection.

8. List of Views and their short description :

	a) home.html – For displaying basic details of the default home page. 
  
	b) register.html – For displaying the registration form as well as the associated errors.
  
	c) login.html – For displaying the login form as well as the associated errors.
  
	d) profile.html – For displaying the account update form as well as the errors.
  
	e) layout.html – This is the base layout which contains the navigation bars and header and footer and can be inherited by the other webpages. It provides placeholder blocks those are implemented by the child classes to present information to the user.
  
	f) searched.html – For displaying the list of entities that the user can search using the search bar. This page has actually 4 major conditional and logical division based on the search type. 
  
	g) selected.html – This is called when a user selects a particular entity from the list that was presented to him/her in the previous step. 
  
	h) favorite.html – This webpage presents the list of favorite entities of the corresponding user. Again this has 4 major conditional and logical partition based on the type of search. 

9. List of Tables, their Structure and short description:

	a) User – This table contains all user details such as id, first name, last name, username, email, password. 
  
	b) Genre – This table contains music genre id and genre name. This is used to group the albums based on their genre and sort them according to the number of album content in an descending order. 
  
	c) Entity – This table contains the entity id and entity name values, which is basically the type of search requested by the user.
  
	d) Favorite – This contains all the favorite entities for a user. The columns of this table are id, user_id, entity_type, entity_id, date_created. The user_id data is queried against the current_user values and the date_created is useful for sorting the results in a meaningful way with the newly added entity shown first.
  

10. References/Resources :

	a) Deezer developer API documentation for integrating the music database and stream service.
  
	b) For user registration and database management - Python Flask Tutorial: Full Featrured Web App by Corey Schafer - The link to github repository - https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog
  
