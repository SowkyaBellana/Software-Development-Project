import os
import csv
from flask import Flask, render_template, request, redirect, url_for, flash

# Importing user_check function from password module
from Functions.password import user_check

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Homepage or landing page
@app.route("/", methods=["GET"])
def start():
    if request.method == "GET":
        return render_template("about_us.html")

# Login page and authentication
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("Login_Page.html")
    
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("pass")

        # Authenticating user credentials
        state = user_check(name, password)

        if state:
            return render_template("home.html")
        else:
            flash("Invalid entry. Please try again.", "error")
            return render_template("Login_Page.html")

# Loading data from CSV into TreeNode
class TreeNode:
    def __init__(self, apartment):
        self.apartment = apartment
        self.left_list = LinkedList()
        self.right_list = LinkedList()
        
    def add_apartment(self, data, side):
        if side == "left":
            self.left_list.add(data)
        elif side == "right":
            self.right_list.add(data)
        else:
            print("Invalid side. Please choose 'left' or 'right'.")

# Handling apartment data
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

# Load data from CSV into the TreeNode
def load_data():
    root = TreeNode("Deccan Enclave")
    csv_path = os.path.join('data', 'apartment.csv')
    with open(csv_path) as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for line in csv_reader:
            if line[0] == '1':
                root.add_apartment(line, "left")
            elif line[0] == '2':
                root.add_apartment(line, "right")
            else:
                pass
    return root

# Route for home page
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/queries')
def queries():
    return render_template('queries.html')

# Route for blockwise apartment details
@app.route('/blockwise')
def blockwise():
    root = load_data()
    block = request.args.get('block')
    if block is None or not block.isdigit():
        return render_template('blockwise.html', result="Invalid block number")
    block = int(block)
    if block == 1:
        result = root.left_list.traverse()
    elif block == 2:
        result = root.right_list.traverse()
    else:
        result = "Block number does not exist"
    return render_template('blockwise.html', result=result)

# Route for apartment details
@app.route('/details', methods=['GET', 'POST'])
def details():
    root = load_data()
    if request.method == 'POST':
        block = request.form.get('block')
        house = request.form.get('house')
        if block is None or not block.isdigit() or house is None or not house.isdigit():
            return render_template('details.html', result="Invalid block or house number")
        block = int(block)
        house = int(house)
        if block == 1:
            if 1 <= house <= 5:
                apartments = root.left_list.traverse()
                res = [line for line in apartments if line[1] == str(house)]
            else:
                res = "House does not exist"
        elif block == 2:
            if 1 <= house <= 5:
                apartments = root.right_list.traverse()
                res = [line for line in apartments if line[1] == str(house)]
            else:
                res = "House does not exist"
        else:
            res = "Block does not exist"
        return render_template('details.html', result=res)
    return render_template('details.html', result=None)

# Route for checking availability
'''
@app.route('/availability', methods=['GET', 'POST'])
def availability():
    root = load_data()
    if request.method == 'POST':
        bhk = request.form.get('bhk')
        if bhk is None or not bhk.isdigit():
            return render_template('availability.html', result="Invalid BHK value")
        bhk = int(bhk)
        res = []
        for block in [1, 2]:
            apartments = root.left_list.traverse() if block == 1 else root.right_list.traverse()
            for apartment in apartments:
                if apartment[2] == str(bhk) and apartment[3] == 'vacant':
                    res.append(apartment)
        if not res:
            res = "No vacant houses found for the given BHK value"
        return render_template('availability.html', result=res)
    return render_template('availability.html', result=None)
    '''
@app.route('/availability', methods=['GET', 'POST'])
def availability():
    if request.method == 'POST':
        bhk = request.form.get('bhk')
        if bhk and bhk.isdigit():
            bhk = int(bhk)
            res = house_availability(bhk)
            return render_template('availability.html', result=res)
    return render_template('availability.html')

def house_availability(bhk):
    root=load_data()
    res=[]
    for block in [1,2]:
        apartments = root.left_list.traverse() if block==1 else root.right_list.traverse()
        for apartment in apartments:
            if apartment[2]==str(bhk) and apartment[3]=='vacant':
                res.append(apartment)
    if len(res)>0:
        return res
    else:
        return "No vacant houses found for the given BHK value"


# Route for maintenance details
@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    root = load_data()
    if request.method == 'POST':
        block = request.form.get('block')
        house = request.form.get('house')
        if block and block.isdigit() and house and house.isdigit():
            block = int(block)
            house = int(house)
            if block == 1:
                apartments = root.left_list.traverse()
            elif block == 2:
                apartments = root.right_list.traverse()
            else:
                return render_template('maintenance.html', result="Block does not exist")
            
            res = [line for line in apartments if line[1] == str(house)]
            if not res:
                result = "Block number or house number does not exist"
            else:
                result = [[line[0], line[1], line[6]] for line in res]
            return render_template('maintenance.html', result=result)
    return render_template('maintenance.html')


'''
@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    root = load_data()
    if request.method == 'POST':
        block = request.form.get('block')
        house = request.form.get('house')
        if block is None or not block.isdigit() or house is None or not house.isdigit():
            return render_template('maintenance.html', result="Invalid block or house number")
        block = int(block)
        house = int(house)
        if block == 1:
            apartments = root.left_list.traverse()
        elif block == 2:
            apartments = root.right_list.traverse()
        else:
            return render_template('maintenance.html', result="Block does not exist")
        
        res = [line for line in apartments if line[1] == str(house)]
        if not res:
            res = "Block number or house number does not exist"
        else:
            res = [[line[0], line[1], line[6]] for line in res]
        return render_template('maintenance.html', result=res)
    return render_template('maintenance.html', result=None)
    '''

# Route for updating occupancy status

@app.route('/updation', methods=['GET', 'POST'])
def updation(block,house,occ):
    if request.method == 'POST':
        block = request.form.get('block')
        house = request.form.get('house')
        occ = request.form.get('occ')
        if block is None or not block.isdigit() or house is None or not house.isdigit() or occ is None:
            return render_template('updation.html', result="Invalid input")
        block = int(block)
        house = int(house)
        l = []
        flag = False
        csv_path = os.path.join('data', 'apartment.csv')
        with open(csv_path, "r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for i in csv_reader:
                l.append(i)
        for j in l:
            if j[0] == str(block) and j[1] == str(house):
                j[3] = str(occ)
                flag = True
                break
        with open(csv_path, "w+", newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(header)
            for i in range(len(l)):
                csv_writer.writerow(l[i])

        res = "Updation successful" if flag else "Updation unsuccessful"
        return render_template('updation.html', result=res)
    return render_template('updation.html', result=None)


# Route for index page
'''
# Route for updating occupancy status (POST method)
@app.route('/update', methods=['POST'])
def update(block,house,occ):
    block = request.form['block']
    house = request.form['house']
    occ = request.form['occ']
    message = updation(block, house, occ)
    flash(message)
    return redirect(url_for('index'))'''


'''  
# Route for index page
@app.route('/')
def index():
    return render_template('updation.html')

# Route for updating occupancy status (POST method)
@app.route('/update', methods=['POST'])
def update():
    return redirect(url_for('updation'))'''

if __name__ == '__main__':
    app.run(debug=True)
