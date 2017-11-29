"""This runs the filters system through the command prompt. Optional memoizing."""
from faceted_search import memoize_to_db as m
from faceted_search import faceted_search_filter_instances as pidf
import time as t


def print_and_prompt(filter_system):
    """Input: Filter system instance.
    Output: Runs the filters system through the command prompt for testing purposes."""
    while True:
        prompt = "Active filters:"
        i = 1
        options = {}  # to save all the remove or add filter options: key is an integer, value is the filter

        # get the currently applied kinds and categories of filters that can be removed
        remove_options_dict = filter_system.get_remove_filter_options()

        for kind in remove_options_dict:  # for every kind of filter that can be removed,
            prompt += "\nRemove " + kind + ": "  # print the kind,
            for one_filter in remove_options_dict[kind]:  # get every specific filter within that kind,
                # number the filter option and print number and category of that filter;
                prompt += ("\n\t" + str(i).rjust(3) + "   " + one_filter.get_cat()).ljust(15)
                options[i] = one_filter  # save the number along with the specific filter in options dictionary
                i += 1

        prompt += "\n\nInactive filters:"

        # get the currently not applied kinds and categories of filters that can be added,
        # and the number of PIDs that would then be selected
        add_options_dict = filter_system.get_add_filter_options()

        for kind in add_options_dict:  # for every kind of filter that can be added,
            prompt += "\nAdd " + kind + ": "  # print the kind,
            # get every filter and corresponding number of PIDs tuple within that kind,
            for filter_numpids_tuple in add_options_dict[kind]:
                # number the filter option and print number and category of that filter,
                substr = "\n\t" + str(i).rjust(3) + "   " + filter_numpids_tuple[0].get_cat()
                # as well as the number of remaining PIDs if this filter were applied;
                prompt += substr.ljust(15) + (" (" + str(filter_numpids_tuple[1]) + ")").rjust(6)
                options[i] = filter_numpids_tuple[0]  # save the number along with the specific filter in options dict
                i += 1

        prompt += "\n\nEnter your choice (a number between 1 and " + str(i-1) + " inclusive) or 'q' to quit:\n"

        choice = input(prompt)
        if choice == 'q':
            break

        filter_system.add_or_remove_filter(options[int(choice)])  # add or remove the selected filter

        print("New active filters:")

        for fltr in filter_system.get_active_filters():  # print all currently active filters
            print(fltr.get_kind() + ": " + fltr.get_cat())

        # print the number of PIDs currently selected
        print("\nNumber of results: " + str(len(filter_system.get_result_pids())))
        print("--------------------------------------------------------------------------")


def memoize_all_and_time():
    """Input: None.
    Output: Runs memoizing/caching and prints how long it took."""
    start_time = t.time()
    m.make_memoize_table()
    print("--- %s seconds ---" % (t.time() - start_time))
    print("--- %s minutes ---" % ((t.time() - start_time)/60))


#memoize_all_and_time()

print_and_prompt(pidf.FilterSystem())

