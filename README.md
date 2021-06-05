# THE DARK POKEDEX

*The Dark Pokedex* is a content creation platform for fans of the *Pokemon* franchise.

Have you ever wanted to create your own *Pokemon* and show them off to the world? Well now you can!

*The Dark Pokedex* allows Users to register their Trainer profile; view, search and sort the database of original and User-created monsters; upload their own creations and rate other Users submissions.

# UX

*The Dark Pokedex* was designed to be simple and attractive in aesthetic, with an emphasis on ease-of-use.

## Wireframes

...

## User Stories

- As a fan of the Pokemon series
	- I want to be able to browse a library of Pokemon
    	- so that I can learn about Pokemon and discover Pokemon I may not be aware of
	- I want to search for specific Pokemon
    	- so that I can view data on a specific Pokemon
	- I want an appealing user interface
    	- so that I can browse and enjoy the content comfortably

- As a creator looking for a platform for creative expression
	- I want a simple and intuitive interface
    	- so that I can easily create, publish and edit content
	- I want to be able to create a profile
    	- so that others can see my work
	- I want a rating system
    	- so that I can measure my work against the opinion of a community

- As a User looking for entertainment
	- I want an appealing user interface
    	- so that I can enjoy the content comfortably
	- I want great content to be added frequently
    	- so that I can enjoy new content when I come back to the site in the future
	- I want a rating system
    	- so that I can find the best user rated content

# Features

## Account registration
- Users can create a Trainer profile easily via the Register page.
- A Trainer profile is required to use some of the application's features, such as uploading a *Pokemon* creation and rating other User's submissions.

## Database functionality

### CRUD
- The database uses two primary collections for Pokemon and Trainers (a third is used to store User feedback which is back-end only). The collections are imported via Python and processed before being rendered for the User.
- Once a User has created a Trainer profile, they can contribute a Pokemon by clicking the link on their profile page. 
- Users can edit their creation from their profile page, and delete their creation if they so wish. 

### Search & Sort
- Whilst viewing the Pokedex or Trainers page, Users are given the option to Search or Sort the relevant collection.
- Users can sort Pokemon by Name, Pokedex ID, Species and Rating.
- Users can sort Trainers by Name, Trainer ID, Hometown and Rating.
- Searching is limited to Pokemon/Trainer name and Pokemon type.

## Content contribution
- Registered Users can create and upload their own *Pokemon*.
- Users can choose a Name, Species, Type(s), Height, Weight, Description and URL link to an image for their *Pokemon*.
- Users can preview their creation before uploading by clicking the Preview button.

## Rating system
- Each *Pokemon* in the Pokedex has a Rating score saved to its record, and displayed at the bottom of each Pokedex entry.
- Registered Users can click the Upvote button to add one point to the Pokemon rating score, and deselect the button to remove one point.
- Trainers receive one rating point each time one of their creations receives an upvote.
- Trainers can also be upvoted in the same way Pokemon can, and the total rating for a Trainer is the sum of their personal rating and their overall score from their creations.
- Both the Pokedex and Trainers page can be sorted by Rating to give Users quick access to the best content. 

## Feedback/contact
- A seperate MongoDB collection is used to store User feedback.
- Users can provide feedback on the Contact page by submitting their name and a message.
- The date and time of the feedback submission is saved to the record alongside the name and message.

# Technologies Used
## Database
- MongoDB

## Languages
- HTML
- CSS
- JavaScript
- Python

## Libraries
- Bootstrap
- Materialize
- jQuery
- Font Awesome
- Google Fonts

# Testing

## Functional Testing

## Script Testing

## UX Testing

## User Testing?

# Deployment

## Forking the GitHub Repository
You can fork The Dark Pokedex if you wish to make a copy of the original repository on your GitHub account without affecting the original respository:

1. Log in to your GitHub account and search for/locate this repository
2. Click the 'Fork' button at the top of the page
3. Your GitHub account will now have an exact copy of the project that you can edit

## Deploying the App via Heroku
You can deploy The Dark Pokedex via Heroku by following these steps:

1. Sign in to your Heroku account
2. Click the "New" button and select "Create New App"
3. Choose a name for your app, select your region and click "Create app"
4. In the Settings tab, click Reveal Convig Vars
5. [config vars]
6. In the Deploy tab, select GitHub as your Deployment Method
7. Connect your GitHub account if you haven't done so already
8. Search for the repo you forked from *The Dark Pokedex* and click Connect
9. If you would like your app to update automatically when *The Dark Pokedex* is updated, click Enable Automatic Deploys
10. Ensure the "main" branch is selected next to Manual Deploy and click Deploy Branch
11. Once the build is completed, click Open app at the top of the page

## Making a Local Clone
To clone The Dark Pokedex locally:

1. Ensure you have Python installed on your machine
2. Download the repo using GitHub Desktop and open it in your preferred IDE
3. Create a new file called "env.py" in the root folder
4. [env.py content]
5. Open a bash command line and type "pip3 install -r requirements.txt" and press enter
6. Once the installation is complete, type "python3 app.py" and press enter
7. Ensure port 8080 is public
8. You can now view the application locally in your web browser!

# Credits

## Resources
- move reference table: https://pokemondb.net/pokedex/pikachu/moves/1
- reference img: https://duckduckgo.com/?q=gen+1+pokedex+bulbasaur+image&atb=v255-1&iar=images&iax=images&ia=images&iai=https%3A%2F%2Fi.etsystatic.com%2F10281372%2Fr%2Fil%2Fa5a209%2F688681698%2Fil_794xN.688681698_s3i1.jpg
- regex for input validation taken from: https://stackoverflow.com/questions/46147700/html-5-regex-that-allow-space-between-characters#46147710
- regex test site:
https://regex101.com/r/WWZgf2/1

## Digital Copyright

## Acknowledgements
- thanks everybody!


