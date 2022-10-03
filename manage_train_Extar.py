def read_stations(station_filename):
    lines = open(station_filename).read().splitlines()
    table = [x.split(",") for x in lines if x != ""]
    station_fees = {}
    station_indexes = {}
    station_fees = {}
    for i in range(len(table)):
        temp_station_fees = []
        for j in range(1, len(table[0])):
            temp_station_fees.append(int(table[i][j]))
        station_fees[table[i][0]] = temp_station_fees
        station_indexes[table[i][0]] = i
    return station_fees, station_indexes


def read_seats(seat_filename):
    lines = open(seat_filename).read().splitlines()
    seats = {}
    seat_classes = []
    for x in lines:
        seats[x] = []
        temp_seat_class = int(x[0])
        if not (temp_seat_class in seat_classes):
            seat_classes.append(temp_seat_class)
    return seats, seat_classes


def read_reserved_tickets(ticket_filename, seats):
    lines = open(ticket_filename).read().splitlines()
    table = [x.split(",") for x in lines if x != ""]
    for row in table:
        seat_num = row[0]
        pax = {'origin': row[1], 'dest': row[2]}
        seats[seat_num].append(pax)


def read_origin():
    while True:
        origin = int(input(f"Enter origin (0-{len(station_indexes) - 1}): "))
        if 0 <= origin < len(station_indexes):
            return origin
        print("Invalid origin station index.")


def read_dest(origin_index):
    while True:
        dest = int(
            input(f"Enter destination (0-{len(station_indexes) - 1}): "))
        if origin_index < dest < len(station_indexes):
            return dest
        print("Invalid destination station index.")


def get_station_index(station_indexes, _station_name):
    return station_indexes[_station_name]


def get_station_name(station_indexes, _station_index):
    for key, value in station_indexes.items():
        if _station_index == value:
            return key


def show_seats(seats, station_indexes):
    for i in seats:
        text = f"{i}:"
        for j in seats[i]:
            origin = j['origin']
            origin_index = station_indexes[origin]
            dest = j['dest']
            dest_index = station_indexes[dest]
            text += f" [{origin}({origin_index})-{dest}({dest_index})],"
        print(text)


def check_routes_available(station_indexes, ticket_list,
                           origin_index, dest_index):
    for j in ticket_list:
        routes = range(station_indexes[j['origin']],
                       station_indexes[j['dest']] + 1)
        reserved = range(origin_index, dest_index + 1)
        if list(set(routes) & set(reserved)):
            return False
    return True


def choose_available_seat(available_seats):
    while True:
        seat = input("Select seat: ")
        if seat in available_seats:
            return seat
        print("Invalid seats.")
        print(f"Available seats: {available_seats}")


def update_seat(station_indexes, origin_index, dest_index, ticket_list):
    ticket_list.append(
        {'origin': get_station_name(station_indexes, origin_index),
         'dest': get_station_name(station_indexes, dest_index)})
    return ticket_list


def get_ticket_price(station_indexes, station_fees, origin_index, dest_index,
                     seat_class):
    seat_class -= 1
    origin = get_station_name(station_indexes, origin_index)
    dest = get_station_name(station_indexes, dest_index)
    return station_fees[dest][seat_class] - station_fees[origin][seat_class]


def reserve(train_seats, train_seat_classes, station_indexes, station_fees):
    origin_index = read_origin()
    dest_index = read_dest(origin_index)

    available = [i for i in train_seats.keys() if check_routes_available(
        station_indexes, train_seats[i], origin_index, dest_index) is True]

    if not available:
        print("Sorry. No available seat.")

    else:
        print(f"Available seats: {available}")
        price = [get_ticket_price(station_indexes, station_fees, origin_index,
                                  dest_index, i)
                 for i in train_seat_classes]
        [print(f"Class {i} Ticket price = {price[i - 1]}") for i in
         train_seat_classes]
        seat = choose_available_seat(available)
        print(f"The selected seat = {seat}")
        print(f"The ticket price = {price[int(seat[0]) - 1]}")
        train_seats[seat] = update_seat(station_indexes, origin_index,
                                        dest_index, train_seats[seat])


def read_canceled_seat(train_seats):
    while True:
        seat = input("Enter seat to cancel: ")
        if seat in train_seats.keys():
            return seat
        print("Invalid seat.")


def remove_ticket(train_seats, station_indexes, seat_str, origin_index,
                  dest_index):
    """ Function remove_ticket does the followings:
        1. get the ticket list of specific seat
        2. check whether ticket between origin and dest station indexes exists \
            inside the ticket list from 1.
        3. if ticket between origin and dest station indexes exists, \
            remove such ticket from the ticket list and return True
        4. if ticket between origin and dest station indexes does not exist, \
            return False

        :param train_seats: dictionary of seats
        :param station_indexes: dictionary of station indexes
        :param seat_str: string
        :param origin_index: int
        :param dest_index: int
        :return: boolean value
    """
    for j in train_seats[seat_str]:
        if station_indexes[j['origin']] == origin_index and \
                station_indexes[j['dest']] == dest_index:
            train_seats[seat_str].remove(j)
            return True
    return False


def cancel(train_seats, station_indexes):
    """ Function cancel does the followings:
        1. read the canceled seat from user
        2. read the origin and destination station index of canceled ticket
        3. display tickets reserved under the canceled seat
        3. if ticket removal is successful,  \
            display updated tickets under the canceled seat
        4.  if ticket removal is not successful (or ticket does not exist \
            in the ticket list, report to user

        :param train_seats: dictionary of seats
        :param station_indexes: dictionary of station indexes
        :return: nothing
    """
    print(f"Seats are {[i for i in train_seats.keys()]}")
    seat_str = read_canceled_seat(train_seats)
    origin_index = read_origin()
    dest_index = read_dest(origin_index)

    text = f"Tickets issued at {seat_str}:"
    for j in train_seats[seat_str]:
        origin = j['origin']
        origin_number = station_indexes[origin]
        dest = j['dest']
        dest_number = station_indexes[dest]
        text += f" [{origin}({origin_number})-{dest}({dest_number})],"
    print(text)

    if remove_ticket(train_seats, station_indexes, seat_str,
                     origin_index, dest_index):
        print("After cancellation:")
        text = f"Tickets issued at {seat_str}:"
        for j in train_seats[seat_str]:
            origin = j['origin']
            origin_number = station_indexes[origin]
            dest = j['dest']
            dest_number = station_indexes[dest]
            text += f" [{origin}({origin_number})-{dest}({dest_number})],"
        print(text)

    else:
        print(f"Ticket does not exist at {seat_str}")


def show_ticket_prices(train_seats, station_indexes, station_fees):
    """ Display reserved tickets from all seats, along with TICKET PRICE
        Use information of ticket list inside each seat from dictionary of
            seats, dictionary of station indexes, and diction of ticket fees
            to help display.

        :param train_seats: dictionary of seats
        :param station_indexes: dictionary of station indexes
        :param station_fees: dictionary of ticket fees
        :return: nothing
    """
    for i in train_seats:
        text = f"{i}:"
        for j in train_seats[i]:
            origin = j['origin']
            origin_index = station_indexes[origin]
            dest = j['dest']
            dest_index = station_indexes[dest]
            price = get_ticket_price(station_indexes, station_fees,
                                     origin_index, dest_index, int(i[0]))
            text += f" [{origin}({origin_index})-{dest}({dest_index})" \
                    f"-{price}],"
        print(text)


def clear_tickets(train_seats):
    """ Set ticket list of each seat to be empty list

        :param train_seats: dictionary of seats
        :return: nothing
    """
    print("After clearing all tickets")
    for i in train_seats.keys():
        train_seats[i].clear()
    show_seats(train_seats, station_indexes)


station_fees, station_indexes = read_stations('south_stations.txt')
# print(station_fees)        # you can uncomment this line to see output
# print(station_indexes)     # you can uncomment this line to see output
TOTAL_NUM_STATIONS = len(station_indexes)
# print(TOTAL_NUM_STATIONS)  # you can uncomment this line to see output

train_seats, train_seat_classes = read_seats('south_train_seats.txt')
# print(train_seats)         # you can uncomment this line to see output
# print(train_seat_classes)  # you can uncomment this line to see output

read_reserved_tickets('south_reserved_tickets.txt', train_seats)
# print(train_seats)  # you can uncomment this line to see output

while True:
    print()
    print('1. Show seats')
    print('2. Reserve ticket')
    print('3. Cancel ticket')
    print('4. Show ticket prices')
    print('5. Clear all tickets')
    print('6. Exit')
    choice = int(input('Enter your choice: '))
    if choice == 1:
        show_seats(train_seats, station_indexes)
    elif choice == 2:
        reserve(train_seats, train_seat_classes, station_indexes, station_fees)
    elif choice == 3:
        cancel(train_seats, station_indexes)
    elif choice == 4:
        show_ticket_prices(train_seats, station_indexes, station_fees)
    elif choice == 5:
        clear_tickets(train_seats)
    elif choice == 6:
        break
    else:
        print("Invalid choice. Choose again.")

if __name__ == '__main__':
    import doctest

    doctest.testmod()
