import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("tickets.json")


class BusTicketSystem:
    def __init__(self, route: str, total_seats: int, fare: float):
        self.route = route
        self.total_seats = total_seats
        self.fare = fare
        self.bookings = self._load_bookings()

    def _load_bookings(self) -> dict:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_bookings(self) -> None:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(self.bookings, f, indent=2)

    def available_seats(self) -> list[int]:
        booked = {int(seat) for seat in self.bookings}
        return [seat for seat in range(1, self.total_seats + 1) if seat not in booked]

    def book_ticket(self, passenger_name: str, seat_number: int) -> dict | None:
        name = passenger_name.strip()
        if not name:
            print("Passenger name cannot be empty.")
            return None
        if seat_number < 1 or seat_number > self.total_seats:
            print(f"Choose a seat between 1 and {self.total_seats}.")
            return None
        if str(seat_number) in self.bookings:
            print(f"Seat {seat_number} is already booked.")
            return None

        ticket = {
            "passenger": name,
            "route": self.route,
            "seat": seat_number,
            "fare": self.fare,
            "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.bookings[str(seat_number)] = ticket
        self._save_bookings()
        return ticket

    def cancel_ticket(self, seat_number: int) -> bool:
        key = str(seat_number)
        if key not in self.bookings:
            print(f"Seat {seat_number} is not currently booked.")
            return False
        del self.bookings[key]
        self._save_bookings()
        return True

    def view_bookings(self) -> None:
        if not self.bookings:
            print("\nNo tickets booked yet.")
            return
        print("\n--- Current Bookings ---")
        for seat in sorted(self.bookings, key=int):
            t = self.bookings[seat]
            print(
                f"Seat {seat:>2} | {t['passenger']} | {t['route']} | "
                f"${t['fare']:.2f} | {t['booked_at']}"
            )


def prompt_int(message: str) -> int | None:
    try:
        return int(input(message).strip())
    except ValueError:
        print("Please enter a valid number.")
        return None


def main() -> None:
    system = BusTicketSystem(route="Downtown -> Airport", total_seats=20, fare=12.50)

    while True:
        print(f"\n=== Bus Ticket System ({system.route}) ===")
        print("1. View available seats")
        print("2. Book a ticket")
        print("3. Cancel a ticket")
        print("4. View all bookings")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            seats = system.available_seats()
            print("Available seats:", seats if seats else "None (Bus Full)")

        elif choice == "2":
            name = input("Passenger name: ")
            seat = prompt_int(f"Seat number (1-{system.total_seats}): ")
            if seat is not None:
                ticket = system.book_ticket(name, seat)
                if ticket:
                    print(
                        f"Booked! Seat {ticket['seat']} for {ticket['passenger']} "
                        f"(${ticket['fare']:.2f})."
                    )

        elif choice == "3":
            seat = prompt_int("Seat number to cancel: ")
            if seat is not None and system.cancel_ticket(seat):
                print(f"Seat {seat} booking cancelled.")

        elif choice == "4":
            system.view_bookings()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Enter 1 through 5.")


if __name__ == "__main__":
    main()