"""Various filter classes."""
import abc
from filters import filter_SQL_queries as sql_fltr


class PidFilter:
    """This is an abstract base class representing a filter on PID lists."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, k):
        self.kind = k

    @abc.abstractmethod
    def apply(self, pids_list):
        """This must be overridden in the derived class"""
        raise Exception("PidFilter is abstract or derived class did not specify apply method")

    @abc.abstractmethod
    def get_cat(self):
        """This must be overridden in the derived class"""
        raise Exception("PidFilter is abstract or derived class did not specify apply method")

    @abc.abstractmethod
    def get_kind_and_cat(self):
        """This must be overridden in the derived class"""
        raise Exception("PidFilter is abstract or derived class did not specify apply method")

    def get_kind(self):
        return self.kind


class PhaseFilter(PidFilter):
    __metaclass__ = abc.ABCMeta

    def __init__(self, category):
        super(PhaseFilter, self).__init__("Phase")
        self.desired_category = category

    def apply(self, pids_list):
        """Input: List of project IDs.
        Output: Returns list of project IDs after filtering by this filter's category type."""
        ans = []
        if self.desired_category == "1":
            ans = sql_fltr.pids_p1_fltr(pids_list)
        elif self.desired_category == "2":
            ans = sql_fltr.pids_p2_fltr(pids_list)
        elif self.desired_category == "1only":
            ans = sql_fltr.pids_p1_only_fltr(pids_list)
        elif self.desired_category == "2only":
            ans = sql_fltr.pids_p2_only_fltr(pids_list)
        return ans

    def get_cat(self):
        return str(self.desired_category)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class CityFilter(PidFilter):
    __metaclass__ = abc.ABCMeta

    def __init__(self, category):
        super(CityFilter, self).__init__("City")
        self.desired_category = category

    def apply(self, pids_list):
        """Input: List of project IDs.
        Output: Returns list of project IDs after filtering by this filter's category type."""
        ans = []
        if self.desired_category == "Cayey":
            ans = sql_fltr.pids_cayey(pids_list)
        elif self.desired_category == "Cidra":
            ans = sql_fltr.pids_cidra(pids_list)
        elif self.desired_category == "Comerio":
            ans = sql_fltr.pids_comerio(pids_list)
        elif self.desired_category == "Aguas Buenas":
            ans = sql_fltr.pids_aguas_buenas(pids_list)
        elif self.desired_category == "Other":
            ans = sql_fltr.pids_other(pids_list)
        return ans

    def get_cat(self):
        return str(self.desired_category)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class GenderFilter(PidFilter):
    __metaclass__ = abc.ABCMeta

    def __init__(self, gen):
        super(GenderFilter, self).__init__("Gender")
        self.desired_gender = gen

    def apply(self, pids_list):
        """Input: List of project IDs.
        Output: Returns list of project IDs after filtering by this filter's gender type."""
        ans = []
        '''For every category of this filter, add an if statement and SQL filter execution'''
        if self.desired_gender == "Male":
            ans = sql_fltr.pids_males(pids_list)
        elif self.desired_gender == "Female":
            ans = sql_fltr.pids_females(pids_list)
        elif self.desired_gender == "Transgender":
            ans = sql_fltr.pids_transgender(pids_list)
        return ans

    def get_cat(self):
        return str(self.desired_gender)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class AgeFilter(PidFilter):
    __metaclass__ = abc.ABCMeta

    def __init__(self, cat):
        super(AgeFilter, self).__init__("Age")
        self.age_category = cat

    def apply(self, pids_list):
        """Input: List of project IDs.
        Output: Returns list of project IDs after filtering by this filter's age category."""
        ans = []
        if self.age_category == "0-18":
            ans = sql_fltr.pids_age_range(pids_list, min_age=0, max_age=18)
        elif self.age_category == "19-24":
            ans = sql_fltr.pids_age_range(pids_list, min_age=19, max_age=24)
        elif self.age_category == "25-40":
            ans = sql_fltr.pids_age_range(pids_list, min_age=25, max_age=40)
        elif self.age_category == "41-100":
            ans = sql_fltr.pids_age_range(pids_list, min_age=41, max_age=100)
        return ans

    def get_cat(self):
        return str(self.age_category)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class MinDrugsFilter(PidFilter):
    __metaclass__ = abc.ABCMeta

    def __init__(self, amnt):
        super(MinDrugsFilter, self).__init__("MinDrugUse")
        self.daily_drug_use = amnt

    def apply(self, pids_list):
        """Input: List of project IDs.
        Output: Returns list of project IDs after filtering by this filter's minimum drug use category."""
        ans = []
        if self.daily_drug_use == "1":
            ans = sql_fltr.pids_min_drug_use_per_day(pids_list, min_use_per_day=1)
        elif self.daily_drug_use == "2-3":
            ans = sql_fltr.pids_min_drug_use_per_day(pids_list, min_use_per_day=2)
        elif self.daily_drug_use == "4-7":
            ans = sql_fltr.pids_min_drug_use_per_day(pids_list, min_use_per_day=4)
        elif self.daily_drug_use == "8":
            ans = sql_fltr.pids_min_drug_use_per_day(pids_list, min_use_per_day=8)
        return ans

    def get_cat(self):
        return str(self.daily_drug_use)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class MaxDrugsFilter(PidFilter):
    __metaclass__ = abc.ABCMeta

    def __init__(self, amnt):
        super(MaxDrugsFilter, self).__init__("MaxDrugUse")
        self.daily_drug_use = amnt

    def apply(self, pids_list):
        """Input: List of project IDs.
        Output: Returns list of project IDs after filtering by this filter's maximum drug use category."""
        ans = []
        if self.daily_drug_use == "1":
            ans = sql_fltr.pids_max_drug_use_per_day(pids_list, max_use_per_day=1)
        elif self.daily_drug_use == "2-3":
            ans = sql_fltr.pids_max_drug_use_per_day(pids_list, max_use_per_day=2)
        elif self.daily_drug_use == "4-7":
            ans = sql_fltr.pids_max_drug_use_per_day(pids_list, max_use_per_day=4)
        elif self.daily_drug_use == "8":
            ans = sql_fltr.pids_max_drug_use_per_day(pids_list, max_use_per_day=8)
        return ans

    def get_cat(self):
        return str(self.daily_drug_use)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class CountryBornFilter(PidFilter):
    __metaclass__ = abc.ABCMeta

    def __init__(self, category):
        super(CountryBornFilter, self).__init__("CountryBorn")
        self.desired_category = category

    def apply(self, pids_list):
        """Input: List of project IDs.
        Output: Returns list of project IDs after filtering by this filter's category type."""
        ans = []
        if self.desired_category == "PuertoRico":
            ans = sql_fltr.pids_born_pr(pids_list)
        elif self.desired_category == "MainlandUS":
            ans = sql_fltr. pids_born_cont_us(pids_list)
        elif self.desired_category == "DomRep":
            ans = sql_fltr.pids_born_dom_rep(pids_list)
        elif self.desired_category == "Other":
            ans = sql_fltr.pids_born_other(pids_list)
        return ans

    def get_cat(self):
        return str(self.desired_category)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())

