import random

import psycopg2
from faker import Faker


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "mysecretpassword",
}


fake = Faker()


def seed_database():
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Generate users
    users = []

    for _ in range(20):
        users.append(
            (
                fake.name(),
                fake.unique.email(),
            )
        )

    cursor.executemany(
        """
        INSERT INTO users (fullname, email)
        VALUES (%s, %s);
        """,
        users,
    )

    # Get user IDs
    cursor.execute("SELECT id FROM users;")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Get status IDs
    cursor.execute("SELECT id FROM status;")
    status_ids = [row[0] for row in cursor.fetchall()]

    # Generate tasks
    tasks = []

    for _ in range(50):
        title = fake.sentence(nb_words=5)
        description = fake.paragraph()
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)

        tasks.append(
            (
                title,
                description,
                status_id,
                user_id,
            )
        )

    cursor.executemany(
        """
        INSERT INTO tasks (
            title,
            description,
            status_id,
            user_id
        )
        VALUES (%s, %s, %s, %s);
        """,
        tasks,
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("Database seeded successfully.")
    print("Created 20 users and 50 tasks.")


if __name__ == "__main__":
    seed_database()