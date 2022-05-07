from requests import get, post, put

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

# Не указан id вопроса, который нужно изменить
print(
    put(
        "http://localhost:5000/api/jobs",
        json={"work_size": 55, "end_date": "27.04.2021"},
    ).json()
)

# Пустой json
print(put("http://localhost:5000/api/jobs").json())

# Указан неверный id
print(
    put(
        "http://localhost:5000/api/jobs",
        json={"id": 999, "work_size": 55, "end_date": "27.04.2021"},
    ).json()
)

# Изменяет work_size = 55 и end_date
print(
    put(
        "http://localhost:5000/api/jobs",
        json={"id": 10, "work_size": 55, "end_date": "27.04.2021"},
    ).json()
)

# Все работы
print(get("http://localhost:5000/api/jobs").json())
