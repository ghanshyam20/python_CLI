import sqlite3
import csv

DB_NAME = "user.sqlite3"

FILE_NAME = "sample_users.csv"


COLUMNS=(
        "first_name",
        "last_name",
        "company_name",
        "address",
        "city",
        "county",
        "state",
        "zip",
        "phone1",
        "phone2",
        "email",
        "web",
)
        

        
        





def create_connection():

    try:

        con = sqlite3.connect(DB_NAME)

        return con

    except Error:
        print("connection error in sqlite")

    except Exception as e:
        print(e)


def create_table(con):

    CREATE_USERS_TABLE_QUERY = """


    CREATE TABLE IF NOT EXISTS users(
    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name CHAR(255) NOT NULL,

    last_name CHAR(255) NOT NULL,

    company_name CHAR(255) NOT NULL,

    address CHAR(255) NOT NULL,

    city CHAR(255) NOT NULL,

    county CHAR(255) NOT NULL,


    state CHAR(255) NOT NULL,


    zip REAL NOT NULL,

    phone1 CHAR(255) NOT NULL,

    phone2 CHAR(255) NOT NULL,

    


    email CHAR(255) NOT NULL,

    web text
    );


"""
    cur = con.cursor()

    cur.execute(CREATE_USERS_TABLE_QUERY)

    print("successfully created the users table.")


def insert_users(con, users):
    user_add_query = """

    INSERT INTO users
    (first_name,
    last_name,
    company_name,
    address,
    city,
    county,
    state,
    zip,
    phone1,
    phone2,
    email,
    

    
    web)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?);
    
    
    """

    cur = con.cursor()
    cur.executemany(user_add_query, users)
    con.commit()

    print(f"{len(users)}users were imported to table.")


def read_csv():

    with open(FILE_NAME) as f:

        parsed_data = []
        data = csv.reader(f)

        for user in data:

            parsed_data.append(tuple(user))
        return parsed_data[1:]


INPUT_STRING = """

Enter the option:
1. CREATE TABLE

 2. DUMP users from csv INTO users TABLE

3. ADD new user INTO users TABLE

4. QUERY all users from TABLE

 5. QUERY user by id from TABLE

6. QUERY specified no. of records from TABLE

7. DELETE all users

 8. DELETE user by id

 9. UPDATE user

10. Press any key to EXIT

"""


def select_users(con,no_of_records=0):

    cur=con.cursor()

    users=con.execute("SELECT * from users;")

    for i, user in enumerate(users):

        if no_of_records and no_of_records==i:
            break

        print(user)
       

def select_user_by_id(con,user_id):
    cur=con.cursor()

    users=con.execute("SELECT *from users where id=?;",(user_id,))
    for user in users:
        print(user)

def delete_user_by_id(con,user_id):
    cur=con.cursor()

    con.execute("DELETE from users where id=?;",(user_id))
    con.commit()
    print(f"User with id{user_id} was successfully deleted.")

def delete_all_users(con):
    cur=con.cursor()
    con.execute("DELETE from users;")
    con.commit()
    print("all users were deleted successfully.")



def update_user_by_id(con,user_id,column_name,column_value):

    cur=con.cursor()
    update_user_query=f"UPDATE users set{column_name}=? where id=?;"
    cur.execute(update_user_query,(column_value,user_id))
    con.commit()

    print(f"{column_name} was updated with {column_name} of user with id{user_id}.")




def main():
    con = create_connection()

    while True:


        user_input = input(INPUT_STRING)

        if user_input == "1":
            create_table(con)

        elif user_input == "2":
            users = read_csv()
            insert_users(con, users)


        elif user_input=="3":

            user_data=[]
            for column in COLUMNS:
                user_input=input(f"Enter the value for{column}:")

                user_data.append(user_input)
            insert_users(con,[tuple(user_data)])

            

        elif user_input=="4":

            select_users(con)


        elif user_input=="5":

            user_id=input("enter the id of user:")

            if user_input.isnumeric():
                select_user_by_id(con,user_id)


        elif user_input=="6":
            no_of_records=input("Enter the no.of records you want to fetch:")

            if no_of_records.isnumeric():
                select_users(con,int(no_of_records))

        elif user_input=="7":
            confirmation=input("are you sure ?press y or yes to continue:")
            if confirmation.lower() in["y","yes"]:

                delete_all_users(con)



        elif user_input=="8":
            user_id=input("enter the id of users:")
            if user_id.isnumeric():
                delete_user_by_id(con,user_id)



        elif user_input=="9":
            user_id=input("enter the id of user:")

            if user_id.isnumeric():
                column_name=input("enter the name of column.please make sure that columns is with in-{COLUMNS}:")

                if column_name in COLUMNS:
                    column_value=input(f"enter the value of {column_name}:")
                    update_user_by_id(con,user_id,column_name,column_value)


        else:
            exit()




                






if __name__ == "__main__":
    main()
