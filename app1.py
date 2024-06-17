from flask import Flask, render_template, request
import csv

app = Flask(__name__)

class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add(self, data):
        if self.size < 5:
            new_node = ListNode(data)
            if self.head is None:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node
            self.size += 1

    def traverse(self):
        current = self.head
        result = []
        while current:
            result.append(current.data)
            current = current.next
        return result

class TreeNode:
    def __init__(self, apartment):
        self.apartment = apartment
        self.left = None
        self.right = None
        self.left_list = LinkedList()
        self.right_list = LinkedList()

    def add_apartment(self,data,side):
        if side == "left":
            self.left_list.add(data)
        elif side == "right":
            self.right_list.add(data)
        else:
            print("Invalid side. Please choose 'left' or 'right'.")

root = TreeNode("Deccan Enclave")

with open('apartment.csv') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for line in csv_reader:
        if line[0] == '1':
            root.add_apartment(line, "left")
        elif line[0] == '2':
            root.add_apartment(line, "right")
        else:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blockwiselist', methods=['POST'])
def blockwiselist():
    block = int(request.form['block'])
    b = blockwiselist(block)
    return render_template('blockwiselist.html', block_data=b)

@app.route('/details', methods=['POST'])
def details():
    block = int(request.form['block'])
    house = int(request.form['house'])
    d = details(block, house)
    return render_template('details.html', details_data=d)

@app.route('/house_availability', methods=['POST'])
def house_availability():
    bhk = int(request.form['bhk'])
    house = house_availability(bhk)
    return render_template('house_availability.html', house_data=house)

@app.route('/maintenance', methods=['POST'])
def maintenance():
    block = int(request.form['block'])
    house = int(request.form['house'])
    m = maintenance(block, house)
    return render_template('maintenance.html', maintenance_data=m)

@app.route('/updation', methods=['POST'])
def updation():
    block = int(request.form['block'])
    house = int(request.form['house'])
    occ = request.form['occ']
    u = updation(block, house, occ)
    return render_template('updation.html', updation_result=u)

if __name__ == '__main__':
    app.run(debug=True)
