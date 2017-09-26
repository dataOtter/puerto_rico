from faceted_search import faceted_search_filter_instances as pidf


def test_print_and_prompt(filter_system):
    while True:
        prompt = "Active filters:"
        i = 1
        options = {}

        remove_options_dict = filter_system.get_remove_filter_options()

        for kind in remove_options_dict:
            prompt += "\nRemove " + kind + ": "
            for filter in remove_options_dict[kind]:
                prompt += ("\n\t" + str(i).rjust(3) + "   " + filter.get_cat()).ljust(15)
                options[i] = filter
                i += 1

        prompt += "\n\nInactive filters:"

        add_options_dict = filter_system.get_add_filter_options()

        for kind in add_options_dict:
            prompt += "\nAdd " + kind + ": "
            for filter_len_tuple in add_options_dict[kind]:
                substr = "\n\t" + str(i).rjust(3) + "   " + filter_len_tuple[0].get_cat()
                prompt += substr.ljust(15) + (" (" + str(filter_len_tuple[1]) + ")").rjust(6)
                options[i] = filter_len_tuple[0]
                i += 1

        prompt += "\n\nEnter your choice (a number between 1 and " + str(i-1) + " inclusive) or 'q' to quit:\n"

        choice = input(prompt)
        if choice == 'q':
            break

        filter_system.add_or_remove_filter(options[int(choice)])

        print("New active filters:")
        j = 0

        for fltr in filter_system.get_active_filters():
            print(fltr.get_kind() + ": " + fltr.get_cat())

        print("\nNumber of results: " + str(len(filter_system.get_result_pids())))
        print("--------------------------------------------------------------------------")

'''start_time = time.time()
m.make_memoize_table()
print("--- %s seconds ---" % (time.time() - start_time))
print("--- %s minutes ---" % ((time.time() - start_time)/60))'''

test_print_and_prompt(pidf.FilterSystem())
