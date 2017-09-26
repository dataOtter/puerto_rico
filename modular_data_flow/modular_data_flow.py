"""This is an abstract base class representing a data-flow module"""
import abc

from ETL import wrangling_functions as w
from filters import filter_SQL_queries as prs


class BaseNode:
    __metaclass__ = abc.ABCMeta

    def __init__(self, k):
        self.kind = k
        self.done = False

    @abc.abstractmethod
    def is_done(self):
        """This must be overridden in the derived class"""
        raise Exception("BaseNode is abstract or derived class did not specify is_done method")

    @abc.abstractmethod
    def receive_data(self, data, caller):
        """This must be overridden in the derived class"""
        raise Exception("BaseNode is abstract or derived class did not specify receive_data method")

    @abc.abstractmethod
    def has_as_input_node(self, input_node):
        """This must be overridden in the derived class"""
        raise Exception("BaseNode is abstract or derived class did not specify has_as_input_node method")

    @abc.abstractmethod
    def has_as_output_node(self, output_node):
        """This must be overridden in the derived class"""
        raise Exception("BaseNode is abstract or derived class did not specify has_as_output_node method")

    @abc.abstractmethod
    def assign_input_node(self, input_node):
        """This must be overridden in the derived class"""
        raise Exception("BaseNode is abstract or derived class did not specify connect_input method")

    @abc.abstractmethod
    def assign_output_node(self, output_node):
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


class PidSink(BaseNode):
    __metaclass__ = abc.ABCMeta

    def __init__(self, type):
        super(PidSink, self).__init__("Pids")
        self.type = type
        self.input_node = None
        self.input_data = []

    def is_done(self):
        return self.done

    def receive_data(self, data, caller):
        if caller == self.input_node:
            self.input_data.append(data)
        else:
            raise Exception("Caller is not the registered input_node")

    def has_as_input_node(self, input_node):
        return self.input_node == input_node

    def has_as_output_node(self, output_node):
        raise Exception("Sink has no output")

    def assign_input_node(self, input_node):
        if input_node is not None:
            if not input_node.has_as_output_node(self) and not input_node.has_as_output_node(None):
                raise Exception("Inconsistent connection attempted")
        self.input_node = input_node

    def assign_output_node(self, output_node):
        raise Exception("Inconsistent connection attempted - sink does have an output connection")

    def do_work(self):
        if len(self.input_data) > 0:
            if self.type == "print_count":
                print("There are " + str(len(self.input_data[0])) + " participants that match your criteria.")
            elif self.type == "print_pids":
                print("These are the Project IDs of the participants that match your criteria:")
                for pid in self.input_data[0]:
                    print(pid)
            self.input_data = self.input_data[1:]

    def get_cat(self):
        return str(self.type)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class PidSource(BaseNode):
    __metaclass__ = abc.ABCMeta

    def __init__(self, phase):
        super(PidSource, self).__init__("Pids")
        self.phase = phase
        self.output_node = None

    def is_done(self):
        return self.done

    def receive_data(self, data, caller):
        raise Exception("Source does not take any input or data")

    def has_as_input_node(self, input_node):
        raise Exception("Source has no input")

    def has_as_output_node(self, output_node):
        return self.output_node == output_node

    def assign_input_node(self, input_node):
        raise Exception("Inconsistent connection attempted - source does not have an input connection")

    def assign_output_node(self, output_node):
        if output_node is not None:
            if not output_node.has_as_input_node(self) and not output_node.has_as_input_node(None):
                raise Exception("Inconsistent connection attempted")
        self.output_node = output_node

    def do_work(self):
        if self.output_node is None:
            raise Exception("Output not set on adapter")

        ans_data = []
        if self.phase == "P1":
            ans_data = prs.pids_phase_1()
        elif self.phase == "P2":
            ans_data = prs.pids_phase_2()

        self.output_node.receive_data(ans_data, self)
        self.done = True

    def get_cat(self):
        return str(self.phase)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class GenderAdapter(BaseNode):
    __metaclass__ = abc.ABCMeta

    def __init__(self, gen):
        super(GenderAdapter, self).__init__("Gender")
        self.desired_gender = gen
        self.input_node = None
        self.output_node = None
        self.input_data = []

    def is_done(self):
        return self.done

    def receive_data(self, data, caller):
        if caller == self.input_node:
            self.input_data.append(data)
        else:
            raise Exception("Caller is not the registered input_node")

    def has_as_input_node(self, input_node):
        return self.input_node == input_node

    def has_as_output_node(self, output_node):
        return self.output_node == output_node

    def assign_input_node(self, input_node):
        if input_node is not None:
            if not input_node.has_as_output_node(self) and not input_node.has_as_output_node(None):
                raise Exception("Inconsistent connection attempted")
        self.input_node = input_node

    def assign_output_node(self, output_node):
        if output_node is not None:
            if not output_node.has_as_input_node(self) and not output_node.has_as_input_node(None):
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
            self.input_data = self.input_data[1:]

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

    def is_done(self):
        return self.done

    def receive_data(self, data, caller):
        if caller == self.input_node:
            self.input_data.append(data)
        else:
            raise Exception("Caller is not the registered input_node")

    def has_as_input_node(self, input_node):
        return self.input_node == input_node

    def has_as_output_node(self, output_node):
        return self.output_node == output_node

    def assign_input_node(self, input_node):
        if input_node is not None:
            if not input_node.has_as_output_node(self) and not input_node.has_as_output_node(None):
                raise Exception("Inconsistent connection attempted")
        self.input_node = input_node

    def assign_output_node(self, output_node):
        if output_node is not None:
            if not output_node.has_as_input_node(self) and not output_node.has_as_input_node(None):
                raise Exception("Inconsistent connection attempted")
        self.output_node = output_node

    def do_work(self):
        if self.output_node is None:
            raise Exception("Output not set on adapter")

        if len(self.input_data) > 0:
            ans_data = []
            if self.desired_age_cat == "0-18":
                ans_data = prs.pids_age_range(self.input_data[0], min_age=0, max_age=18)
            elif self.desired_age_cat == "19-24":
                ans_data = prs.pids_age_range(self.input_data[0], min_age=19, max_age=24)
            elif self.desired_age_cat == "25-40":
                ans_data = prs.pids_age_range(self.input_data[0], min_age=25, max_age=40)
            elif self.desired_age_cat == "41-100":
                ans_data = prs.pids_age_range(self.input_data[0], min_age=41, max_age=100)

            self.output_node.receive_data(ans_data, self)
            self.input_data = self.input_data[1:]

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

    def is_done(self):
        return self.done

    def receive_data(self, data, caller):
        if caller == self.input_node:
            self.input_data.append(data)
        else:
            raise Exception("Caller is not the registered input_node")

    def has_as_input_node(self, input_node):
        return self.input_node == input_node

    def has_as_output_node(self, output_node):
        return self.output_node == output_node

    def assign_input_node(self, input_node):
        if input_node is not None:
            if not input_node.has_as_output_node(self) and not input_node.has_as_output_node(None):
                raise Exception("Inconsistent connection attempted")
        self.input_node = input_node

    def assign_output_node(self, output_node):
        if output_node is not None:
            if not output_node.has_as_input_node(self) and not output_node.has_as_input_node(None):
                raise Exception("Inconsistent connection attempted")
        self.output_node = output_node

    def do_work(self):
        if self.output_node is None:
            raise Exception("Output not set on adapter")

        if len(self.input_data) > 0:
            ans_data = []
            if self.daily_drug_use == "1":
                ans_data = prs.pids_min_drug_use_per_day(self.input_data[0], min_use_per_day=1)
            elif self.daily_drug_use == "2-3":
                ans_data = prs.pids_min_drug_use_per_day(self.input_data[0], min_use_per_day=2)
            elif self.daily_drug_use == "4-7":
                ans_data = prs.pids_min_drug_use_per_day(self.input_data[0], min_use_per_day=4)
            elif self.daily_drug_use == "8":
                ans_data = prs.pids_min_drug_use_per_day(self.input_data[0], min_use_per_day=8)

            self.output_node.receive_data(ans_data, self)
            self.input_data = self.input_data[1:]

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

    def is_done(self):
        return self.done

    def receive_data(self, data, caller):
        if caller == self.input_node:
            self.input_data.append(data)
        else:
            raise Exception("Caller is not the registered input_node")

    def has_as_input_node(self, input_node):
        return self.input_node == input_node

    def has_as_output_node(self, output_node):
        return self.output_node == output_node

    def assign_input_node(self, input_node):
        if input_node is not None:
            if not input_node.has_as_output_node(self) and not input_node.has_as_output_node(None):
                raise Exception("Inconsistent connection attempted")
        self.input_node = input_node

    def assign_output_node(self, output_node):
        if output_node is not None:
            if not output_node.has_as_input_node(self) and not output_node.has_as_input_node(None):
                raise Exception("Inconsistent connection attempted")
        self.output_node = output_node

    def do_work(self):
        if self.output_node is None:
            raise Exception("Output not set on adapter")
        if len(self.input_data) > 0:
            ans_data = []
            if self.daily_drug_use == "1":
                ans = prs.pids_max_drug_use_per_day(self.input_data[0], max_use_per_day=1)
            elif self.daily_drug_use == "2-3":
                ans = prs.pids_max_drug_use_per_day(self.input_data[0], max_use_per_day=2)
            elif self.daily_drug_use == "4-7":
                ans = prs.pids_max_drug_use_per_day(self.input_data[0], max_use_per_day=4)
            elif self.daily_drug_use == "8":
                ans = prs.pids_max_drug_use_per_day(self.input_data[0], max_use_per_day=8)

            self.output_node.receive_data(ans_data, self)
            self.input_data = self.input_data[1:]

    def get_cat(self):
        return str(self.daily_drug_use)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class PidMerger(BaseNode):
    __metaclass__ = abc.ABCMeta

    def __init__(self, merge_type):
        super(PidMerger, self).__init__("Gender")
        self.merge_type = merge_type
        self.input_node1 = None
        self.input_node2 = None
        self.output_node = None
        self.input_data1 = []
        self.input_data2 = []

    def is_done(self):
        return self.done

    def receive_data(self, data, caller):
        if caller == self.input_node1:
            self.input_data1.append(data)
        elif caller == self.input_node2:
            self.input_data2.append(data)
        else:
            raise Exception("Caller is not the registered input_node")

    def has_as_input_node(self, input_node):
        return input_node == self.input_node1 or input_node == self.input_node2

    def has_as_output_node(self, output_node):
        return self.output_node == output_node

    def assign_input_node(self, input_node):
        if input_node is not None:
            if not input_node.has_as_output_node(self) and not input_node.has_as_output_node(None):
                raise Exception("Inconsistent connection attempted")
        if self.input_node1 is None:
            self.input_node1 = input_node
        elif self.input_node2 is None:
            self.input_node2 = input_node
        else:
            raise Exception("Already two inputs connected")

    def assign_output_node(self, output_node):
        if output_node is not None:
            if not output_node.has_as_input_node(self) and not output_node.has_as_input_node(None):
                raise Exception("Inconsistent connection attempted")
        self.output_node = output_node

    def do_work(self):
        if self.output_node is None:
            raise Exception("Output not set on adapter")

        if len(self.input_data1) > 0 and len(self.input_data2) > 0:
            ans_data = []
            if self.merge_type == "union":
                ans_data = w.get_union_of_lists(self.input_data1[0], self.input_data2[0])
            elif self.merge_type == "intersection":
                ans_data = w.get_intersection_of_lists(self.input_data1[0], self.input_data2[0])
            elif self.merge_type == "difference":
                ans_data = w.get_difference_list1_only(self.input_data1[0], self.input_data2[0])

            self.output_node.receive_data(ans_data, self)
            self.input_data1 = self.input_data1[1:]
            self.input_data2 = self.input_data2[1:]

    def get_cat(self):
        return str(self.merge_type)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


p1 = PidSource("P1")
p2 = PidSource("P2")
intersection = PidMerger("intersection")
difference = PidMerger("difference")
men = GenderAdapter("M")
age = AgeAdapter("25-40")
mindrug = MinDrugUseAdapter("2-3")
printer = PidSink("print_count")

p1.assign_output_node(difference)
p2.assign_output_node(difference)
difference.assign_input_node(p2)
difference.assign_input_node(p1)
difference.assign_output_node(men)
men.assign_input_node(difference)
men.assign_output_node(age)
age.assign_input_node(men)
age.assign_output_node(mindrug)
mindrug.assign_input_node(age)
mindrug.assign_output_node(printer)
printer.assign_input_node(mindrug)

modules = [p1, p2, printer, difference, age, mindrug, men]

# must have a point where done is switched to true for each class instance

done = False
while not done:
    done_counter = 0
    for m in modules:
        if not m.is_done():
            m.do_work()
        else:
            done_counter += 1
    if done_counter == len(modules):
        done = True
