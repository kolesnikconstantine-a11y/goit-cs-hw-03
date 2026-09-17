import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "mysecretpassword",
}


def print_results(cursor, title):
    """Print query results in a readable format."""
    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)

    rows = cursor.fetchall()

    if not rows:
        print("No results found.")
        return

    columns = [description[0] for description in cursor.description]

    print(" | ".join(columns))
    print("-" * 60)

    for row in rows:
        print(" | ".join(str(value) for value in row))


# ============================================================
# 1. Get all tasks of a specific user
# ============================================================

def get_user_tasks(cursor, user_id):
    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE user_id = %s;
        """,
        (user_id,),
    )

    print_results(
        cursor,
        f"1. Tasks of user with id = {user_id}",
    )


# ============================================================
# 2. Get tasks with a specific status
# Using a subquery
# ============================================================

def get_tasks_by_status(cursor, status_name):
    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE status_id = (
            SELECT id
            FROM status
            WHERE name = %s
        );
        """,
        (status_name,),
    )

    print_results(
        cursor,
        f"2. Tasks with status = '{status_name}'",
    )


# ============================================================
# 3. Change the status of a specific task
# ============================================================

def update_task_status(cursor, task_id, status_name):
    cursor.execute(
        """
        UPDATE tasks
        SET status_id = (
            SELECT id
            FROM status
            WHERE name = %s
        )
        WHERE id = %s;
        """,
        (status_name, task_id),
    )

    print(
        f"\n3. Task {task_id} status changed "
        f"to '{status_name}'."
    )


# ============================================================
# 4. Get users who have no tasks
# Using WHERE NOT IN and a subquery
# ============================================================

def get_users_without_tasks(cursor):
    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id NOT IN (
            SELECT user_id
            FROM tasks
        );
        """
    )

    print_results(
        cursor,
        "4. Users without tasks",
    )


# ============================================================
# 5. Add a new task for a specific user
# ============================================================

def add_task(cursor, user_id):
    cursor.execute(
        """
        INSERT INTO tasks (
            title,
            description,
            status_id,
            user_id
        )
        VALUES (
            %s,
            %s,
            (
                SELECT id
                FROM status
                WHERE name = %s
            ),
            %s
        )
        RETURNING id, title, description, status_id, user_id;
        """,
        (
            "Prepare project report",
            "Prepare the final report for the project.",
            "new",
            user_id,
        ),
    )

    print_results(
        cursor,
        f"5. New task for user {user_id}",
    )


# ============================================================
# 6. Get all tasks that are not completed
# ============================================================

def get_not_completed_tasks(cursor):
    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE status_id != (
            SELECT id
            FROM status
            WHERE name = 'completed'
        );
        """
    )

    print_results(
        cursor,
        "6. Tasks that are not completed",
    )


# ============================================================
# 7. Delete a specific task
# ============================================================

def delete_task(cursor, task_id):
    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = %s
        RETURNING id, title;
        """,
        (task_id,),
    )

    print_results(
        cursor,
        f"7. Deleted task with id = {task_id}",
    )


# ============================================================
# 8. Find users by email
# ============================================================

def find_users_by_email(cursor, email_part):
    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email LIKE %s;
        """,
        (f"%{email_part}%",),
    )

    print_results(
        cursor,
        f"8. Users with email containing '{email_part}'",
    )


# ============================================================
# 9. Update a user's name
# ============================================================

def update_user_name(cursor, user_id, new_name):
    cursor.execute(
        """
        UPDATE users
        SET fullname = %s
        WHERE id = %s
        RETURNING id, fullname, email;
        """,
        (new_name, user_id),
    )

    print_results(
        cursor,
        f"9. Updated user with id = {user_id}",
    )


# ============================================================
# 10. Get the number of tasks for each status
# Using COUNT and GROUP BY
# ============================================================

def get_task_count_by_status(cursor):
    cursor.execute(
        """
        SELECT
            s.name AS status,
            COUNT(t.id) AS task_count
        FROM status AS s
        LEFT JOIN tasks AS t
            ON s.id = t.status_id
        GROUP BY s.id, s.name
        ORDER BY s.id;
        """
    )

    print_results(
        cursor,
        "10. Number of tasks for each status",
    )


# ============================================================
# 11. Get tasks assigned to users with a specific email domain
# Using JOIN and LIKE
# ============================================================

def get_tasks_by_email_domain(cursor, domain):
    cursor.execute(
        """
        SELECT
            t.id AS task_id,
            t.title,
            u.fullname,
            u.email
        FROM tasks AS t
        INNER JOIN users AS u
            ON t.user_id = u.id
        WHERE u.email LIKE %s;
        """,
        (f"%{domain}",),
    )

    print_results(
        cursor,
        f"11. Tasks of users with domain '{domain}'",
    )


# ============================================================
# 12. Get tasks without a description
# ============================================================

def get_tasks_without_description(cursor):
    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE description IS NULL;
        """
    )

    print_results(
        cursor,
        "12. Tasks without a description",
    )


# ============================================================
# 13. Get users and their tasks with 'in progress' status
# Using INNER JOIN
# ============================================================

def get_in_progress_tasks(cursor):
    cursor.execute(
        """
        SELECT
            u.id AS user_id,
            u.fullname,
            t.id AS task_id,
            t.title
        FROM users AS u
        INNER JOIN tasks AS t
            ON u.id = t.user_id
        INNER JOIN status AS s
            ON t.status_id = s.id
        WHERE s.name = 'in progress';
        """
    )

    print_results(
        cursor,
        "13. Users and their 'in progress' tasks",
    )


# ============================================================
# 14. Get users and the number of their tasks
# Using LEFT JOIN and GROUP BY
# ============================================================

def get_user_task_counts(cursor):
    cursor.execute(
        """
        SELECT
            u.id,
            u.fullname,
            COUNT(t.id) AS task_count
        FROM users AS u
        LEFT JOIN tasks AS t
            ON u.id = t.user_id
        GROUP BY u.id, u.fullname
        ORDER BY u.id;
        """
    )

    print_results(
        cursor,
        "14. Users and number of their tasks",
    )


# ============================================================
# Main program
# ============================================================

def main():
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    try:
        # Read operations
        get_user_tasks(cursor, 1)

        get_tasks_by_status(cursor, "new")

        get_users_without_tasks(cursor)

        get_not_completed_tasks(cursor)

        find_users_by_email(cursor, "@example.com")

        get_task_count_by_status(cursor)

        get_tasks_by_email_domain(cursor, "@example.com")

        get_tasks_without_description(cursor)

        get_in_progress_tasks(cursor)

        get_user_task_counts(cursor)

        # Update / insert / delete operations
        update_task_status(cursor, 1, "in progress")

        add_task(cursor, 1)

        update_user_name(
            cursor,
            1,
            "John Smith",
        )

        delete_task(cursor, 10)

        connection.commit()

    except Exception as error:
        connection.rollback()
        print(f"\nError: {error}")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()