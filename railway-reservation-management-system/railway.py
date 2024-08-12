import json
import os

class Train:
    # Represents a train with its details and coaches.
    def __init__(self, train_id, name, origin, destination, day_of_week):
        self.train_id = train_id
        self.name = name
        self.origin = origin
        self.destination = destination
        self.day_of_week = day_of_week
        self.coaches = []

    def add_coach(self, coach_type, available_seats, fare):
        # Adds a coach to the train.
        coach = Coach(coach_type, available_seats, fare)
        self.coaches.append(coach)

    def to_dict(self):
        # Converts train details to dictionary format.
        return {
            'train_id': self.train_id,
            'name': self.name,
            'origin': self.origin,
            'destination': self.destination,
            'day_of_week': self.day_of_week,
            'coaches': [coach.to_dict() for coach in self.coaches]
        }

    @classmethod
    def from_dict(cls, data):
        # Creates a train object from dictionary data.
        train = cls(data['train_id'], data['name'], data['origin'], data['destination'], data['day_of_week'])
        train.coaches = [Coach.from_dict(coach) for coach in data['coaches']]
        return train


class Coach:
    # Represents a coach with its details.
    def __init__(self, coach_type, available_seats, fare):
        self.coach_type = coach_type
        self.available_seats = available_seats
        self.fare = fare

    def to_dict(self):
        # Converts coach details to dictionary format.
        return {
            'coach_type': self.coach_type,
            'available_seats': self.available_seats,
            'fare': self.fare
        }

    @classmethod
    def from_dict(cls, data):
        # Creates a coach object from dictionary data.
        return cls(data['coach_type'], data['available_seats'], data['fare'])


class User:
    # Represents a user with their details and bookings.
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.bookings = []

    def add_booking(self, booking):
        # Adds a booking to the user's bookings.
        self.bookings.append(booking)

    def cancel_booking(self, pnr):
        # Cancels a booking by PNR.
        self.bookings = [b for b in self.bookings if b.pnr != pnr]

    def to_dict(self):
        # Converts user details to dictionary format.
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'bookings': [booking.to_dict() for booking in self.bookings]
        }

    @classmethod
    def from_dict(cls, data):
        # Creates a user object from dictionary data.
        user = cls(data['user_id'], data['username'], data['password'])
        user.bookings = [Booking.from_dict(booking) for booking in data['bookings']]
        return user


class Booking:
    # Represents a booking with its details.
    def __init__(self, pnr, train_id, coach_type):
        self.pnr = pnr
        self.train_id = train_id
        self.coach_type = coach_type

    def to_dict(self):
        # Converts booking details to dictionary format.
        return {
            'pnr': self.pnr,
            'train_id': self.train_id,
            'coach_type': self.coach_type
        }

    @classmethod
    def from_dict(cls, data):
        # Creates a booking object from dictionary data.
        return cls(data['pnr'], data['train_id'], data['coach_type'])


class RailwayReservationSystem:
    # Manages the railway reservation system, including trains, users, and bookings.
    def __init__(self):
        self.trains = []
        self.users = []
        self.current_user = None
        self.next_pnr = 1
        self.load_data()

    def load_data(self):
        # Loads system data from a JSON file.
        if os.path.exists('system_data.json'):
            with open('system_data.json', 'r') as file:
                data = json.load(file)
                self.trains = [Train.from_dict(train) for train in data.get('trains', [])]
                self.users = [User.from_dict(user) for user in data.get('users', [])]
                self.next_pnr = data.get('next_pnr', 1)
        if not self.trains:
            self.add_default_trains()

    def save_data(self):
        # Saves system data to a JSON file.
        data = {
            'trains': [train.to_dict() for train in self.trains],
            'users': [user.to_dict() for user in self.users],
            'next_pnr': self.next_pnr
        }
        with open('system_data.json', 'w') as file:
            json.dump(data, file, indent=4)

    def add_default_trains(self):
        # Adds default trains and coaches to the system.
        self.add_train("Express 1", "City A", "City B", "Monday")
        self.add_train("Express 2", "City C", "City D", "Tuesday")
        self.add_coach(1, "Sleeper", 100, 500)
        self.add_coach(1, "AC", 50, 1000)
        self.add_coach(2, "Sleeper", 100, 500)
        self.add_coach(2, "AC", 50, 1000)

    def add_train(self, name, origin, destination, day_of_week):
        # Adds a train to the system.
        train_id = len(self.trains) + 1
        train = Train(train_id, name, origin, destination, day_of_week)
        self.trains.append(train)
        self.save_data()

    def add_coach(self, train_id, coach_type, available_seats, fare):
        # Adds a coach to a specific train.
        for train in self.trains:
            if train.train_id == train_id:
                train.add_coach(coach_type, available_seats, fare)
                self.save_data()
                return
        print("Train ID not found.")

    def search_trains(self, origin, destination, day_of_week):
        # Searches for trains based on origin, destination, and day of the week.
        results = []
        for train in self.trains:
            if train.origin == origin and train.destination == destination and train.day_of_week == day_of_week:
                results.append(train)
        return results

    def book_ticket(self, train_id, coach_type):
        # Books a ticket for the current user.
        if self.current_user is None:
            print("Please log in to book a ticket.")
            return

        for train in self.trains:
            if train.train_id == train_id:
                for coach in train.coaches:
                    if coach.coach_type == coach_type:
                        if coach.available_seats > 0:
                            coach.available_seats -= 1
                            booking = Booking(self.next_pnr, train_id, coach_type)
                            self.current_user.add_booking(booking)
                            print(f"Ticket booked successfully! PNR: {self.next_pnr}")
                            self.next_pnr += 1
                            self.save_data()
                            return
                        else:
                            print("No available seats in the selected coach.")
                            return
        print("Train ID or Coach Type not found.")

    def cancel_ticket(self, pnr):
        # Cancels a ticket for the current user.
        if self.current_user is None:
            print("Please log in to cancel a ticket.")
            return

        for booking in self.current_user.bookings:
            if booking.pnr == pnr:
                self.current_user.cancel_booking(pnr)
                for train in self.trains:
                    if train.train_id == booking.train_id:
                        for coach in train.coaches:
                            if coach.coach_type == booking.coach_type:
                                coach.available_seats += 1
                print("Ticket canceled successfully!")
                self.save_data()
                return
        print("PNR not found.")

    def check_pnr(self, pnr):
        # Checks the status of a PNR for the current user.
        if self.current_user is None:
            print("Please log in to check PNR status.")
            return

        for booking in self.current_user.bookings:
            if booking.pnr == pnr:
                print(f"PNR: {pnr}, Train ID: {booking.train_id}, Coach Type: {booking.coach_type}")
                return
        print("PNR not found.")

    def check_seat_availability(self, train_id, coach_type):
        # Checks seat availability for a specific train and coach type.
        for train in self.trains:
            if train.train_id == train_id:
                for coach in train.coaches:
                    if coach.coach_type == coach_type:
                        print(f"Available seats in Coach Type {coach_type}: {coach.available_seats}")
                        return
        print("Train ID or Coach Type not found.")

    def create_account(self, username, password):
        # Creates a new user account.
        user_id = len(self.users) + 1
        user = User(user_id, username, password)
        self.users.append(user)
        self.save_data()
        print("Account created successfully!")

    def login(self, username, password):
        # Logs in a user.
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print("Logged in successfully!")
                return
        print("Invalid username or password.")

    def check_previous_bookings(self):
        # Checks previous bookings for the current user.
        if self.current_user is None:
            print("Please log in to check previous bookings.")
            return

        if not self.current_user.bookings:
            print("No previous bookings found.")
            return

        for booking in self.current_user.bookings:
            print(f"PNR: {booking.pnr}, Train ID: {booking.train_id}, Coach Type: {booking.coach_type}")


def main():
    system = RailwayReservationSystem()
    
    while True:
        print("\n" + "="*40)
        print("  Railway Reservation Management System  ")
        print("="*40)
        print("1. Book Ticket")
        print("2. Cancel Ticket")
        print("3. Check PNR")
        print("4. Check Seat Availability")
        print("5. Create New Account")
        print("6. Check Previous Bookings")
        print("7. Login")
        print("8. Search Trains")
        print("9. Exit")
        print("="*40)
                
        choice = input("Enter your choice: ")
        
        if choice == '1':
            train_id = int(input("Enter train ID: "))
            coach_type = input("Enter coach type: ")
            system.book_ticket(train_id, coach_type)
        
        elif choice == '2':
            pnr = int(input("Enter PNR: "))
            system.cancel_ticket(pnr)
        
        elif choice == '3':
            pnr = int(input("Enter PNR: "))
            system.check_pnr(pnr)
        
        elif choice == '4':
            train_id = int(input("Enter train ID: "))
            coach_type = input("Enter coach type: ")
            system.check_seat_availability(train_id, coach_type)
        
        elif choice == '5':
            username = input("Enter username: ")
            password = input("Enter password: ")
            system.create_account(username, password)
        
        elif choice == '6':
            system.check_previous_bookings()
        
        elif choice == '7':
            username = input("Enter username: ")
            password = input("Enter password: ")
            system.login(username, password)

        elif choice == '8':
            origin = input("Enter origin: ")
            destination = input("Enter destination: ")
            day_of_week = input("Enter day of the week: ")
            results = system.search_trains(origin, destination, day_of_week)
            if results:
                print("Available trains:")
                for train in results:
                    print(f"Train ID: {train.train_id}, Name: {train.name}")
            else:
                print("No trains found for the given criteria.")
        
        elif choice == '9':
            system.save_data()
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
