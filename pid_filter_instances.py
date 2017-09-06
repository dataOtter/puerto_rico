import pid_filter_classes as cl
import PR_SQL_queries as prs
import constants as c
import wrangling_functions as w


class FilterSystem:
    def __init__(self):
        g1 = cl.GenderFilter("M")
        g2 = cl.GenderFilter("F")
        g3 = cl.GenderFilter("TG")

        a1 = cl.AgeFilter("0-18")
        a2 = cl.AgeFilter("19-24")
        a3 = cl.AgeFilter("25-40")
        a4 = cl.AgeFilter("41-100")

        mind1 = cl.MinDrugsFilter("1")
        mind2 = cl.MinDrugsFilter("2-3")
        mind3 = cl.MinDrugsFilter("4-7")
        mind4 = cl.MinDrugsFilter("8")

        maxd1 = cl.MaxDrugsFilter("1")
        maxd2 = cl.MaxDrugsFilter("2-3")
        maxd3 = cl.MaxDrugsFilter("4-7")
        maxd4 = cl.MaxDrugsFilter("8")

        self.filters_tuple = (g1, g2, g3, a1, a2, a3, a4, mind1, mind2, mind3, mind4, maxd1, maxd2, maxd3, maxd4)
        self.filters_dict = {"Gender": (g1, g2, g3),
                             "Age": (a1, a2, a3, a4),
                             "MinDrugUse": (mind1, mind2, mind3, mind4),
                             "MaxDrugUse": (maxd1, maxd2, maxd3, maxd4)}
        self.inactive_filters = list(self.filters_tuple)
        self.active_filters = []
        self.result_pids = w.get_union_of_lists(prs.pids_phase_1(), prs.pids_phase_2())

    def add_filter(self, filter):
        self.result_pids = self.apply_one_filter(filter)
        self.active_filters.append(filter)
        self.inactive_filters.remove(filter)

    def remove_filter(self, filter):
        try:
            self.active_filters.remove(filter)
            self.apply_all_filters()
            self.inactive_filters.append(filter)
        except ValueError:
            print("Cannot remove this filter, it wasn't added in the first place")

    def apply_one_filter(self, filter):
        return filter.apply(self.result_pids)

    def apply_all_filters(self):
        self.result_pids = w.get_union_of_lists(prs.pids_phase_1(), prs.pids_phase_2())
        for filter in self.active_filters:
            self.result_pids = filter.apply(self.result_pids)
        return self.result_pids

    def get_remove_filter_options(self):
        options_dict = {}
        for filter in self.active_filters:
            kind = filter.get_kind()
            if kind in options_dict:
                options_dict[kind].append(filter)
            else:
                options_dict[kind] = [filter]
        return options_dict

    def get_add_filter_options(self):
        options_dict = {}
        for filter in self.inactive_filters:
            temp_pids = filter.apply(self.result_pids)
            temp_len = len(temp_pids)
            if temp_len > 0:
                kind = filter.get_kind()
                if kind in options_dict:
                    options_dict[kind].append((filter, temp_len))
                else:
                    options_dict[kind] = [(filter, temp_len)]
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
