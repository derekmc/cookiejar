
import collections
import csv

# if this needs to be fast, write to a ramdisk or something like that.

class Table:
    def __init__(self, customNamedTuple, filename):
        self.TupleObject = customNamedTuple
        self.rows = {}
        self.filename = filename
        pass

    def keys(self):
        return self.rows.keys()

    def __contains__(self, key):
        return key in self.rows

    def __getitem__(self, key):
        return self.rows[key]

    def __setitem__(self, key, value):
        self.rows[key] = value

    def __delitem__(self, key):
        del self.rows[key]

    def clear(self):
        self.rows = {}

    def addRow(self, *row):
        if self.TupleObject:
            datarow = self.TupleObject(*row)
        else:
            datarow = row
        self.rows[row[0]] = datarow

    def getColumnField(self, key, field):
        getattr(self.rows[key], field)

    def setColumnField(self, key, field, value):
        setattr(self.rows[key], field, value)

    def getColumnIndex(self, key, index):
        return self.rows[key][index]

    def setColumnIndex(self, key, index, value):
        self.rows[key][index] = value

    def __str__(self):
        result = ""
        if self.TupleObject:
            fields = self.TupleObject._fields
            result += (", ").join(self.TupleObject._fields)
        for key in self.rows:
            row = self.rows[key]
            result += "\n" + (", ").join(row)
        return result

    def load(self):
        self.clear()
        try:
            with open(self.filename) as csvfile:
                #reader = csv.reader(csvfile, dialect="excel", quoting=csv.QUOTE_ALL, delimiter=",")
                reader = csv.reader(csvfile)
                next(reader) # skip first row.
                for row in reader:
                    self.addRow(*row)
            return True
        except IOError:
            return False

    def save(self):
        try:
            with open(self.filename, 'w') as csvfile:
                writer = csv.writer(csvfile, dialect="excel", quoting=csv.QUOTE_ALL, delimiter=',')
                if self.TupleObject:
                    writer.writerow(self.TupleObject._fields)
                else:
                    writer.writerow([])
                for key in self.rows:
                    writer.writerow(self.rows[key])
            return True
        except IOError:
            return False

def TestSave():
    Person = collections.namedtuple("Person", "name email password")
    people = Table(Person, "people.csv")
    people.addRow("cl", "bla@host.com", "opensesame123")
    people.addRow("joe", "bla@host.com", "opensesame123")
    people.addRow("bill", "bla@host.com", 7)
    people.save()

def TestLoad():
    Person = collections.namedtuple("Person", "name email password")
    people = Table(Person, "people.csv")
    people.load()
    print("people:")
    print(people)

def Test():
    TestLoad()

if __name__ == "__main__":
    Test()

