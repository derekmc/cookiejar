
import collections
import csv

class Table:

    def __init__(self, customNamedTuple):
        self.TupleObject = customNamedTuple
        self.rows = {}
        pass

    def __contains__(self, key):
        return key in self.rows

    def __getitem__(self, key):
        return self.rows[key]

    def __setitem__(self, key, value):
        self.rows[key] = value

    def __delitem__(self, key):
        del self.rows

    def clear(self):
        self.rows = {}

    def addRow(self, *row):
        self.rows[row[0]] = self.TupleObject(*row)

    def getColumnField(self, key, field):
        getattr(self.rows[key], field)

    def setColumnField(self, key, field, value):
        setattr(self.rows[key], field, value)

    def getColumnIndex(self, key, index):
        self.rows[key][index]

    def setColumnIndex(self, key, index, value):
        self.rows[key][index] = value

    def __str__(self):
        fields = self.TupleObject._fields
        result = ""
        result += (", ").join(self.TupleObject._fields)
        for key in self.rows:
            row = self.rows[key]
            result += "\n" + (", ").join(row)
        return result

    def load(self, filename):
        self.clear()
        with open(filename) as csvfile:
            #reader = csv.reader(csvfile, dialect="excel", quoting=csv.QUOTE_ALL, delimiter=",")
            reader = csv.reader(csvfile)
            next(reader) # skip first row.
            for row in reader:
                self.addRow(*row)

    def save(self, filename):
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, dialect="excel", quoting=csv.QUOTE_ALL, delimiter=',')
            writer.writerow(self.TupleObject._fields)
            for key in self.rows:
                writer.writerow(self.rows[key])

def TestSave():
    Person = collections.namedtuple("Person", "name email password")
    people = Table(Person)
    people.addRow("cl", "bla@host.com", "opensesame123")
    people.addRow("joe", "bla@host.com", "opensesame123")
    people.addRow("bill", "bla@host.com", 7)
    people.save('people.csv')

def TestLoad():
    Person = collections.namedtuple("Person", "name email password")
    people = Table(Person)
    people.load('people.csv')
    print("people:")
    print(people)

def Test():
    TestLoad()

if __name__ == "__main__":
    Test()

