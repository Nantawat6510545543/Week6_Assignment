def check_routes_available(station_indexes, ticket_list,
                           origin_index, dest_index):
    """
        >>> check_routes_available({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4}\
        ,[{'origin': 'AA', 'dest': 'CC'}],3,4)
        True
        >>> check_routes_available({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4}\
        ,[{'origin': 'AA', 'dest': 'BB'}, {'origin': 'CC', 'dest': 'EE'}],1,3)
        False
        >>> check_routes_available({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4}\
        ,[{'origin': 'CC', 'dest': 'EE'}],0,1)
        True
    """

    for j in ticket_list:
        routes = range(station_indexes[j['origin']],
                       station_indexes[j['dest']] + 1)
        reserved = range(origin_index, dest_index + 1)
        if list(set(routes) & set(reserved)):
            return False
    return True

    # return not all([bool(list(set(range(station_indexes[j['origin']],
    #                                     station_indexes[j['dest']] + 1))
    #                           & set(range(origin_index, dest_index + 1))))
    #                 for j in ticket_list])


# def is_ticket_available(reserved_routes, origin_index, dest_index):
#     """
#         >>> is_ticket_available([1, 1, 1, 0, 0], 3, 4)
#         True
#         >>> is_ticket_available([1, 1, 1, 0, 0], 0, 1)
#         False
#         >>> is_ticket_available([0, 0, 0, 1, 1, 1, 0, 0, 0], 0, 1)
#         True
#         >>> is_ticket_available([0, 0, 0, 1, 1, 1, 0, 0, 0], 0, 5)
#         False
#         >>> is_ticket_available([0, 0, 0, 1, 1, 1, 0, 0, 0], 6, 7)
#         True
#     """
#     return all(
#         [reserved_routes[i] == 0 for i in range(origin_index, dest_index + 1)])
