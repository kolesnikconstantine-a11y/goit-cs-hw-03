import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "mysecretpassword",
}


def create_tables():
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Create users table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
        """
    )

    # Create status table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
        """
    )

    # Create tasks table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,

            CONSTRAINT fk_task_status
                FOREIGN KEY (status_id)
                REFERENCES status(id),

            CONSTRAINT fk_task_user
                FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        );
        """
    )

    # Insert initial statuses
    cursor.execute(
        """
        INSERT INTO status (name)
        VALUES
            ('new'),
            ('in progress'),
            ('completed')
        ON CONFLICT (name) DO NOTHING;
        """
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("Tables created successfully.")


if __name__ == "__main__":
    create_tables()