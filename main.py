from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError


# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017/"

DATABASE_NAME = "cats_database"
COLLECTION_NAME = "cats"


def connect_to_database():
    """Connect to MongoDB and return the cats collection."""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

        # Check that MongoDB is available
        client.admin.command("ping")

        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        print("Successfully connected to MongoDB.")
        return collection

    except ConnectionFailure:
        print("Error: Could not connect to MongoDB.")
        return None


def create_cat(collection, name, age, features):
    """Create a new cat document."""
    try:
        cat = {
            "name": name,
            "age": age,
            "features": features
        }

        result = collection.insert_one(cat)

        print(f"Cat '{name}' was added.")
        print(f"ID: {result.inserted_id}")

    except PyMongoError as error:
        print(f"Error while adding cat: {error}")


def read_all_cats(collection):
    """Display all cats from the collection."""
    try:
        cats = collection.find()

        print("\nAll cats:")

        found = False

        for cat in cats:
            found = True
            print(
                f"ID: {cat['_id']}\n"
                f"Name: {cat['name']}\n"
                f"Age: {cat['age']}\n"
                f"Features: {', '.join(cat['features'])}\n"
            )

        if not found:
            print("The collection is empty.")

    except PyMongoError as error:
        print(f"Error while reading cats: {error}")


def find_cat_by_name(collection):
    """Find and display a cat by its name."""
    name = input("Enter the cat's name: ")

    try:
        cat = collection.find_one({"name": name})

        if cat:
            print("\nCat found:")
            print(f"ID: {cat['_id']}")
            print(f"Name: {cat['name']}")
            print(f"Age: {cat['age']}")
            print(f"Features: {', '.join(cat['features'])}")
        else:
            print(f"Cat '{name}' was not found.")

    except PyMongoError as error:
        print(f"Error while searching for cat: {error}")


def update_cat_age(collection):
    """Update a cat's age by its name."""
    name = input("Enter the cat's name: ")

    try:
        age = int(input("Enter the new age: "))

        result = collection.update_one(
            {"name": name},
            {"$set": {"age": age}}
        )

        if result.matched_count:
            print(f"Age of cat '{name}' was updated.")
        else:
            print(f"Cat '{name}' was not found.")

    except ValueError:
        print("Error: age must be an integer.")

    except PyMongoError as error:
        print(f"Error while updating age: {error}")


def add_feature(collection):
    """Add a new feature to a cat's features list."""
    name = input("Enter the cat's name: ")
    feature = input("Enter a new feature: ")

    try:
        result = collection.update_one(
            {"name": name},
            {"$addToSet": {"features": feature}}
        )

        if result.matched_count:
            if result.modified_count:
                print(f"Feature '{feature}' was added to '{name}'.")
            else:
                print(f"Feature '{feature}' already exists.")
        else:
            print(f"Cat '{name}' was not found.")

    except PyMongoError as error:
        print(f"Error while adding feature: {error}")


def delete_cat(collection):
    """Delete a cat by its name."""
    name = input("Enter the cat's name: ")

    try:
        result = collection.delete_one({"name": name})

        if result.deleted_count:
            print(f"Cat '{name}' was deleted.")
        else:
            print(f"Cat '{name}' was not found.")

    except PyMongoError as error:
        print(f"Error while deleting cat: {error}")


def delete_all_cats(collection):
    """Delete all cats from the collection."""
    try:
        result = collection.delete_many({})

        print(f"Deleted {result.deleted_count} cats.")

    except PyMongoError as error:
        print(f"Error while deleting cats: {error}")


def main():
    """Run the MongoDB CRUD application."""
    collection = connect_to_database()

    if collection is None:
        return

    while True:
        print("\n========== CAT DATABASE ==========")
        print("1. Add a cat")
        print("2. Show all cats")
        print("3. Find a cat by name")
        print("4. Update cat's age")
        print("5. Add a feature")
        print("6. Delete a cat")
        print("7. Delete all cats")
        print("0. Exit")
        print("=================================")

        choice = input("Choose an operation: ")

        if choice == "1":
            name = input("Enter cat's name: ")

            try:
                age = int(input("Enter cat's age: "))
            except ValueError:
                print("Error: age must be an integer.")
                continue

            features_input = input(
                "Enter features separated by commas: "
            )

            features = [
                feature.strip()
                for feature in features_input.split(",")
                if feature.strip()
            ]

            create_cat(collection, name, age, features)

        elif choice == "2":
            read_all_cats(collection)

        elif choice == "3":
            find_cat_by_name(collection)

        elif choice == "4":
            update_cat_age(collection)

        elif choice == "5":
            add_feature(collection)

        elif choice == "6":
            delete_cat(collection)

        elif choice == "7":
            delete_all_cats(collection)

        elif choice == "0":
            print("Program finished.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
