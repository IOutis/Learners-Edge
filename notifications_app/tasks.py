from celery import shared_task
from notifications.signals import notify
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from notifications_app.utils import get_current_username
@shared_task(bind=True)
def test_func(self,user):
    user = User.objects.get(username=user)
    # user_mode = get_user_model()
    # username = user_mode.get_username()
    username1 = get_current_username()
    # Iterate over each user and print their username
    print(str(user))
    print(username1)
    message = 'you reached level 105'+str(user)
    notify.send(user,recipient=user, verb=message)
    return "Done"



from celery import shared_task
import mysql.connector
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware,now,get_current_timezone

@shared_task
def process_timetable_deadlines():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mmh13138",
        database="learners"
    )
    cursor = connection.cursor()
    query = "SELECT * FROM timetable WHERE status != 'Not Done' ORDER BY date, time_slot"
    cursor.execute(query)
    fetched_data = cursor.fetchall()
    
    print(get_current_timezone())
    # Process the fetched data and send notifications for approaching deadlines
    # now = timezone.now()
    if not fetched_data:
        # Handle case where there are no tasks in the timetable
        print(f"No tasks found in the timetable for user {user_id}")
        return
    
    first_task = fetched_data[0]
    _, user_id, time_slot, task_activity, _, status, _, _, _, date = first_task
    time_slot = (datetime.min + time_slot).time()
    task_datetime = datetime.combine(date, time_slot)
    task_datetime = make_aware(task_datetime)
    current_datetime = now()
    current_time = current_datetime.time()

    # Extract time component from task_datetime
    task_time = task_datetime.time()

    # Combine current_time with current_date to create a datetime.datetime object
    current_datetime_with_time = current_datetime.replace(hour=current_time.hour, minute=current_time.minute, second=current_time.second, microsecond=current_time.microsecond)

    # Now you can add timedelta to current_datetime_with_time
    future_time = current_datetime_with_time + timedelta(minutes=5)
    future_time= future_time.time()
    print(type(task_time))
    print(type(current_time))
    print(type(future_time))
    print(current_time)
    # Check if the deadline of the first task is approaching
    if date == current_datetime.date():
        print("In first condition")
        if current_time <= task_time <= future_time:
            # Send notification for approaching deadline
            message = f"Task '{task_activity}' deadline is approaching!"
            notify.send(user_id, recipient=user_id, verb=message)
            print("If condition is true")
        elif task_time<current_time:
            update_query = "UPDATE timetable SET status = 'Not Done' WHERE id = %s"
            cursor.execute(update_query, (first_task[0],))  # Assuming id is the first column
            connection.commit()
            print("Status updated")
        
        
    # for row in fetched_data:
    #     print("Here")
    #     id, user_id, time_slot, task_activity, description, status, recurring, created_at,updated_at, date = row
    #     time_slot = (datetime.min + time_slot).time()
    #     print(user_id)
    #     task_datetime = datetime.combine(date, time_slot)
    #     print(time_slot)
    #     task_datetime= make_aware(task_datetime)
    #     if task_datetime <= now + timedelta(minutes=5) <= task_datetime:
    #         print("HELLOO")
    #         break

        #     # Send notification for approaching deadline
        #     message=f"Task '{task_activity}' deadline is approaching!"
        #     notify.send(user_id,recipient=user_id, verb=message)
        #     # Break the loop after sending the first notification
        #     break

    # Close the cursor and connection
    cursor.close()
    connection.close()
