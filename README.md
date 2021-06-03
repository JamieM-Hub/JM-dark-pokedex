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

You can deploy this project to GitHub by doing the following:

1. Log in to your GitHub account and search for/locate this repository
2. Click the 'Settings'button at the top of the page
3. Find the 'GitHub Pages' section
4. Make sure 'main' is selected on the 'Branch' dropdown
5. Click the newly-created link with a green tick next to it.
6. Enjoy the website!

## Forking the GitHub Repository
You can fork this GitHub Repository if you wish to make a copy of the original repository on your GitHub account without affecting the original respository:

1. Log in to your GitHub account and search for/locate this repository
2. Click the 'Fork' button at the top of the page
3. Your GitHub account will now have an exact copy of the project that you can edit

## Making a Local Clone
1. Log in to your GitHub account and search for/locate this repository
2. Click the 'Code' dropdown and select your cloning method
3. If you have GitHub Desktop, click the GitHub Desktop button
    * The application will open with this repository available for editing
4. If you're using an alternative Git service
    1. Open Git Bash
    2. Make sure the current working directory is set to the location where you want to place the clone.
    3. Type 'git clone' in your command line and paste the URL given on the GitHub repository page

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


