"""This is a filter system class made of instances of various filters."""
import copy
import constants as c
from ETL import wrangling_functions as w
from faceted_search import faceted_search_filter_classes as cl, memoize_to_db as m
from filters import filter_SQL_queries as sql_fltr


class FilterSystem:
    """Filter system class made of instances of various filters."""
    def __init__(self):
        male = cl.GenderFilter("M")
        female = cl.GenderFilter("F")
        transgender = cl.GenderFilter("TG")

        ageto18 = cl.AgeFilter("0-18")
        age19to24 = cl.AgeFilter("19-24")
        age25to40 = cl.AgeFilter("25-40")
        age41to100 = cl.AgeFilter("41-100")

        drugmin1 = cl.MinDrugsFilter("1")
        drugmin3 = cl.MinDrugsFilter("2-3")
        drugmin7 = cl.MinDrugsFilter("4-7")
        drugmin8 = cl.MinDrugsFilter("8")

        drugmax1 = cl.MaxDrugsFilter("1")
        drugmax3 = cl.MaxDrugsFilter("2-3")
        drugmax7 = cl.MaxDrugsFilter("4-7")
        drugmax8 = cl.MaxDrugsFilter("8")

        self.filters_tuple = (male, female, transgender,
                              ageto18, age19to24, age25to40, age41to100,
                              drugmin1, drugmin3, drugmin7, drugmin8,
                              drugmax1, drugmax3, drugmax7, drugmax8)
        self.filters_dict = {"Gender": (male, female, transgender),
                             "Age": (ageto18, age19to24, age25to40, age41to100),
                             "MinDrugUse": (drugmin1, drugmin3, drugmin7, drugmin8),
                             "MaxDrugUse": (drugmax1, drugmax3, drugmax7, drugmax8)}
        self.inactive_filters = list(self.filters_tuple)
        self.active_filters = []
        self.result_pids = w.get_union_of_lists(sql_fltr.pids_phase_1(), sql_fltr.pids_phase_2())

    def get_filters_dict(self):
        """Input: None.
        Output: Returns dictionary of all filter kinds to categories (class member)."""
        return self.filters_dict

    def get_result_pids(self):
        """Input: None.
        Output: Returns list of all project IDs (class member)."""
        return self.result_pids

    def get_active_filters(self):
        """Input: None.
        Output: Returns list of all currently active filters (class member)."""
        return self.active_filters

    def get_inactive_filters(self):
        """Input: None.
        Output: Returns list of all currently inactive filters (class member)."""
        return self.inactive_filters

    def get_add_filter_options_list(self):
        """Input: None.
        Output: Returns list of each addable filter's kind, category and number of resulting project IDs."""
        aslist = []
        for kind, fltr_num_list in self.get_add_filter_options().items():
            for fltr_num in fltr_num_list:
                aslist.append(kind)
                aslist.append(fltr_num[0].get_cat())
                aslist.append(fltr_num[1])
        return aslist

    def add_filter(self, filter):
        """Input: A filter instance.
        Output: Adds a filter to the active filters list; applies filter and updates list of results pids;
        uses caching if memoizing is turned on in constants."""
        self.active_filters.append(filter)
        self.inactive_filters.remove(filter)
        if c.MEMOIZE:
            pids_list_exists = m.get_filters_result_pids_from_memo_table(self.active_filters)
            if not pids_list_exists:
                self.result_pids = self.apply_one_filter(filter)
                m.add_filter_pid_pair_to_db_table(self.active_filters, self.result_pids)
            else:
                self.result_pids = pids_list_exists
        else:
            self.result_pids = self.apply_one_filter(filter)

    def remove_filter(self, filter):
        """Input: A filter instance.
        Output: Adds a filter to the inactive filters list; "un-applies" filter and updates list of results pids;
        uses caching if memoizing is turned on in constants."""
        try:
            self.active_filters.remove(filter)
            self.inactive_filters.append(filter)
            if c.MEMOIZE:
                pids_list_exists = m.get_filters_result_pids_from_memo_table(self.active_filters)
                if not pids_list_exists:
                    self.result_pids = self.apply_all_filters()
                    m.add_filter_pid_pair_to_db_table(self.active_filters, self.result_pids)
                else:
                    self.result_pids = pids_list_exists
            else:
                self.result_pids = self.apply_all_filters()
        except ValueError:
            print("Cannot remove this filter, it wasn't added in the first place")

    def apply_one_filter(self, filter):
        """Input: A filter instance.
        Output: Applies the given filter to this class instance's results pids, and updates results pids."""
        return filter.apply(self.result_pids)

    def apply_one_filter_to_given_pids(self, filter, pids):
        """Input: A filter instance; a list of pids.
        Output: Returns list of pids after applying the given filter to the given pids."""
        return filter.apply(pids)

    def apply_all_filters(self):
        """Input: None.
        Output: Returns this class instance's results pids after applying all active filters."""
        self.result_pids = w.get_union_of_lists(sql_fltr.pids_phase_1(), sql_fltr.pids_phase_2())
        for filter in self.active_filters:
            self.result_pids = filter.apply(self.result_pids)
        return self.result_pids

    def apply_all_given_filters_to_all_pids(self, filters: list):
        """Input: A list of filter instances.
        Output: Returns list of pids after applying all given filters to all pids."""
        pids = w.get_union_of_lists(sql_fltr.pids_phase_1(), sql_fltr.pids_phase_2())
        for filter in filters:
            if len(pids) == 0:
                break
            pids = filter.apply(pids)
        return pids

    def get_remove_filter_options(self):
        """Input: None.
        Output: Returns dictionary of all active filter kinds to active filter categories."""
        options_dict = {}
        for fltr in self.active_filters:
            kind = fltr.get_kind()
            if kind in options_dict:
                options_dict[kind].append(fltr)
            else:
                options_dict[kind] = [fltr]
        return options_dict

    def get_add_filter_options(self):
        """Input: None.
        Output: Returns dictionary of all inactive filter kinds to
        inactive filter categories and the number of pids that would remain if this filter were applied;
        uses caching if memoizing is turned on in constants."""
        options_dict = {}
        for fltr in self.inactive_filters:  # look at all the inactive filters one by one
            if c.MEMOIZE:
                # make filter list for each fltr: active_filters + fltr
                temp_active_filters = copy.deepcopy(self.active_filters)
                temp_active_filters.append(fltr)
                # to try to get the pids from the memo table
                temp_pids_list_exists = m.get_filters_result_pids_from_memo_table(temp_active_filters)
                #if len(temp_pids_list_exists) <= 0:
                if not temp_pids_list_exists:
                    # get pids with current temp filters
                    temp_pids = fltr.apply(self.result_pids)
                    m.add_filter_pid_pair_to_db_table(temp_active_filters, temp_pids)
                else:
                    temp_pids = temp_pids_list_exists
            else:
                temp_pids = fltr.apply(self.result_pids)

            temp_len = len(temp_pids)
            if temp_len > 0:
                kind = fltr.get_kind()
                if kind in options_dict:
                    options_dict[kind].append((fltr, temp_len))
                else:
                    options_dict[kind] = [(fltr, temp_len)]

        options_dict = options_dict
        return options_dict

    def add_or_remove_filter(self, filter):
        """Input: A filter instance.
        Output: If the filter is currently active, removes the given filter, otherwise adds it."""
        if filter in self.active_filters:
            self.remove_filter(filter)
        else:
            self.add_filter(filter)
