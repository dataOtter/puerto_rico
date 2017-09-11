"""This is an abstract base class representing a data-flow module"""
import abc
import PR_SQL_queries as prs
import constants as c


class BaseNode:
    __metaclass__ = abc.ABCMeta

    def __init__(self, k):
        self.kind = k

    @abc.abstractmethod
    def receive_data(self, data, caller):
        """This must be overridden in the derived class"""
        raise Exception("BaseNode is abstract or derived class did not specify receive_data method")

    @abc.abstractmethod
    def connect_input(self, input_node):
        """This must be overridden in the derived class"""
        raise Exception("BaseNode is abstract or derived class did not specify connect_input method")

    @abc.abstractmethod
    def connect_output(self, output_node):
        """This must be overridden in the derived class"""
        raise Exception("BaseNode is abstract or derived class did not specify connect_output method")

    @abc.abstractmethod
    def do_work(self):
        """This must be overridden in the derived class"""
        raise Exception("BaseNode is abstract or derived class did not specify do_work method")

    @abc.abstractmethod
    def get_cat(self):
        """This must be overridden in the derived class"""
        raise Exception("BaseNode is abstract or derived class did not specify get_cat method")

    @abc.abstractmethod
    def get_kind_and_cat(self):
        """This must be overridden in the derived class"""
        raise Exception("BaseNode is abstract or derived class did not specify get_kind_and_cat method")

    def get_kind(self):
        return self.kind


class GenderAdapter(BaseNode):
    __metaclass__ = abc.ABCMeta

    def __init__(self, gen):
        super(GenderAdapter, self).__init__("Gender")
        self.desired_gender = gen
        self.input_node = None
        self.output_node = None
        self.input_data = []

    def receive_data(self, data, caller):
        if caller == self.input_node:
            self.input_data.append(data)
        else:
            raise Exception("Caller is not the registered input_node")

    def connect_input(self, input_node):
        if input_node is not None:
            if input_node.output_node != self and input_node.output_node is not None:
                raise Exception("Inconsistent connection attempted")
        self.input_node = input_node

    def connect_output(self, output_node):
        if output_node is not None:
            if output_node.input_node != self and output_node.input_node is not None:
                raise Exception("Inconsistent connection attempted")
        self.output_node = output_node

    def do_work(self):
        if self.output_node is None:
            raise Exception("Output not set on adapter")

        if len(self.input_data) > 0:
            ans_data = []
            if self.desired_gender == "M":
                ans_data = prs.pids_males(self.input_data[0])
            elif self.desired_gender == "F":
                ans_data = prs.pids_females(self.input_data[0])
            elif self.desired_gender == "TG":
                ans_data = prs.pids_transgender(self.input_data[0])

            self.output_node.receive_data(ans_data, self)


    def get_cat(self):
        return str(self.desired_gender)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class AgeAdapter(BaseNode):
    __metaclass__ = abc.ABCMeta

    def __init__(self, cat):
        super(AgeAdapter, self).__init__("Age")
        self.desired_age_cat = cat
        self.input_node = None
        self.output_node = None
        self.input_data = []

    @abc.abstractmethod
    def receive_data(self, data, caller):
        if caller == self.input_node:
            # self.input_data.extend(data)
            self.input_data = data
        else:
            raise Exception("Caller is not the registered input_node")

    @abc.abstractmethod
    def connect_input(self, input_node):
        self.input_node = input_node

    @abc.abstractmethod
    def connect_output(self, output_node):
        self.output_node = output_node

    @abc.abstractmethod
    def do_work(self):
        if len(self.input_data) > 0:
            ans_data = []
            if self.desired_age_cat == "0-18":
                ans_data = prs.pids_age_range(self.input_data, min_age=0, max_age=18)
            elif self.desired_age_cat == "19-24":
                ans_data = prs.pids_age_range(self.input_data, min_age=19, max_age=24)
            elif self.desired_age_cat == "25-40":
                ans_data = prs.pids_age_range(self.input_data, min_age=25, max_age=40)
            elif self.desired_age_cat == "41-100":
                ans_data = prs.pids_age_range(self.input_data, min_age=41, max_age=100)

            self.output_node.receive_data(ans_data, self)

        #raise Exception("BaseNode is abstract or derived class did not specify do_work method")

    def get_cat(self):
        return str(self.desired_age_cat)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class MinDrugUseAdapter(BaseNode):
    __metaclass__ = abc.ABCMeta

    def __init__(self, amnt):
        super(MinDrugUseAdapter, self).__init__("MinDrugUse")
        self.daily_drug_use = amnt
        self.input_node = None
        self.output_node = None
        self.input_data = []

    @abc.abstractmethod
    def receive_data(self, data, caller):
        if caller == self.input_node:
            # self.input_data.extend(data)
            self.input_data = data
        else:
            raise Exception("Caller is not the registered input_node")

    @abc.abstractmethod
    def connect_input(self, input_node):
        self.input_node = input_node

    @abc.abstractmethod
    def connect_output(self, output_node):
        self.output_node = output_node

    @abc.abstractmethod
    def do_work(self):
        if len(self.input_data) > 0:
            ans_data = []
            if self.daily_drug_use == "1":
                ans = prs.pids_min_drug_use_per_day(self.input_data, min_use_per_day=1)
            elif self.daily_drug_use == "2-3":
                ans = prs.pids_min_drug_use_per_day(self.input_data, min_use_per_day=2)
            elif self.daily_drug_use == "4-7":
                ans = prs.pids_min_drug_use_per_day(self.input_data, min_use_per_day=4)
            elif self.daily_drug_use == "8":
                ans = prs.pids_min_drug_use_per_day(self.input_data, min_use_per_day=8)

            self.output_node.receive_data(ans_data, self)

        #raise Exception("BaseNode is abstract or derived class did not specify do_work method")

    def get_cat(self):
        return str(self.daily_drug_use)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class MaxDrugUseAdapter(BaseNode):
    __metaclass__ = abc.ABCMeta

    def __init__(self, amnt):
        super(MaxDrugUseAdapter, self).__init__("MaxDrugUse")
        self.daily_drug_use = amnt
        self.input_node = None
        self.output_node = None
        self.input_data = []

    @abc.abstractmethod
    def receive_data(self, data, caller):
        if caller == self.input_node:
            # self.input_data.extend(data)
            self.input_data = data
        else:
            raise Exception("Caller is not the registered input_node")

    @abc.abstractmethod
    def connect_input(self, input_node):
        self.input_node = input_node

    @abc.abstractmethod
    def connect_output(self, output_node):
        self.output_node = output_node

    @abc.abstractmethod
    def do_work(self):
        if len(self.input_data) > 0:
            ans_data = []
            if self.daily_drug_use == "1":
                ans = prs.pids_max_drug_use_per_day(self.input_data, max_use_per_day=1)
            elif self.daily_drug_use == "2-3":
                ans = prs.pids_max_drug_use_per_day(self.input_data, max_use_per_day=2)
            elif self.daily_drug_use == "4-7":
                ans = prs.pids_max_drug_use_per_day(self.input_data, max_use_per_day=4)
            elif self.daily_drug_use == "8":
                ans = prs.pids_max_drug_use_per_day(self.input_data, max_use_per_day=8)

            self.output_node.receive_data(ans_data, self)

        #raise Exception("BaseNode is abstract or derived class did not specify do_work method")

    def get_cat(self):
        return str(self.daily_drug_use)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())