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
    return redirect('/get/')