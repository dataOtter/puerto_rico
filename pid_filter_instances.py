import pid_filter_classes as cl
import PR_SQL_queries as prs
import constants as c
import wrangling_functions as w
import memoize_to_db as m
import copy


class FilterSystem:
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
        self.result_pids = w.get_union_of_lists(prs.pids_phase_1(), prs.pids_phase_2())

    def get_result_pids(self):
        return self.result_pids

    def get_active_filters(self):
        return self.active_filters

    def get_inactive_filters(self):
        return self.inactive_filters

    def add_filter(self, filter):
        self.active_filters.append(filter)
        self.inactive_filters.remove(filter)
        if c.MEMOIZE:
            pids_list_exists = m.get_filters_result_pids_from_memo_table(self.active_filters)
            #if len(pids_list_exists) <= 0:
            if not pids_list_exists:
                self.result_pids = self.apply_one_filter(filter)
                m.add_filter_pid_pair_to_db_table(self.active_filters, self.result_pids)
            else:
                self.result_pids = pids_list_exists
        else:
            self.result_pids = self.apply_one_filter(filter)

    def remove_filter(self, filter):
        try:
            self.active_filters.remove(filter)
            self.inactive_filters.append(filter)
            if c.MEMOIZE:
                pids_list_exists = m.get_filters_result_pids_from_memo_table(self.active_filters)
                #if len(pids_list_exists) <= 0:
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
        return filter.apply(self.result_pids)

    def apply_one_filter_to_given_pids(self, filter, pids):
        return filter.apply(pids)

    def apply_all_filters(self):
        self.result_pids = w.get_union_of_lists(prs.pids_phase_1(), prs.pids_phase_2())
        for filter in self.active_filters:
            self.result_pids = filter.apply(self.result_pids)
        return self.result_pids

    def apply_all_given_filters_to_all_pids(self, filters: list):
        pids = w.get_union_of_lists(prs.pids_phase_1(), prs.pids_phase_2())
        for filter in filters:
            if len(pids) == 0:
                break
            pids = filter.apply(pids)
        return pids

    def get_remove_filter_options(self):
        options_dict = {}
        for fltr in self.active_filters:
            kind = fltr.get_kind()
            if kind in options_dict:
                options_dict[kind].append(fltr)
            else:
                options_dict[kind] = [fltr]
        return options_dict

    def get_add_filter_options(self):
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

        '''for fltr in self.inactive_filters:
            temp_pids = fltr.apply(self.result_pids)
            temp_len = len(temp_pids)
            if temp_len > 0:
                kind = fltr.get_kind()
                if kind in options_dict:
                    options_dict[kind].append((fltr, temp_len))
                else:
                    options_dict[kind] = [(fltr, temp_len)]'''
        options_dict = options_dict
        return options_dict

    def add_or_remove_filter(self, filter):
        if filter in self.active_filters:
            self.remove_filter(filter)
        else:
            self.add_filter(filter)





'''p1_ids = prs.pids_phase_1()

res1 = g1.apply(p1_ids)
flist = []
flist.append(g1)

res = p1_ids
for f in flist:
    print("Before applying filter " + f.toString() + " we have " + str(len(res)) + " results")
    res = f.apply(res)
    print("After applying filter " + f.toString() + " we have " + str(len(res)) + " results")'''
