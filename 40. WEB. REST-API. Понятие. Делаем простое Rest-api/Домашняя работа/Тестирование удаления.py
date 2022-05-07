from requests import delete, get, post

# Добавляем работу
print(
    post(
        "http://localhost:5000/api/jobs",
        json={
            "id": 10,
            "team_leader": 1,
            "job": "test",
            "work_size": 45,
            "collaborators": "1,3",
            "start_date": "21.04.2021",
            "end_date": "25.04.2021",
            "is_finished": False,
            "creator": 1,
        },
    ).json()
)

# работы с id = 999 нет в базе
print(delete("http://localhost:5000/api/jobs/999").json())

# Неверный параметр - q
print(delete("http://localhost:5000/api/jobs/q").json())

# Удаляем работу
print(delete("http://localhost:5000/api/jobs/10").json())

# Все работы
print(get("http://localhost:5000/api/jobs").json())
