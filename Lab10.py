# name: YOUR NAME HERE
# date:
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5 (out of 5) --f I don't change this, I agree to get 0 points. i

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('reading_list')

def create_book():
    """
    Prompt user for a Movie Title.
    Add the movie to the database with the title and an empty Ratings list.
    """
    title = input("What book would you like to add?")
    print("creating a book")

    response = table.put_item(
        Item={
            'pk': f"{title}",
        }
    )
    return response


def print_book(book):
    title = book.get("pk", "Unknown Title")
    author = book.get("Author", "Unknown Author")
    Publishing_Date = book.get("Publishing Date", "No Date")

    print(f"  Title  : {title}")
    print(f"  Year   : {author}")
    print(f"  Ratings: {Publishing_Date}")
    print()

def print_all_books():
    """Scan the entire Movies table and print each item."""
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No books found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} book(s):\n")
    for book in items:
        print_book(book)

def update_publication_date():
    try:
        title = input("What is the book title? ")
        publication_date = int(input("What is the new publication date? (integer): "))
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Publication Date, :r)",
            ExpressionAttributeValues={':r': [publication_date]}
        )
    except:
        print("error in updating book publication date.")

def delete_book():
    """
    Prompt user for a Movie Title.
    Delete that item from the database.
    """
    try:
        title = input("Which book do you want to delete? ")
        table.delete_item(
            Key={
                'Title': title
            }
        )
    except:
        print("failed in deleting book.")

def query_book():
    """
    Prompt user for a Movie Title.
    Print out the average of all ratings in the movie's Ratings list.
    """
    try:
        title = input("What book do you want to query? ")
        response = table.get_item(Key={"Title": title})
        book = response.get("Item")
        print_book(book)
            
    except:
        print("book not found")


def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new book")
    print("Press R: to READ all books")
    print("Press U: to UPDATE a book (change publication date)")
    print("Press D: to DELETE a book")
    print("Press Q: to QUERY a books information")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_book()
        elif input_char.upper() == "R":
            print_all_books()
        elif input_char.upper() == "U":
            update_publication_date()
        elif input_char.upper() == "D":
            delete_book()
        elif input_char.upper() == "Q":
            query_book()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
