def read_stations(station_filename):
    """ Read station file
        Read one line as one string and use , to split into multiple values
        Each line contains n+1 values: station X (string),
            ticket price of class 1 between Bangkok and station X (int),
            ticket price of class 2 between Bangkok and station X (int),
            ...
            ticket price of class n between Bangkok and station X (int),
        Return 2 dictionaries
        1) Dictionary of ticket prices for different classes,
            where key is station X (string), and
                  value is a list of ticket prices from different seat classes.
                  If there are n seat classes, a list of ticket prices will
                    have n members. First member = Ticket price of class 1, ...,
                    Last member = Ticket price of class n.
        2) Dictionary of station indexes
            where key is station X (string), and
                  value is station index (int)
                  Bangkok station has station index = 0

    :param station_filename: string
    :return: dictionary of ticket prices, and dictionary of station indexes
    """
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
    """ Read seat file
        Read one line as one string and return 2 items
        1) dictionary of seats: key is seat, and value is an empty ticket list
        2) list of seat classes

        :param seat_filename: string
        :return: dictionary of seats, and list of seat classes
    """
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
    """ Read reserved ticket file
        Read one line as one string and use , to split into multiple values
        Each line contains 3 values: seat (string),
            origin station name (string),
            destination station name (string)
        For each reserved ticket at seat S,
            add a ticket dictionary with origin and destination stations
            to seat S in dictionary of seats
        Note that no value is returned here.  If values inside dictionary
            seats are changed, dictionary seats will be updated as well.

    :param ticket_filename: string
    :param seats: dictionary of seats
    :return: nothing
    """
    lines = open(ticket_filename).read().splitlines()
    table = [x.split(",") for x in lines if x != ""]
    for row in table:
        seat_num = row[0]
        pax = {'origin': row[1], 'dest': row[2]}
        seats[seat_num].append(pax)


def read_origin():
    """ Read origin station index from user
        If user enters an invalid station index, report to user and
            continuously ask until a valid index is entered.
        Return origin station index (int)

    :param: Nothing
    :return: int
    """
    while True:
        origin = int(input(f"Enter origin (0-{len(station_indexes)-1}): "))
        if 0 <= origin < len(station_indexes):
            return origin
        print("Invalid origin station index.")


def read_dest(origin_index):
    """ Read destination station index  from user
        Receive origin station index as function input.
        If user enters an invalid station index, report to user and
            continuously ask until a valid index is entered.
        Note that destination station index cannot be the same as, or be less
            than the origin station index
        Return destination station index (int)

        :param: origin_index: int
        :return: int
    """
    while True:
        dest = int(input(f"Enter destination (0-{len(station_indexes)-1}): "))
        if origin_index < dest < len(station_indexes):
            return dest
        print("Invalid destination station index.")


def get_station_index(station_indexes, _station_name):
    """ From a given _station_name, return station index of this station

        :param station_indexes: dictionary of station indexes
        :param _station_name: string
        :return: int
        >>> get_station_index({'AA': 0, 'BB': 1, 'CC': 2}, 'AA')
        0
        >>> get_station_index({'AA': 0, 'BB': 1, 'CC': 2}, 'BB')
        1
        >>> get_station_index({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3}, 'DD')
        3
    """
    return station_indexes[_station_name]


def get_station_name(station_indexes, _station_index):
    """ From a given _station_index, return station name (string) of this
    station index

        :param station_indexes: dictionary of station indexes
        :param _station_index: int
        :return: string
        >>> get_station_name({'AA': 0, 'BB': 1, 'CC': 2}, 0)
        'AA'
        >>> get_station_name({'AA': 0, 'BB': 1, 'CC': 2}, 1)
        'BB'
        >>> get_station_name({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3}, 3)
        'DD'
    """
    for key, value in station_indexes.items():
        if _station_index == value:
            return key


def show_seats(station_seats, station_indexes):
    """ Display reserved tickets from all seats
        Use information of ticket list inside each seat from dictionary of seats \
            and dictionary of station indexes to help display.

        :param station_seats: dictionary of seats
        :param station_indexes: dictionary of station indexes
        :return: Nothing
    """
    for i in station_seats:
        text = f"{i}:"
        for j in station_seats[i]:
            origin = j['origin']
            origin_index = get_station_index(station_indexes, origin)
            dest = j['dest']
            dest_index = get_station_index(station_indexes, dest)
            text += f" [{origin}({origin_index})-{dest}({dest_index})],"
        print(text)


def check_reserved_routes(station_indexes, ticket_list):
    """ Create a list with length = number of all stations
        This list has values of 1's or 0's
        The value is 1 if such station index is on any reserved ticket.
        The value if 0 if such station index is not on any reserved ticket.
        Return this list of 1's or 0's

        :param station_indexes: dictionary of station indexes
        :param ticket_list: list of tickets
        :return: list of ints
        >>> check_reserved_routes({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4},\
            [{'origin': 'AA', 'dest': 'CC'}])
        [1, 1, 1, 0, 0]
        >>> check_reserved_routes({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4},\
            [{'origin': 'AA', 'dest': 'BB'}, {'origin': 'CC', 'dest': 'EE'}])
        [1, 1, 1, 1, 1]
        >>> check_reserved_routes({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4},\
            [{'origin': 'BB', 'dest': 'EE'}])
        [0, 1, 1, 1, 1]
    """
    reserved = [0 for _ in range(len(station_indexes))]
    for i in range(len(station_indexes)):
        for j in range(len(ticket_list)):
            origin = get_station_index(station_indexes,
                                       ticket_list[j]['origin'])
            dest = get_station_index(station_indexes, ticket_list[j]['dest'])
            reserved[i] = int((i in range(origin, dest + 1)) or reserved[i])

    return reserved


def is_ticket_available(reserved_routes, origin_index, dest_index):
    """ Return True if ticket with origin station index and dest station index \
        is available. Otherwise, return False.
        Use a list, reserved_routes, to help find out whether ticket starting \
            from origin station index to  dest station index is available or not

        :param reserved_routes: list of ints
        :param origin_index: int
        :param dest_index: int
        :return: boolean value
        >>> is_ticket_available([1, 1, 1, 0, 0], 3, 4)
        True
        >>> is_ticket_available([1, 1, 1, 0, 0], 0, 1)
        False
        >>> is_ticket_available([0, 0, 0, 1, 1, 1, 0, 0, 0], 0, 1)
        True
        >>> is_ticket_available([0, 0, 0, 1, 1, 1, 0, 0, 0], 0, 5)
        False
        >>> is_ticket_available([0, 0, 0, 1, 1, 1, 0, 0, 0], 6, 7)
        True
    """
    return all(
        [reserved_routes[i] == 0 for i in range(origin_index, dest_index + 1)])


def choose_available_seat(available_seats):
    """ Read available seat from user
        Receive a list of available seats (e.g., ['1A', '1B', '1C'])
        If user enters seat that is not in available_seats, report to
        user and continuously ask until a valid seat is entered.
        Return destination seat (string)

    :param available_seats: list of strings
    :return: string
    """
    while True:
        seat = input("Select seat: ")
        if seat in available_seats:
            return seat
        print("Invalid seats.")
        print(f"Available seats: {available_seats}")


def update_seat(station_indexes, origin_index, dest_index, ticket_list):
    """ Add new ticket to the ticket list of one seat
        Receive dictionary of station indexes, origin station index (int), \
            dest station index (int) and ticket list of one specific seat as \
            function inputs
        This function is called after the program finds out ticket between \
            origin station index and dest station index is available.
        Return the updated ticket list

        :param station_indexes: dictionary of station indexes
        :param origin_index: int
        :param dest_index: int
        :param ticket_list: list of ticket from one seat
        :return: ticket list
        >>> update_seat(\
            {'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4},\
             2, 3, \
            [{'origin': 'AA', 'dest': 'BB'}])
        [{'origin': 'AA', 'dest': 'BB'}, {'origin': 'CC', 'dest': 'DD'}]

        >>> update_seat(\
            {'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4, 'FF': 5, 'GG': 6}, \
            3, 4, \
            [{'origin': 'AA', 'dest': 'BB'}, {'origin': 'FF', 'dest': 'GG'}])
        [{'origin': 'AA', 'dest': 'BB'}, {'origin': 'FF', 'dest': 'GG'}, {'origin': 'DD', 'dest': 'EE'}]

        >>> update_seat(\
        {   'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4},\
            0, 1, \
            [{'origin': 'DD', 'dest': 'EE'}])
        [{'origin': 'DD', 'dest': 'EE'}, {'origin': 'AA', 'dest': 'BB'}]
    """
    ticket_list.append(
        {'origin': get_station_name(station_indexes, origin_index),
         'dest': get_station_name(station_indexes, dest_index)})
    return ticket_list


def get_ticket_price(station_indexes, station_fees, origin_index, dest_index,
                     seat_class):
    """ Return a price of ticket class = seat_class between origin station index
            and dest station index
        Note that the ticket price between station index 2 and station index 3
            can be computed from DIFFERENCE between \
            ticket price between station index 0 and station index 3 and
            ticket price between station index 0 and station index 2

        :param station_indexes: dictionary of station indexes
        :param station_fees: dictionary of ticket fees
        :param origin_index: int
        :param dest_index: int
        :param seat_class: int
        :return: boolean value
        >>> get_ticket_price({'AA': 0, 'BB': 1, 'CC': 2}, \
            {'AA': [0, 0], 'BB': [200, 100], 'CC': [275, 150]}, \
            0, 1, 1)
        200
        >>> get_ticket_price({'AA': 0, 'BB': 1, 'CC': 2}, \
            {'AA': [0, 0], 'BB': [200, 100], 'CC': [275, 150]}, \
            0, 1, 2)
        100
        >>> get_ticket_price({'AA': 0, 'BB': 1, 'CC': 2}, \
            {'AA': [0, 0], 'BB': [200, 100], 'CC': [275, 150]}, \
            1, 2, 1)
        75
        >>> get_ticket_price({'AA': 0, 'BB': 1, 'CC': 2}, \
            {'AA': [0, 0], 'BB': [200, 100], 'CC': [275, 150]}, \
            1, 2, 2)
        50
    """
    seat_class -= 1
    origin = get_station_name(station_indexes, origin_index)
    dest = get_station_name(station_indexes, dest_index)
    return station_fees[dest][seat_class] - station_fees[origin][seat_class]


def reserve(train_seats, train_seat_classes, station_indexes, station_fees):
    """ Function reserve does the followings:
        1. read origin and destination station indexes from user
        2. find available seats between origin and destination station indexes
        3. if there are available seats,
            3.1 show ticket prices from all seat classes
            3.2 let user choose one of available seat
            3.3 report price of the chosen seat
            3.4 update ticket list of the chosen seat
        4. if there is no available seat, report to user

        :param train_seats: dictionary of seats
        :param train_seat_classes: list of seat classes
        :param station_indexes: dictionary of station indexes
        :param station_fees: dictionary of ticket fees
        :return: nothing
    """
    origin_index = read_origin()
    dest_index = read_dest(origin_index)

    available = [i for i in train_seats.keys() if is_ticket_available(
        check_reserved_routes(station_indexes, train_seats[i]), origin_index,
        dest_index) is True]

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
    """ Read the canceled seat  from user
        Receive dictionary of seats as function input.
        If user enters an invalid seat, report to user and
            continuously ask until a valid seat is entered.
        Note that the canceled seat may or may not have the canceled ticket. \
            We will check whether the canceled ticket is available inside \
            this canceled seat later.
        Return the canceled seat (string)

        :param: train_seats: dictionary of seats
        :return: string
    """
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
        origin_number = get_station_index(station_indexes, origin)
        dest = j['dest']
        dest_number = get_station_index(station_indexes, dest)
        text += f" [{origin}({origin_number})-{dest}({dest_number})],"
    print(text)

    if remove_ticket(train_seats, station_indexes, seat_str,
                     origin_index, dest_index):
        print("After cancellation:")
        text = f"Tickets issued at {seat_str}:"
        for j in train_seats[seat_str]:
            origin = j['origin']
            origin_number = get_station_index(station_indexes, origin)
            dest = j['dest']
            dest_number = get_station_index(station_indexes, dest)
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
            origin_index = get_station_index(station_indexes, origin)
            dest = j['dest']
            dest_index = get_station_index(station_indexes, dest)
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


station_fees, station_indexes = read_stations('north_stations.txt')
# print(station_fees)        # you can uncomment this line to see output
# print(station_indexes)     # you can uncomment this line to see output
TOTAL_NUM_STATIONS = len(station_indexes)
# print(TOTAL_NUM_STATIONS)  # you can uncomment this line to see output

train_seats, train_seat_classes = read_seats('north_train_seats.txt')
# print(train_seats)         # you can uncomment this line to see output
# print(train_seat_classes)  # you can uncomment this line to see output

read_reserved_tickets('north_reserved_tickets.txt', train_seats)
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
