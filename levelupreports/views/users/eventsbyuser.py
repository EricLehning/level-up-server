"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all events along with the gamer first name, last name, and id
            db_cursor.execute("""
                SELECT
                    e.id AS event_id,
                    e.description,
                    e.date,
                    e.time,
                    g.title AS game_name,
                    ga.user_id AS organizer_id,
                    u.first_name,
                    u.last_name
                FROM
                    levelupapi_event AS e
                    JOIN levelupapi_game AS g ON e.game_id = g.id
                    JOIN levelupapi_gamer AS ga ON e.organizer_id = ga.id
                    JOIN auth_user AS u ON ga.user_id = u.id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the events_by_user list:
            #
#             # [
#   {
#     "gamer_id": 1,
#     "full_name": "Molly Ringwald",
#     "events": [
#       {
#         "id": 5,
#         "date": "2020-12-23",
#         "time": "19:00",
#         "game_name": "Fortress America"
#       }
#     ]
#   }
# ]

            events_by_user = []

            for row in dataset:
                # TODO: Create a dictionary called event that includes 
                # the description, date, time,
                # game_id, and organizer_id, which references the gamer, and the full_name of the gamer from the row dictionary
                event = {
                    "id": row['event_id'],
                    "description": row['description'],
                    "date": str(row['date']),
                    "time": str(row['time']),
                    "game_name": row['game_name']
                }
                
                # See if the gamer has been added to the events_by_user list already
                user_dict = None
                for user_event in events_by_user:
                     if user_event['gamer_id'] == row['organizer_id']:
                         user_dict = user_event
                
                
                if user_dict:
                    # If the user_dict is already in the events_by_user list, append the event to the events list
                    user_dict['events'].append(event)
                else:
                    # If the user is not on the events_by_user list, create and add the user to the list
                    events_by_user.append({
                        "gamer_id": row['organizer_id'],
                        "full_name": row["first_name"] + " " + row["last_name"],
                        "events": [event]
                    })
        
        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)
