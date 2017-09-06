"""This is an abstract base class representing a filter on PID lists"""
import abc
import PR_SQL_queries as prs
import constants as c


class PidFilter:
    __metaclass__ = abc.ABCMeta

    def __init__(self, k):
        self.kind = k

    @abc.abstractmethod
    def apply(self, pids_list):
        """This must be overridden in the derived class"""
        raise Exception("PidFilter is abstract or derived class did not specify apply method")

    @abc.abstractmethod
    def toString(self):
        """This must be overridden in the derived class"""
        raise Exception("PidFilter is abstract or derived class did not specify apply method")

    def get_kind(self):
        return self.kind


class GenderFilter(PidFilter):
    __metaclass__ = abc.ABCMeta

    def __init__(self, gen):
        super(GenderFilter, self).__init__("Gender")
        self.desired_gender = gen

    def apply(self, pids_list):
        ans = []
        if self.desired_gender == "M":
            ans = prs.pids_males(pids_list)
        elif self.desired_gender == "F":
            ans = prs.pids_females(pids_list)
        elif self.desired_gender == "TG":
            ans = prs.pids_transgender(pids_list)
        return ans

    def toString(self):
        return "GenderFilter on " + self.desired_gender


class AgeFilter(PidFilter):
    __metaclass__ = abc.ABCMeta

    def __init__(self, cat):
        super(AgeFilter, self).__init__("Age")
        self.age_category = cat

    def apply(self, pids_list):
        ans = []
        if self.age_category == "0-18":
            ans = prs.pids_age_range(pids_list, min_age=0, max_age=18)
        elif self.age_category == "19-24":
            ans = prs.pids_age_range(pids_list, min_age=19, max_age=24)
        elif self.age_category == "25-40":
            ans = prs.pids_age_range(pids_list, min_age=25, max_age=40)
        elif self.age_category == "40-100":
            ans = prs.pids_age_range(pids_list, min_age=41, max_age=100)
        return ans

    def toString(self):
        return "AgeFilter on " + self.age_category


class MinDrugsFilter(PidFilter):
    __metaclass__ = abc.ABCMeta

    def __init__(self, amnt):
        super(MinDrugsFilter, self).__init__("MinDrugUse")
        self.daily_drug_use = amnt

    def apply(self, pids_list):
        ans = []
        if self.daily_drug_use == "1":
            ans = prs.pids_min_drug_use_per_day(pids_list, min_use_per_day=1)
        elif self.daily_drug_use == "2-3":
            ans = prs.pids_min_drug_use_per_day(pids_list, min_use_per_day=2)
        elif self.daily_drug_use == "4-7":
            ans = prs.pids_min_drug_use_per_day(pids_list, min_use_per_day=4)
        elif self.daily_drug_use == "8":
            ans = prs.pids_min_drug_use_per_day(pids_list, min_use_per_day=8)
        return ans

    def toString(self):
        return "MinDrugFilter on " + self.daily_drug_use


class MaxDrugsFilter(PidFilter):
    __metaclass__ = abc.ABCMeta

    def __init__(self, amnt):
        super(MaxDrugsFilter, self).__init__("MaxDrugUse")
        self.daily_drug_use = amnt

    def apply(self, pids_list):
        ans = []
        if self.daily_drug_use == "1":
            ans = prs.pids_max_drug_use_per_day(pids_list, max_use_per_day=1)
        elif self.daily_drug_use == "2-3":
            ans = prs.pids_max_drug_use_per_day(pids_list, max_use_per_day=2)
        elif self.daily_drug_use == "4-7":
            ans = prs.pids_max_drug_use_per_day(pids_list, max_use_per_day=4)
        elif self.daily_drug_use == "8":
            ans = prs.pids_max_drug_use_per_day(pids_list, max_use_per_day=8)
        return ans

    def toString(self):
        return "MaxDrugFilter on " + self.daily_drug_use
