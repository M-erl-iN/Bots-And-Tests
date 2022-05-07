from requests import get, post

# Пустой json
print(post("http://localhost:5000/api/jobs").json())

# Не все параметры для добавления работы
print(
    post(
        "http://localhost:5000/api/jobs",
        json={
            "title": "Заголовок"
        },
    ).json()
)

# Работа с таким id уже есть
print(
    post(
        "http://localhost:5000/api/jobs",
        json={
            "id": 1,
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

# Верный запрос
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

# Все работы
print(get("http://localhost:5000/api/jobs").json())
