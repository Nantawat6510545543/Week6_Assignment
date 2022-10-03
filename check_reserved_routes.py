def get_station_index(station_indexes, _station_name):
    return station_indexes[_station_name]


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
        >>> check_reserved_routes({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4, 'FF': 5},\
            [{'origin': 'AA', 'dest': 'BB'}, {'origin': 'CC', 'dest': 'DD'}, {'origin': 'EE', 'dest': 'FF'}])
        [1, 1, 1, 1, 1, 1]
        >>> check_reserved_routes({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4},\
            [{'origin': 'BB', 'dest': 'EE'}])
        [0, 1, 1, 1, 1]
    """
    reserved = [0 for _ in range(len(station_indexes))]
    for i in range(len(station_indexes)):
        for j in range(len(ticket_list)):
            origin = get_station_index(station_indexes, ticket_list[j]['origin'])
            dest = get_station_index(station_indexes, ticket_list[j]['dest'])
            # print(f"{i} is in rang {origin}-{dest} = {i in range(origin,dest+1)}")
            reserved[i] = int((i in range(origin, dest+1)) or reserved[i])

    return reserved
