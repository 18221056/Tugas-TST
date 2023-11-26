from database.connection import database
from datetime import datetime, date
from service import get_current_user
from fastapi import Depends
import pytz

collection_task = database["tasks"]
collection_user = database["users"] 

deadline = date(2023, 11, 25)

def seed_create_users():
    '''
    inisisalisasi data awal users
    
    semua password = test
    '''
    print("creating users..................")
    
    try:
        
        users = [
            {
                "id": "c3fe330d-032e-4f87-bd57-1e3bfe694816",
                "email": "ana@gmail.com",
                "username": "ana",
                "password": "JDJiJDEyJEFBUy4vRDg3NnRrWS5Kb29Hc0JCMXVPQ0cyVjFDcjM4cnVGVVA1Q1cwRmZ0YU9nN2FNUUZx",
                "role": "teacher",
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "29b9cf5f-8a25-4314-aed0-42a9247db25a",
                "email": "bob@gmail.com",
                "username": "bob",
                "password": "JDJiJDEyJEFBUy4vRDg3NnRrWS5Kb29Hc0JCMXVPQ0cyVjFDcjM4cnVGVVA1Q1cwRmZ0YU9nN2FNUUZx",
                "role": "teacher",
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "e8712b46-eb1a-42b1-8c6f-15a9e48114d8",
                "email": "sri@gmail.com",
                "username": "sri",
                "password": "JDJiJDEyJEFBUy4vRDg3NnRrWS5Kb29Hc0JCMXVPQ0cyVjFDcjM4cnVGVVA1Q1cwRmZ0YU9nN2FNUUZx",
                "role": "user",
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "4a4b7e8e-0214-4ea2-b0a7-48d23e1027e0",
                "email": "don@gmail.com",
                "username": "don",
                "password": "JDJiJDEyJEFBUy4vRDg3NnRrWS5Kb29Hc0JCMXVPQ0cyVjFDcjM4cnVGVVA1Q1cwRmZ0YU9nN2FNUUZx",
                "role": "user",
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "7881b520-7852-4a14-bca2-5f457bf836c9",
                "email": "carol@gmail.com",
                "username": "carol",
                "password": "JDJiJDEyJEFBUy4vRDg3NnRrWS5Kb29Hc0JCMXVPQ0cyVjFDcjM4cnVGVVA1Q1cwRmZ0YU9nN2FNUUZx",
                "role": "teacher",
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            }
        ]
        
        result = collection_user.insert_many(users)

        print("Inserted IDs:", result.inserted_ids)
        return {"message": "successfully inserted users"}
    
    except Exception as e:
        message = f"Error inserting  tasks: {e}"
        print(message)
        return message
    
def seed_create_tasks():
    '''
    inisisalisasi data awal tasks
    '''
    print("creating tasks..................")
    
    try:
    
        tasks = [
            {
                "id": "e636a3ac-5b24-4e4d-ba4d-05a76be3e78e",
                "title": "Learn Python",
                "description": "Python programming language basics",
                "deadline": datetime.combine(deadline, datetime.min.time()),
                "level": "medium",
                "category": "programming",
                "status": "completed",
                "user_id": ["7881b520-7852-4a14-bca2-5f457bf836c9"],
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "3df2cd4e-83c2-4ad8-8396-6b91a4f9ee84",
                "title": "Build a Web App",
                "description": "Create a simple web application",
                "deadline": datetime.combine(deadline, datetime.min.time()),
                "level": "high",
                "category": "web development",
                "status": "on progress",
                "user_id": ["29b9cf5f-8a25-4314-aed0-42a9247db25a"],
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "fc62fc58-9f0c-4eb2-b441-6366dbd4e1c5",
                "title": "Learn Data Science",
                "description": "Study data analysis and visualization",
                "deadline": datetime.combine(deadline, datetime.min.time()),
                "level": "low",
                "category": "data science",
                "status": "not completed",
                "user_id": ["c3fe330d-032e-4f87-bd57-1e3bfe694816"],
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "9cfb66b8-5347-4f1a-9cc3-c5f8f43a65f4",
                "title": "Practice Algorithms",
                "description": "Solve algorithmic problems",
                "deadline": datetime.combine(deadline, datetime.min.time()),
                "level": "medium",
                "category": "programming",
                "status": "completed",
                "user_id": ["7881b520-7852-4a14-bca2-5f457bf836c9"],
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "8e93a5af-0437-44cc-b2bf-61a2fc29d3e2",
                "title": "Build a Mobile App",
                "description": "Develop a mobile application",
                "deadline": datetime.combine(deadline, datetime.min.time()),
                "level": "low",
                "category": "mobile development",
                "status": "on progress",
                "user_id": ["29b9cf5f-8a25-4314-aed0-42a9247db25a"],
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "b13d7e5d-d7bf-4e77-b99f-5ce7bc6f9f27",
                "title": "Learn Machine Learning",
                "description": "Explore machine learning concepts",
                "deadline": datetime.combine(deadline, datetime.min.time()),
                "level": "high",
                "category": "machine learning",
                "status": "completed",
                "user_id": ["c3fe330d-032e-4f87-bd57-1e3bfe694816"],
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "0f12e396-9a77-4e77-881e-4ba1da1572c8",
                "title": "Practice Frontend Development",
                "description": "Improve skills in frontend technologies",
                "deadline": datetime.combine(deadline, datetime.min.time()),
                "level": "medium",
                "category": "web development",
                "status": "on progress",
                "user_id": ["7881b520-7852-4a14-bca2-5f457bf836c9"],
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "9a41708d-5e76-460b-95d7-3c2c527b5454",
                "title": "Build a REST API",
                "description": "Create a RESTful API",
                "deadline": datetime.combine(deadline, datetime.min.time()),
                "level": "high",
                "category": "web development",
                "status": "not completed",
                "user_id": ["c3fe330d-032e-4f87-bd57-1e3bfe694816"],
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "4b86441a-9021-48cd-97b3-4a773af3c098",
                "title": "Learn Cybersecurity",
                "description": "Study cybersecurity concepts",
                "deadline": datetime.combine(deadline, datetime.min.time()),
                "level": "low",
                "category": "security",
                "status": "completed",
                "user_id": ["29b9cf5f-8a25-4314-aed0-42a9247db25a"],
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "e0efc07f-512f-4f56-8f1a-4a87775f91c6",
                "title": "Practice Databases",
                "description": "Improve skills in working with databases",
                "deadline": datetime.combine(deadline, datetime.min.time()),
                "level": "medium",
                "category": "database",
                "status": "not completed",
                "user_id": ["c3fe330d-032e-4f87-bd57-1e3bfe694816"],
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            },
            {
                "id": "3fbc042f-8725-4f19-9d5d-fd7f8a2f2a82",
                "title": "Build a Chat Application",
                "description": "Create a real-time chat application",
                "deadline": datetime.combine(deadline, datetime.min.time()),
                "level": "high",
                "category": "web development",
                "status": "on progress",
                "user_id": ["7881b520-7852-4a14-bca2-5f457bf836c9"],
                "created_at": datetime.now(pytz.timezone("Asia/Jakarta")),
                "updated_at": datetime.now(pytz.timezone("Asia/Jakarta"))
            }
        ]
     
        result = collection_task.insert_many(tasks)
        
        print("Inserted IDs:", result.inserted_ids)
        return {"message": "successfully inserted tasks"}
    
    except Exception as e:
        message = f"Error inserting  tasks: {e}"
        print(message)
        return message