import json
import mysql.connector
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import *
import pathlib
import textwrap

#phind
from .forms import TimetableForm
# views.py
from django.http import JsonResponse
from django.core import serializers
# from .models import TimetableEntry # Assuming TimetableEntry is your model



import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

# api key = AIzaSyBoeUBPThWqaYJbLClhWgqW1TrLiNw_Xjg
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
# Used to securely store your API key
from google.cloud import *


from django.contrib.auth.decorators import login_required
from notifications_app.tasks import process_timetable_deadlines
# Create your views here.
@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        process_timetable_deadlines.delay()
    return render(request,'index.html',{
        'room_name' : 'broadcast'
    })
    #return HttpResponse("This is homepage.")

def dash(request):
    
    return render(request,'dashboard.html')

def chat(request):
    return render(request,'chat.html')

def about(request):
    return render(request, "about.html")


def services(request):
    return HttpResponse("This is service page.")


def contact(request):
    return HttpResponse("This is contact page.")


def pomodoro(request):
    return render(request,'pomodoro.html')
def login(request):
    return render(request,'login.html')








# def save(ts, date, ta, de, stat, rec):
#     try:
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="mmh13138",
#             database="learners"
#         )
#         cursor = connection.cursor()
        
#         # Assuming 'date' is in the format 'YYYY-MM-DD'
#         date_obj = datetime.strptime(date, '%Y-%m-%d')

#         # Check if task is not empty and time slot is not '00:00'
#         if ta and ts != '00:00':

#             insert_query = "INSERT INTO timetable (time_slot, task_activity, description, status, recurring, date) VALUES (%s, %s, %s, %s, %s, %s)"
#             cursor.execute(insert_query, (ts, ta, de, stat, rec, date))
#             connection.commit() # Ensure commit is called here
#             # Check if the task is recurring
#             # if rec == 1:
#             #     recurr(ts, ta, de, stat, date_obj)
#         else:
#             return HttpResponse('Enter the Task activity and Time Slot!')
        
#         connection.close()
#         cursor.close()
        
#     except Exception as e:
#         return HttpResponse(f'An error occurred: {e}')



def delete(request):
    if request.method == 'POST':
            # Connect to the database and execute the delete query
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mmh13138",
                database="learners"
            )
            entry_id = request.POST.get('entry_id')
            cursor = connection.cursor()
            query = "DELETE FROM timetable WHERE id = %s"
            cursor.execute(query, (entry_id,))
            connection.commit()
            cursor.close()
            connection.close()
            # Redirect to the timetable page or display a success message
            return redirect('/timetable')
            


    else:
        # Handle invalid request methods
        return HttpResponse(['POST'])


def return_to_tt(request):
    return redirect('/timetable',)


def recurr(user_id,time_slot, task_activity, description, status, date):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mmh13138",
        database="learners"
    )
    cursor = connection.cursor()

    end_date = date + timedelta(days=6)  # Set end date to 6 days from start date
    current_date = date + timedelta(days=1)  # Start from the day after the start date
    
    while current_date <= end_date:
        # Check if the task already exists for the current date
        query = "SELECT COUNT(*) FROM timetable WHERE user_id = %s and task_activity = %s AND date = %s"
        cursor.execute(query, (user_id,task_activity, current_date.strftime('%Y-%m-%d')))
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insert recurring task into the database for each consecutive date
            insert_query = "INSERT INTO timetable (user_id,time_slot, task_activity, description, status, recurring, date) VALUES (%s,%s, %s, %s, %s, %s, %s)"
            # Provide values for the recurring task
            values = (user_id,time_slot, task_activity, description, status, 1, current_date.strftime('%Y-%m-%d'))
            cursor.execute(insert_query, values)
            
        
        # Move to the next day
        current_date += timedelta(days=1)

    connection.commit()  # Commit the transaction
    connection.close()
    cursor.close()


def get_table_data(user_id):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mmh13138",
        database="learners"
    )
    cursor = connection.cursor()
    query = "SELECT * FROM timetable WHERE user_id = %s and status!= 'Not Done' ORDER BY date, time_slot"
    cursor.execute(query,(user_id,))
    fetched_data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Process the fetched data and populate the timetable_data list
    timetable_data = []
    for row in fetched_data:
        date_obj = datetime.strptime(str(row[9]), '%Y-%m-%d')
    # Derive the day of the week from the datetime object
        day_of_week = date_obj.strftime('%A')
        timetable_data.append({
            'id':row[0],
            'day_of_week': day_of_week,
            'time_slot': row[2],
            'task_activity': row[3],
            'description': row[4],
            'status': row[5],
            'recurring': 'Recurring' if row[6]==1 else 'Not recurring',
            'date':row[9],
        })

    # Pass the data to the template
    data = {'timetable_data': timetable_data}
    return data

def gettable(request):
    user_id = request.user.username
    data = get_table_data(user_id)
    return render(request,'timetable.html',data)



def get_notdone_data(user_id):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mmh13138",
        database="learners"
    )
    cursor = connection.cursor()
    query = "SELECT * FROM timetable WHERE user_id = %s and status = 'Not Done' ORDER BY date, time_slot"
    cursor.execute(query,(user_id,))
    fetched_data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Process the fetched data and populate the timetable_data list
    timetable_data = []
    for row in fetched_data:
        date_obj = datetime.strptime(str(row[9]), '%Y-%m-%d')
    # Derive the day of the week from the datetime object
        day_of_week = date_obj.strftime('%A')
        timetable_data.append({
            'id':row[0],
            'day_of_week': day_of_week,
            'time_slot': row[2],
            'task_activity': row[3],
            'description': row[4],
            'status': row[5],
            'recurring': 'Recurring' if row[6]==1 else 'Not recurring',
            'date':row[9],
        })

    # Pass the data to the template
    data = {'timetable_data': timetable_data}
    return data


def getnotdone(request):
    user_id = request.user.username
    data = get_notdone_data(user_id)
    return render(request,'timetable.html',data)


def get_completed_data(user_id):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mmh13138",
        database="learners"
    )
    cursor = connection.cursor()
    query = "SELECT * FROM timetable WHERE user_id = %s and status = 'Completed' ORDER BY date, time_slot"
    cursor.execute(query,(user_id,))
    fetched_data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Process the fetched data and populate the timetable_data list
    timetable_data = []
    for row in fetched_data:
        date_obj = datetime.strptime(str(row[9]), '%Y-%m-%d')
    # Derive the day of the week from the datetime object
        day_of_week = date_obj.strftime('%A')
        timetable_data.append({
            'id':row[0],
            'day_of_week': day_of_week,
            'time_slot': row[2],
            'task_activity': row[3],
            'description': row[4],
            'status': row[5],
            'recurring': 'Recurring' if row[6]==1 else 'Not recurring',
            'date':row[9],
        })

    # Pass the data to the template
    data = {'timetable_data': timetable_data}
    return data


def getcompleted(request):
    user_id = request.user.username
    data = get_completed_data(user_id)
    return render(request,'timetable.html',data)

def get_inprogress_data(user_id):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mmh13138",
        database="learners"
    )
    print(user_id)
    cursor = connection.cursor()
    query = "SELECT * FROM timetable WHERE (user_id = %s and status = 'In Progress') OR (user_id = %s and status = 'Planned') ORDER BY date, time_slot"

    cursor.execute(query,(user_id,user_id))
    fetched_data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Process the fetched data and populate the timetable_data list
    timetable_data = []
    for row in fetched_data:
        date_obj = datetime.strptime(str(row[9]), '%Y-%m-%d')
    # Derive the day of the week from the datetime object
        day_of_week = date_obj.strftime('%A')
        timetable_data.append({
            'id':row[0],
            'day_of_week': day_of_week,
            'time_slot': row[2],
            'task_activity': row[3],
            'description': row[4],
            'status': row[5],
            'recurring': 'Recurring' if row[6]==1 else 'Not recurring',
            'date':row[9],
        })

    # Pass the data to the template
    data = {'timetable_data': timetable_data}
    return data

def get_in_progress(request):
    user_id = request.user.username
    data = get_inprogress_data(user_id)
    return render(request, 'timetable.html', data)



def delete_all(request):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mmh13138",
        database="learners"
    )
    user_id = request.user.username
    print(type(user_id))
    cursor = connection.cursor()
    query = "DELETE from learners.timetable where user_id=%s"
    cursor.execute(query,(user_id,))
    connection.commit()
    connection.close()
    cursor.close()
    return redirect('/timetable')




def delete_tasks(request):
    if request.method == 'POST':
        try:
            selected_task_ids = request.POST.getlist('selected_tasks')
            if selected_task_ids:
                # Convert list of task IDs to string format for query
                task_ids_string = ', '.join(selected_task_ids)
                
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="mmh13138",
                    database="learners"
                )
                cursor = connection.cursor()
                user_id = request.user.username
            if 'delete_button' in request.POST:
                    # Construct the delete query to delete multiple tasks at once
                    delete_query = "DELETE FROM timetable WHERE user_id=%s AND id IN ({})".format(task_ids_string)
                    cursor.execute(delete_query,(user_id,))
            elif 'progress_button' in request.POST:
                status_query = "UPDATE timetable SET status = 'In Progress' where user_id=%s and  id IN ({})".format(task_ids_string)
                cursor.execute(status_query,(user_id,))
            else:
                status_query = "UPDATE timetable SET status = 'Completed' where user_id=%s and  id IN ({})".format(task_ids_string)
                cursor.execute(status_query,(user_id,))
                
            connection.commit()
            
            cursor.close()
            connection.close()
            return redirect('/timetable')
        except:
            return redirect('/timetable')
    



from django.contrib.auth.decorators import login_required
@login_required
def timetable(request):
#phind one
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            # Extract form data
            user_id = str(request.user)
            time_slot = form.cleaned_data['time_slot']
            date = form.cleaned_data['date']
            task_activity = form.cleaned_data['task_activity']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']
            recurring = form.cleaned_data['recurring']
            print(type(user_id))
            # Call the function to save the timetable entry
            save(user_id,time_slot, date, task_activity, description, status, recurring)
            
            if recurring:
               
                recurr(user_id,time_slot, task_activity, description, status, date)

            # Redirect to a new URL:
            return redirect('/timetable/')
    else:
        form = TimetableForm()
    
    return render(request, 'timetable.html', {'form': form})

def save(user,ts, date, ta, de, stat, rec):
  
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mmh13138",
            database="learners"
        )
        cursor = connection.cursor()
        
        from datetime import datetime

# Assuming 'date' is in the format 'YYYY-MM-DD'
       

        # Check if task is not empty and time slot is not '00:00'
       
        insert_query = "INSERT INTO timetable (user_id,time_slot, task_activity, description, status, recurring, date) VALUES (%s,%s, %s, %s, %s, %s, %s)"            # Execute the query with provided values
        cursor.execute(insert_query, (user,ts, ta, de, stat, rec,date))
        # Commit the transaction
        connection.commit()
        connection.close()
        cursor.close()
        print("save")
        
       
      
        return redirect('/timetable.html')

    

from django.http import JsonResponse
from django.core import serializers
# from .models import TimetableEntry

# def get_scheduled_tasks(request):
#     # Fetch scheduled tasks from the database
#     tasks = TimetableEntry.objects.filter(date__gte=datetime.now().date())
#     # Serialize the tasks to JSON
#     tasks_json = serializers.serialize('json', tasks)
#     # Return the tasks as JSON
#     print(tasks_json)
#     return JsonResponse(tasks_json, safe=False)


# def gemini(request):
#     GOOGLE_API_KEY = 'AIzaSyBoeUBPThWqaYJbLClhWgqW1TrLiNw_Xjg'
#     genai.configure(api_key=GOOGLE_API_KEY)

#     # List available models.
#     print('Available models:')
#     for m in genai.list_models():
#         if 'generateContent' in m.supported_generation_methods:
#             print(f'- {m.name}')
#     model = genai.GenerativeModel('gemini-pro')

#     print('\nReady to chat...')
#     prompt = input("You: ")
#     response = model.generate_content(prompt)
#     responce_text=''.join([p.text for p in response.candidates[0].content.parts])
#     return render(request,'base.html',{"Gemini":responce_text})


def gemini(request):
    
    # Ensure your API key is stored securely, such as in environment variables
    GOOGLE_API_KEY = 'AIzaSyBoeUBPThWqaYJbLClhWgqW1TrLiNw_Xjg'
    genai.configure(api_key=GOOGLE_API_KEY)

    # Create a GenerativeModel instance using the Gemini model
    model = genai.GenerativeModel('gemini-pro')

    # If a user sends a message through a form, retrieve the message from the request
    if request.method == 'POST':
        prompt = request.POST.get('message')  # Assuming the message is sent as 'message' in the form data
    else:
        # If not using a form, you can prompt the user directly
        prompt = input("You: ")

    # Generate a response from the Gemini model based on the user's prompt
    response = model.generate_content(prompt)
    
    # Extract the text response from the Gemini response object
    response_text = ''.join([p.text for p in response.candidates[0].content.parts])
    lines = response_text.strip().split('\n')
    formatted_lines = []
    for line in lines:
        formatted_line = line.strip().replace("**", "").strip()
        formatted_lines.append(formatted_line)

# Join the formatted lines to create the final response
    formatted_response = '\n'.join(formatted_lines)
    connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mmh13138",
                database="learners"
            )
    cursor = connection.cursor()
    query = "INSERT INTO chats (user_message, bot_response) Values(%s, %s);"
    cursor.execute(query, (prompt, formatted_response))
    connection.commit()
    connection.close()
    cursor.close()
    connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mmh13138",
                database="learners"
            )
    cursor = connection.cursor()
    query = "SELECT user_message, bot_response from chats;"
    cursor.execute(query)
    
    # Fetch all rows from the result set
    chat_data = cursor.fetchall()
    
    # Close the cursor and database connection
    cursor.close()
    connection.close()
    
    
    
    return render(request, 'chat.html', {'response_text': formatted_response, 'chat_data': chat_data})




# def gemini(request):
#     if request.method == 'POST' and 'message' in request.POST:
#         message = request.POST['message']
#         response = generate_response(message)
#         return JsonResponse({'response': response})

#     return render(request, 'gemini_chat.html')

# def generate_response(message):
#     GOOGLE_API_KEY = 'AIzaSyBoeUBPThWqaYJbLClhWgqW1TrLiNw_Xjg'
#     genai.configure(api_key=GOOGLE_API_KEY)
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content(message)
#     return ''.join([p.text for p in response.candidates[0].content.parts])

def chat_delete(request):
    connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mmh13138",
                database="learners"
            )
    cursor = connection.cursor()
    query = "TRUNCATE  TABLE chats;"
    cursor.execute(query)
    cursor.close()
    connection.close()
    return redirect('/chat/')


# def getList(request):
#     if request.method=='POST':
#         GOOGLE_API_KEY = 'AIzaSyBoeUBPThWqaYJbLClhWgqW1TrLiNw_Xjg'
#         genai.configure(api_key=GOOGLE_API_KEY)

#         # Create a GenerativeModel instance using the Gemini model
#         model = genai.GenerativeModel('gemini-pro')
#         tasks_list = request.POST.get('task')
#         prompt = "Arrange the following tasks using eisenhower matrix . database ( table learners.tasks(Urgent_important VARCHAR(255),Urgent_notimportant VARCHAR(255),Noturgent_important VARCHAR(255),Noturgent_notimportant VARCHAR(255)); ). Give me only mysql query for inserting the tasks in the right column : "+ tasks_list 
#         response = model.generate_content(prompt)
#         response_text = ''.join([p.text for p in response.candidates[0].content.parts])
#         lines = response_text.strip().split('\n')
#         formatted_lines = []
#         for line in lines:
#             formatted_line = line.strip().replace("**", "").strip()
#             formatted_lines.append(formatted_line)

# # Join the formatted lines to create the final response
#         formatted_response = '\n'.join(formatted_lines)
#         print(formatted_response)
#         return HttpResponse(formatted_response)


# def Task_template(request):
#     return render(request, 'tasklist.html')

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
from notifications.signals import notify
from django.contrib.auth.models import User
from notifications_app.tasks import test_func
def test(request):
    user = request.user.id
    channel_layer = get_channel_layer()
    # for i in range(1,10):
    #     async_to_sync(channel_layer.group_send)(
    #         "notification_"+str(user),
    #         {
    #             'type': 'send_message',
    #             'text_data': json.dumps({'New':"Notification","count":i})
    #         }
    #     )
    #     time.sleep(2)
    # user = User.objects.all()
    notify.send(user,recipient=user, verb='you reached level 10')
    # time.sleep(5)
    test_func.delay(user)
    return redirect('/home/')


from django.http import JsonResponse
from notifications.models import Notification

def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.deleted = False
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)
    
    

def testing(request,notification_id):
    print(notification_id)
    notification = Notification.objects.get(id=notification_id)
    notification.mark_as_read()
    notification.delete()
    return redirect('/get_notdone/')



from django.conf import settings
import os

def react_app(request):
    index_html_path = os.path.join(settings.BASE_DIR, 'static', 'react', 'index.html')
    return render(request, index_html_path)


# @login_required
# def dashboard(request):
#     connection = mysql.connector.connect(
#                 host="localhost",
#                 user="root",
#                 password="mmh13138",
#                 database="learners"
#             )
#     cursor = connection.cursor()
#     user = str(request.user)
#     query = '''SELECT COUNT(*) as completed_task_count, date,status
# FROM learners.timetable
# WHERE status = 'Completed' AND user_id =%s
# GROUP BY date
# ORDER BY date ASC;'''
#     cursor.execute(query,(user,))
#     completed_task_data = cursor.fetchall()
    
    
#     query = '''SELECT COUNT(*) as completed_task_count, date,status
# FROM learners.timetable
# WHERE status = 'Not Done' AND user_id =%s
# GROUP BY date
# ORDER BY date ASC;'''
#     cursor.execute(query,(user,))
#     not_completed_task_data = cursor.fetchall()
#     print(not_completed_task_data)


    
#     data_list = [{'date': d[1], 'value': d[0], 'status': d[2]} for d in completed_task_data + not_completed_task_data]

# # Sort by date
#     data_list.sort(key=lambda x: x['date'])
#     earliest_date = data_list[0]['date']
#     latest_date = data_list[-1]['date']
#     # print(type(min_date)) 
#     total_days = (latest_date - earliest_date).days + 1

# # Generate a list of dates starting from the earliest date
#     dates_sequence = []
#     current_date = earliest_date
#     while current_date <= latest_date:
#         dates_sequence.append(current_date.isoformat())
#         current_date += timedelta(days=1)
    
#     final_data_list = []

# # Iterate over the dates_sequence
#     for date_str in dates_sequence:
#         # Check if the date exists in data_list
#         for item in data_list:
            
#             if str(item['date']) == date_str:
#                 print(type(item['date']),type(date_str))    
#                 # If found, append the item to final_data_list
#                 final_data_list.append({'date': date_str, 'value': item['value'], 'status': item['status']})
#                 break
#         else:
#             # If the date was not found, append a dictionary with value 0
#             final_data_list.append({'date': date_str, 'value': 0, 'status': item['status']})
#     print(final_data_list)
#     final_data_json = json.dumps(final_data_list)
#     #date count of task where status = complete
    
#     cursor.close()
#     connection.close()
#     return render(request, 'dashboard.html',{'data':final_data_json})


# @login_required
# def dashboard(request):
#     connection = mysql.connector.connect(
#                 host="localhost",
#                 user="root",
#                 password="mmh13138",
#                 database="learners"
#             )
#     cursor = connection.cursor()
#     user = str(request.user)

#     # Query for completed tasks
#     query_completed = '''SELECT COUNT(*) as completed_task_count, date,status
#                          FROM learners.timetable
#                          WHERE status = 'Completed' AND user_id = %s
#                          GROUP BY date
#                          ORDER BY date ASC;'''
#     cursor.execute(query_completed, (user,))
#     completed_task_data = cursor.fetchall()

#     # Query for not completed tasks
#     query_not_completed = '''SELECT COUNT(*) as completed_task_count, date,status
#                              FROM learners.timetable
#                              WHERE status = 'Not Done' AND user_id = %s
#                              GROUP BY date
#                              ORDER BY date ASC;'''
#     cursor.execute(query_not_completed, (user,))
#     not_completed_task_data = cursor.fetchall()

#     # Convert data to JSON
#     completed_tasks = [{'date': d[1].isoformat(), 'value': d[0]} for d in completed_task_data]
#     not_completed_tasks = [{'date': d[1].isoformat(), 'value': d[0]} for d in not_completed_task_data]
#     print(completed_tasks)
#     # Close the cursor and connection
#     earliest_date = min([min(d[1] for d in completed_task_data), min(d[1] for d in not_completed_task_data)], default=None)
#     latest_date = max([max(d[1] for d in completed_task_data), max(d[1] for d in not_completed_task_data)], default=None)

#     if earliest_date and latest_date:
#         # Directly use earliest_date and latest_date as datetime.date objects
#         # start_date = datetime.combine(earliest_date, datetime.min.time())  # Combine date with minimum time to get a datetime object
#         # end_date = datetime.combine(latest_date, datetime.max.time())  # Combine date with maximum time to get a datetime object
#         # num_days = (end_date - start_date).days + 1
#         # print('earliest_date: ',type(earliest_date), earliest_date)
#         # # Generate a list of all dates between the earliest and latest dates
#         # all_dates = [(start_date + timedelta(days=i)).isoformat() for i in range(num_days)]

#         # Create empty lists for completed and not completed tasks
#         # completed_tasks = [{'date': '', 'value': 0} for _ in all_dates]
#         # not_completed_tasks = [{'date': '', 'value': 0} for _ in all_dates]
#         dates_str =[]
#         current_date = earliest_date
#         # print(start_date,end_date)
#         while current_date<=latest_date:
#             dates_str.append(current_date.isoformat())
#             current_date += timedelta(days=1)
#         print("dates_str = ",dates_str)
        
        
#         # Populate the lists with actual data
#         # for d in completed_task_data:
#         #     date_in_d = d[1].isoformat()  
#         #     # for j in dates_str:
#         #     #     print("J value =",j)
#         #     #     if date_in_d==j:
#         #     #         print("date in d : ",date_in_d,"------- date in j",j)
#         #     #         final_data_list.append({'date': j, 'value': d[0]})
#         #     #         break
#         #     #     else:
#         #     #         # If the date was not found, append a dictionary with value 0
#         #     #         final_data_list.append({'date': j, 'value': 0})
#         #     if date_in_d in dates_str:
#         #         print(str(date_in_d))
#         #         final_data_list.append({'date':str(date_in_d),'value':d[0]})
#         complete_final_data_list = []

# # Iterate through dates_str
#         for date_str in dates_str:
#             # Initialize a flag to False
#             found = False
#             # Try to find the date in completed_task_data
#             for d in completed_task_data:
#                 if d[1].isoformat() == date_str:
#                     # If found, set the flag to True and store the value
#                     found = True
#                     value = d[0]
#                     break  # Exit the loop since we found a match
#             # After the loop, check the flag to decide what to append
#             if found:
#                 # If found, append the date and its value to final_data_list
#                 complete_final_data_list.append({'date': date_str, 'value': value})
#             else:
#                 # If not found, append the date with a value of 0
#                 complete_final_data_list.append({'date': date_str, 'value': 0})



        
                            
        
        
        
        
#         not_complete_final_data_list = []

# # Iterate through dates_str
#         for date_str in dates_str:
#             # Initialize a flag to False
#             found = False
#             # Try to find the date in completed_task_data
#             for d in not_completed_task_data:
#                 if d[1].isoformat() == date_str:
#                     # If found, set the flag to True and store the value
#                     found = True
#                     value = d[0]
#                     break  # Exit the loop since we found a match
#             # After the loop, check the flag to decide what to append
#             if found:
#                 # If found, append the date and its value to final_data_list
#                 not_complete_final_data_list.append({'date': date_str, 'value': value})
#             else:
#                 # If not found, append the date with a value of 0
#                 not_complete_final_data_list.append({'date': date_str, 'value': 0})



        
                            
#         print(not_complete_final_data_list)
                    
#             # if date_to_insert not in all_dates:  # Check if the date already exists
#             #     continue  # Skip this iteration if the date is not in all_dates
#             # index = all_dates.index(date_to_insert)
#             # completed_tasks[index] = {'date': date_to_insert, 'value': d[0]}

#         # for d in not_completed_task_data:
#         #     date_to_insert = d[1].isoformat()  # Ensure consistency in format
#         #     if date_to_insert not in all_dates:  # Check if the date already exists
#         #         continue  # Skip this iteration if the date is not in all_dates
#         #     index = all_dates.index(date_to_insert)
#         #     not_completed_tasks[index] = {'date': date_to_insert, 'value': d[0]}
#         # At this point, completed_tasks and not_completed_tasks contain all dates, filled with actual data where available
#         # You can proceed to process these lists as needed
#     else:
#         # Handle cases where there are no dates available
#         print("No dates available for processing.")

#     # Remember to close the cursor and connection
#     cursor.close()
#     connection.close()
    

#     # Render the template with the data
#     return render(request, 'dashboard.html', {'completed_tasks': json.dumps(complete_final_data_list), 'not_completed_tasks': json.dumps(not_complete_final_data_list)})





from datetime import date as dt


#to display from earliest to latest then change this part
#            current_date = earliest_date
#            today_ = dt.today()
#            # print('today =',today_, 'type: ',type(today_),' current_date=',type(current_date))
#            # print(start_date,end_date)
#            while current_date<=today_:
# while condition to latest_date




@login_required
def dashboard(request):
    connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mmh13138",
                database="learners"
            )
    cursor = connection.cursor()
    user = str(request.user)

    # Query for completed tasks
    query_completed = '''SELECT COUNT(*) as completed_task_count, date,status
                         FROM learners.timetable
                         WHERE status = 'Completed' AND user_id = %s
                         GROUP BY date
                         ORDER BY date ASC;'''
    cursor.execute(query_completed, (user,))
    completed_task_data = cursor.fetchall()

    # Query for not completed tasks
    query_not_completed = '''SELECT COUNT(*) as completed_task_count, date,status
                             FROM learners.timetable
                             WHERE status = 'Not Done' AND user_id = %s
                             GROUP BY date
                             ORDER BY date ASC;'''
    cursor.execute(query_not_completed, (user,))
    not_completed_task_data = cursor.fetchall()

    if completed_task_data and not_completed_task_data:
    # Close the cursor and connection
        earliest_date = min([min(d[1] for d in completed_task_data), min(d[1] for d in not_completed_task_data)], default=None)
        latest_date = max([max(d[1] for d in completed_task_data), max(d[1] for d in not_completed_task_data)], default=None)

        if earliest_date and latest_date:
            # Directly use earliest_date and latest_date as datetime.date objects
            # start_date = datetime.combine(earliest_date, datetime.min.time())  # Combine date with minimum time to get a datetime object
            # end_date = datetime.combine(latest_date, datetime.max.time())  # Combine date with maximum time to get a datetime object
            # num_days = (end_date - start_date).days + 1
            # print('earliest_date: ',type(earliest_date), earliest_date)
            # # Generate a list of all dates between the earliest and latest dates
            # all_dates = [(start_date + timedelta(days=i)).isoformat() for i in range(num_days)]

            # Create empty lists for completed and not completed tasks
            # completed_tasks = [{'date': '', 'value': 0} for _ in all_dates]
            # not_completed_tasks = [{'date': '', 'value': 0} for _ in all_dates]
            dates_str =[]
            current_date = earliest_date
            today_ = dt.today()
            # print('today =',today_, 'type: ',type(today_),' current_date=',type(current_date))
            # print(start_date,end_date)
            while current_date<=today_:
                dates_str.append(current_date.isoformat())
                current_date += timedelta(days=1)
            print("dates_str = ",dates_str)
            
            
            # Populate the lists with actual data
            # for d in completed_task_data:
            #     date_in_d = d[1].isoformat()  
            #     # for j in dates_str:
            #     #     print("J value =",j)
            #     #     if date_in_d==j:
            #     #         print("date in d : ",date_in_d,"------- date in j",j)
            #     #         final_data_list.append({'date': j, 'value': d[0]})
            #     #         break
            #     #     else:
            #     #         # If the date was not found, append a dictionary with value 0
            #     #         final_data_list.append({'date': j, 'value': 0})
            #     if date_in_d in dates_str:
            #         print(str(date_in_d))
            #         final_data_list.append({'date':str(date_in_d),'value':d[0]})
            complete_final_data_list = []

    # Iterate through dates_str
            for date_str in dates_str:
                # Initialize a flag to False
                found = False
                # Try to find the date in completed_task_data
                for d in completed_task_data:
                    if d[1].isoformat() == date_str:
                        # If found, set the flag to True and store the value
                        found = True
                        value = d[0]
                        break  # Exit the loop since we found a match
                # After the loop, check the flag to decide what to append
                if found:
                    # If found, append the date and its value to final_data_list
                    complete_final_data_list.append({'date': date_str, 'value': value})
                else:
                    # If not found, append the date with a value of 0
                    complete_final_data_list.append({'date': date_str, 'value': 0})



            
                                
            
            
            
            
            not_complete_final_data_list = []

    # Iterate through dates_str
            for date_str in dates_str:
                # Initialize a flag to False
                found = False
                # Try to find the date in completed_task_data
                for d in not_completed_task_data:
                    if d[1].isoformat() == date_str:
                        # If found, set the flag to True and store the value
                        found = True
                        value = d[0]
                        break  # Exit the loop since we found a match
                # After the loop, check the flag to decide what to append
                if found:
                    # If found, append the date and its value to final_data_list
                    not_complete_final_data_list.append({'date': date_str, 'value': value})
                else:
                    # If not found, append the date with a value of 0
                    not_complete_final_data_list.append({'date': date_str, 'value': 0})



            
                                
            print(not_complete_final_data_list)
                        
                # if date_to_insert not in all_dates:  # Check if the date already exists
                #     continue  # Skip this iteration if the date is not in all_dates
                # index = all_dates.index(date_to_insert)
                # completed_tasks[index] = {'date': date_to_insert, 'value': d[0]}

            # for d in not_completed_task_data:
            #     date_to_insert = d[1].isoformat()  # Ensure consistency in format
            #     if date_to_insert not in all_dates:  # Check if the date already exists
            #         continue  # Skip this iteration if the date is not in all_dates
            #     index = all_dates.index(date_to_insert)
            #     not_completed_tasks[index] = {'date': date_to_insert, 'value': d[0]}
            # At this point, completed_tasks and not_completed_tasks contain all dates, filled with actual data where available
            # You can proceed to process these lists as needed
        else:
            # Handle cases where there are no dates available
            print("No dates available for processing.")

        # Remember to close the cursor and connection
        cursor.close()
        connection.close()
        

        # Render the template with the data
        return render(request, 'dashboard.html', {'completed_tasks': json.dumps(complete_final_data_list), 'not_completed_tasks': json.dumps(not_complete_final_data_list)})
    elif completed_task_data:
        earliest_date = min(d[1] for d in completed_task_data)
        latest_date = max(d[1] for d in completed_task_data)

        if earliest_date and latest_date:
            dates_str =[]
            current_date = earliest_date
            today_ = dt.today()
            # print('today =',today_, 'type: ',type(today_),' current_date=',type(current_date))
            # print(start_date,end_date)
            while current_date<=today_:
                dates_str.append(current_date.isoformat())
                current_date += timedelta(days=1)
            print("dates_str = ",dates_str)
            complete_final_data_list = []

    # Iterate through dates_str
            for date_str in dates_str:
                # Initialize a flag to False
                found = False
                # Try to find the date in completed_task_data
                for d in completed_task_data:
                    if d[1].isoformat() == date_str:
                        # If found, set the flag to True and store the value
                        found = True
                        value = d[0]
                        break  # Exit the loop since we found a match
                # After the loop, check the flag to decide what to append
                if found:
                    # If found, append the date and its value to final_data_list
                    complete_final_data_list.append({'date': date_str, 'value': value})
                else:
                    # If not found, append the date with a value of 0
                    complete_final_data_list.append({'date': date_str, 'value': 0})

            not_complete_final_data_list=[{'date':'', "value":0}]
            
        else:
            # Handle cases where there are no dates available
            print("No dates available for processing.")

        # Remember to close the cursor and connection
        cursor.close()
        connection.close()
        

        # Render the template with the data
        return render(request, 'dashboard.html', {'completed_tasks': json.dumps(complete_final_data_list), 'not_completed_tasks': json.dumps(not_complete_final_data_list)})
    elif not_completed_task_data:
        earliest_date = min(d[1] for d in not_completed_task_data)
        latest_date = max(d[1] for d in not_completed_task_data)

        if earliest_date and latest_date:
            dates_str =[]
            current_date = earliest_date
            today_ = dt.today()
            # print('today =',today_, 'type: ',type(today_),' current_date=',type(current_date))
            # print(start_date,end_date)
            while current_date<=today_:
                dates_str.append(current_date.isoformat())
                current_date += timedelta(days=1)
            print("dates_str = ",dates_str)
            not_complete_final_data_list = []

    # Iterate through dates_str
            for date_str in dates_str:
                # Initialize a flag to False
                found = False
                # Try to find the date in completed_task_data
                for d in not_completed_task_data:
                    if d[1].isoformat() == date_str:
                        # If found, set the flag to True and store the value
                        found = True
                        value = d[0]
                        break  # Exit the loop since we found a match
                # After the loop, check the flag to decide what to append
                if found:
                    # If found, append the date and its value to final_data_list
                    not_complete_final_data_list.append({'date': date_str, 'value': value})
                else:
                    # If not found, append the date with a value of 0
                    not_complete_final_data_list.append({'date': date_str, 'value': 0})

            complete_final_data_list=[{'date':'', 'value':0}]
            
        else:
            # Handle cases where there are no dates available
            print("No dates available for processing.")

        # Remember to close the cursor and connection
        cursor.close()
        connection.close()
        

        # Render the template with the data
        return render(request, 'dashboard.html', {'completed_tasks': json.dumps(complete_final_data_list), 'not_completed_tasks': json.dumps(not_complete_final_data_list)})
    else:
        complete_final_data_list=[{'date':'', 'value':0}]
        not_complete_final_data_list=[{'date':'', 'value':0}]
        
        return render(request, 'dashboard.html', {'completed_tasks': json.dumps(complete_final_data_list), 'not_completed_tasks': json.dumps(not_complete_final_data_list)})
        




def notes(request):
    return render(request,'notes.html')



from notes.models import Note
from bson.json_util import dumps
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import uuid
from django.http import HttpResponseBadRequest

@csrf_exempt
def save_notes(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user
        
        # Save text content
        note = Note(user=user, content=content)
        note.save()

        # Assuming you have a way to get the uploaded image(s) from the request
        # This part is highly dependent on how you're handling file uploads
        # For simplicity, let's assume you're uploading a single image per note
        image_file = request.FILES.get('image')
        if image_file:
            filename = f"{uuid.uuid4()}.jpg"
            with default_storage.open(filename, "wb") as f:
                f.write(image_file.read())

            # Save the image URL to the note
            note.image_url = filename
            note.save()

        return redirect('/notes/')
    else:
        return HttpResponseBadRequest("Invalid request")
    
    
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import uuid

@csrf_exempt
def upload_image(request):
    if request.is_ajax():
        form = request.FILES.get('file')
        if form:
            filename = f"uploads/{uuid.uuid4()}.{form.name.split('.')[-1]}"
            with default_storage.open(filename, 'wb+') as dest:
                dest.write(form.read())
            return JsonResponse({'location': request.build_absolute_uri(filename)})
    return JsonResponse({}, status=401)



from django.shortcuts import render, redirect
from.forms import NoteForm
from notes.models import Note,Article
import os

import sqlite3


@login_required
def create_note(request):

    
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            if request.FILES.get('image'):
                filename = request.FILES['image'].name
                filepath = os.path.join('media/images/', filename)
                with open(filepath, 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
                note.image_path = filepath
                
            note.user = request.user
            note.save()
            print("IN IF")
            notes = Article.objects.all()
            notes_data = list(n for n in notes)
            return redirect('/new_notes/', {'notes':notes_data})
    else:
        form = NoteForm()
        print("In else: ")
    print(request.method)
    print("Notes data:")
    user_id = request.user.id
    notes = Article.objects.filter(user_id=user_id)
    for note in notes:
        print(note.title)
        print(note.user_id)
        
    return render(request, 'notes.html', {'form': form,'notes':notes})



# views.py
from django.shortcuts import get_object_or_404, render
from notes.models import Article  
def note_detail(request, note_id):
    note = get_object_or_404(Article, pk=note_id)
    return render(request, 'note_detail.html', {'note': note,'MEDIA_URL': settings.MEDIA_URL})


def delete_confirm(request):
    return render(request, 'delete_confirmation.html')
@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Article, pk=note_id)
    if request.method == 'POST':
        note.delete()
        return redirect('/new_notes/')  
    return render(request, 'delete_confirmation.html', {'note': note})
