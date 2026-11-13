
import mysql.connector
import uuid

# CONNECT TO MYSQL DATABASE
db = mysql.connector.connect(host="localhost", user="root", password="YOUR_MYSQL_PASSWORD", database="railway_reservation")
cursor = db.cursor()

def intro():
    print("=" * 60)
    print("{:^60}".format("RAILWAY RESERVATION SYSTEM"))
    print("{:^60}".format("CLASS XII PROJECT"))
    print("=" * 60)


# 1. ADD A TRAIN
def add_train():
    print("\nADD NEW TRAIN")
    train_no = int(input("Enter train number: "))
    train_name = input("Enter train name: ")
    source = input("Enter source: ")
    destination = input("Enter destination: ")
    seats = int(input("Enter total seats: "))

    cursor.execute(
        """INSERT INTO trains
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (train_no, train_name, source, destination, seats, seats)
    )

    db.commit()
    print("Train added successfully!")


# 2. DISPLAY ALL TRAINS
def display_trains():
    cursor.execute("SELECT * FROM trains")
    records = cursor.fetchall()

    if not records:
        print("No trains available.")
        return

    print("\nTRAIN DETAILS")
    print("-" * 75)

    for record in records:
        print("Train Number:", record[0])
        print("Train Name:", record[1])
        print("Source:", record[2])
        print("Destination:", record[3])
        print("Total Seats:", record[4])
        print("Available Seats:", record[5])
        print("-" * 75)


# 3. SEARCH TRAINS
def search_train():
    source = input("Enter source: ")
    destination = input("Enter destination: ")

    cursor.execute(
        """SELECT * FROM trains
        WHERE source = %s AND destination = %s""",
        (source, destination)
    )

    records = cursor.fetchall()

    if not records:
        print("No trains found for this route.")
    else:
        for record in records:
            print(record)


# 4. BOOK A TICKET
def book_ticket():
    print("\nTICKET BOOKING")

    train_no = int(input("Enter train number: "))

    cursor.execute(
        "SELECT * FROM trains WHERE train_no = %s",
        (train_no,)
    )

    train = cursor.fetchone()

    if train is None:
        print("Train not found.")
        return

    print("Train:", train[1])
    print("Available seats:", train[5])

    seats = int(input("Enter number of seats to book: "))

    if seats <= 0 or seats > train[5]:
        print("Invalid number of seats or insufficient availability.")
        return

    name = input("Enter passenger name: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender: ")
    phone = input("Enter phone number: ")
    journey_date = input("Enter journey date (YYYY-MM-DD): ")

    pnr = uuid.uuid4().hex[:10].upper()

    try:
        # INSERT PASSENGER
        cursor.execute(
            """INSERT INTO passengers
            (passenger_name, age, gender, phone)
            VALUES (%s, %s, %s, %s)""",
            (name, age, gender, phone)
        )

        passenger_id = cursor.lastrowid

        # INSERT BOOKING
        cursor.execute(
            """INSERT INTO bookings
            (passenger_id, train_no, journey_date,
            seats_booked, pnr)
            VALUES (%s, %s, %s, %s, %s)""",
            (passenger_id, train_no, journey_date, seats, pnr)
        )

        # UPDATE AVAILABLE SEATS
        cursor.execute(
            """UPDATE trains
            SET available_seats = available_seats - %s
            WHERE train_no = %s""",
            (seats, train_no)
        )

        db.commit()

        print("\nTICKET BOOKED SUCCESSFULLY!")
        print("Passenger Name:", name)
        print("Train:", train[1])
        print("PNR:", pnr)

    except mysql.connector.Error as error:
        db.rollback()
        print("Booking failed:", error)


# 5. DISPLAY ALL BOOKINGS
def display_bookings():
    cursor.execute(
        """SELECT b.pnr, p.passenger_name, t.train_name,
        b.journey_date, b.seats_booked, b.booking_status
        FROM bookings b
        JOIN passengers p
        ON b.passenger_id = p.passenger_id
        JOIN trains t
        ON b.train_no = t.train_no"""
    )

    records = cursor.fetchall()

    if not records:
        print("No bookings found.")
        return

    print("\nBOOKING DETAILS")

    for record in records:
        print("-" * 50)
        print("PNR:", record[0])
        print("Passenger:", record[1])
        print("Train:", record[2])
        print("Journey Date:", record[3])
        print("Seats Booked:", record[4])
        print("Status:", record[5])


# 6. CANCEL A BOOKING
def cancel_booking():
    pnr = input("Enter PNR number: ")

    cursor.execute(
        """SELECT booking_id, train_no, seats_booked
        FROM bookings
        WHERE pnr = %s AND booking_status = 'CONFIRMED'""",
        (pnr,)
    )

    booking = cursor.fetchone()

    if booking is None:
        print("Booking not found or already cancelled.")
        return

    try:
        cursor.execute(
            """UPDATE bookings
            SET booking_status = 'CANCELLED'
            WHERE booking_id = %s""",
            (booking[0],)
        )

        cursor.execute(
            """UPDATE trains
            SET available_seats = available_seats + %s
            WHERE train_no = %s""",
            (booking[2], booking[1])
        )

        db.commit()
        print("Booking cancelled successfully!")

    except mysql.connector.Error as error:
        db.rollback()
        print("Cancellation failed:", error)


# MAIN MENU
def main():
    intro()

    while True:
        print("\nMAIN MENU")
        print("1. Add Train")
        print("2. Display All Trains")
        print("3. Search Train")
        print("4. Book Ticket")
        print("5. Display All Bookings")
        print("6. Cancel Booking")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            add_train()

        elif choice == "2":
            display_trains()

        elif choice == "3":
            search_train()

        elif choice == "4":
            book_ticket()

        elif choice == "5":
            display_bookings()

        elif choice == "6":
            cancel_booking()

        elif choice == "7":
            print("Thank you for using Railway Reservation System!")
            break

        else:
            print("Invalid choice. Try again.")

    cursor.close()
    db.close()


main()
