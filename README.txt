Group 34

Audrey Mohbat (am5083) 
Jain Ryu (jr3990)

PostgreSQL account: jr3990

URL:


<DESCRIPTION OF OUR APPLICATION>
Overview:
We implemented every part we mentioned in Part1 except that the user enters only city name (not both city and state)
to search for hotels. This worked for our application as all cities have unique names in our database and we specified 
states inside the parentheses for clarity.

1) Index.html: 
Application asks users to enter the city they are travelling to.

2) hotelinfo.html:
Returns a list of hotels located in the city with additional information (name, number of rooms, number of stars, date founded). Users select hotels by clicking the button which has each hotel's id.

Also Returns a list of tourist attractions in the city along with its name and price.
Underneath, there are transportation information from one place to another. (This contains all transportation information in our database rather than only those in certain cities.)

3) book.html:
When the user selecs the hotel, it retuns a list of rooms with neceesary information underneath (room number, room size price per night).

Users enter the room number as well as their information to book a room.
This data will be added to "booking" table in the database.
If they have any travel companions, they have to provide their information. 
This data will be added to "travel companion" table in the database.

NEW FEATURES:
1) On any page in the application, the user can access register and login pages or go back to home page.
2) register.html:
The users have to register in order to book a room.
This data will be added to "customer" table in the database.
3) login.html:
When the registered users enter their customer id, it returns information about their past bookings.
It moreover provides a recommendation of hotels which have the same number of stars as those that users have booked before.

Interesting Database Operations:
1) Booking Process
When the user clicks a button on hotelinfo.html, the selected hotel's id is passed to booking page.
Then, it accesses "room" table to list all the rooms in that hotel.
Moreover, to avoid more than one booking in one room, we accessed booking and room tables to retrieve unavailable dates.

2) Hotel Recommendation
user's customer id is passed as an input to booking, room, hotel tables to find booked hotels' number of stars.
Then using a list of number of stars as an input, it retrieves all hotels with the same number of stars.
I thought this was interesting, since it is a simplified version of how real-world recommendation algorithm works. It looks at the past activities and predicts/recommends choices to be made in the future.

