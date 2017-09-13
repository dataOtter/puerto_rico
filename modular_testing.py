"""This is the testing file for an abstract base class representing a data-flow module"""
import abc
from random import randint


class BaseNode:
    __metaclass__ = abc.ABCMeta

    def __init__(self, k):
        self.kind = k
        self.done = False
        self.counter = 0

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


class Printer(BaseNode):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(Printer, self).__init__("Printer")
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
        raise Exception("Printer has no output")

    def assign_input_node(self, input_node):
        if input_node is not None:
            if not input_node.has_as_output_node(self) and not input_node.has_as_output_node(None):
                raise Exception("Inconsistent connection attempted")
        self.input_node = input_node

    def assign_output_node(self, output_node):
        raise Exception("Inconsistent connection attempted - sink does have an output connection")

    def do_work(self):
        if len(self.input_data) > 0:
            for num in self.input_data[0]:
                print(num)
            self.input_data = self.input_data[1:]
            self.counter += 1
            if self.counter == 100:
                self.done = True

    def get_cat(self):
        raise Exception("Printer does not have a category")

    def get_kind_and_cat(self):
        return str(self.get_kind())


class Source(BaseNode):
    __metaclass__ = abc.ABCMeta

    def __init__(self, generator):
        super(Source, self).__init__("Numbers")
        self.generator = generator
        self.output_node = None
        self.constant = 0

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

        if self.generator == "bursty":
            x, n = 0, randint(1, 10)
            while x < n:
                self.output_node.receive_data([randint(50, 55)], self)
                x += 1
        elif self.generator == "constant":
            self.constant += 1
            self.output_node.receive_data([self.constant], self)

        self.counter += 1
        if self.counter == 100:
            self.done = True

    def get_cat(self):
        return str(self.generator)

    def get_kind_and_cat(self):
        return str(self.get_kind() + " " + self.get_cat())


class DrainAdapter(BaseNode):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(DrainAdapter, self).__init__("Drain")
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
            for e in self.input_data:
                for element in e:
                    ans_data.append(element)
            self.output_node.receive_data(ans_data, self)
            self.input_data = []
            self.counter += 1
            if self.counter == 100:
                self.done = True

    def get_cat(self):
        raise Exception("DrainAdapter does not have a category")

    def get_kind_and_cat(self):
        return str(self.get_kind())


class MaxMerge(BaseNode):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(MaxMerge, self).__init__("Max")
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
            stop = False
            ans_data = []
            while not stop:
                ans_data.append(max(self.input_data1[0][0], self.input_data2[0][0]))

                self.input_data1[0] = self.input_data1[0][1:]
                self.input_data2[0] = self.input_data2[0][1:]

                if len(self.input_data1[0]) == 0:
                    self.input_data1 = self.input_data1[1:]
                if len(self.input_data2[0]) == 0:
                    self.input_data2 = self.input_data2[1:]

                if len(self.input_data1) == 0:
                    stop = True
                if len(self.input_data2) == 0:
                    stop = True

            self.output_node.receive_data(ans_data, self)
            self.counter += 1
            if self.counter == 100:
                self.done = True

    def get_cat(self):
        raise Exception("MaxMerge does not have a category")

    def get_kind_and_cat(self):
        return str(self.get_kind())


def get_modules_dict():
    modules_dict = {"printer": '',
                    "numbers": {"bursty": '',
                            "constant": ''},
                    "drain": '',
                    "max": ''}
    return modules_dict


def get_node(name: str):
    if name == 'numbers bursty':
        return Source("bursty")
    elif name == 'numbers constant':
        return Source("constant")
    elif name == 'drain':
        return DrainAdapter()
    elif name == 'max':
        return MaxMerge()
    elif name == 'printer':
        return Printer()


'''bursty = Source("bursty")
constant = Source("constant")
drain1 = DrainAdapter()
drain2 = DrainAdapter()
max_merge = MaxMerge()
printer = Printer()

bursty.assign_output_node(drain1)
drain1.assign_input_node(bursty)
drain1.assign_output_node(max_merge)
max_merge.assign_input_node(drain1)

constant.assign_output_node(drain2)
drain2.assign_input_node(constant)
drain2.assign_output_node(max_merge)
max_merge.assign_input_node(drain2)

max_merge.assign_output_node(printer)
printer.assign_input_node(max_merge)


modules = [bursty, constant, drain1, drain2, max_merge, printer]

done = False
while not done:
    done_counter = 0
    for m in modules:
        if not m.is_done():
            m.do_work()
        else:
            done_counter += 1
    if done_counter == len(modules):
        done = True'''
