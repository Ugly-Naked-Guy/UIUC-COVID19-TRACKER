import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set()

def draw_barchar(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT  department,COUNT(*) FROM user natural JOIN reported WHERE reported.testResult = 'positive' GROUP BY user.department ")
    # cur.execute("SELECT  department,COUNT(*) FROM user natural join  GROUP BY department ")
    data = cur.fetchall()
    cur.close()
    sns.set()
    print(data)
    fig = plt.figure()
    # ax = fig.add_axes([0,0,1,1])
    langs = list(zip(*data))[0]
    students = list(zip(*data))[1]
    plt.bar(langs, students)
    # plt.xlabel("Energy Source")
    plt.ylabel("Confirmed Cases")
    # plt.title("Energy output from various fuel sources")
    plt.xticks(rotation=20)

    abspath = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(abspath + "/static/books_read.jpg")
    # plt.show()


def draw_barchar_address(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT  address,COUNT(*) FROM user natural JOIN reported WHERE reported.testResult = 'positive' GROUP BY address  ")
    data = cur.fetchall()
    cur.close()
    sns.set()
    print(data)
    fig = plt.figure()
    # ax = fig.add_axes([0,0,1,1])
    langs = list(zip(*data))[0]
    students = list(zip(*data))[1]
    plt.bar(langs, students)
    # plt.xlabel("Energy Source")
    plt.ylabel("Reported Cases")
    # plt.title("Energy output from various fuel sources")
    plt.xticks(rotation=20)

    abspath = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(abspath + "/static/bar_address.jpg")
    # plt.show()


def pie_char(mysql):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    cur = mysql.connection.cursor()
    cur.execute("SELECT  department,COUNT(*) FROM user natural JOIN reported WHERE reported.testResult = 'positive' GROUP BY user.department ")
    data = cur.fetchall()

    labels = list(zip(*data))[0]
    sizes = list(zip(*data))[1]
    plt.figure()

    plt.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    abspath = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(abspath + "/static/pie_char.jpg")
    # plt.show()


def user_draw_barchar(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT  department,COUNT(*) FROM user GROUP BY department ")
    data = cur.fetchall()
    cur.close()
    sns.set()
    print(data)
    fig = plt.figure()
    # ax = fig.add_axes([0,0,1,1])
    langs = list(zip(*data))[0]
    students = list(zip(*data))[1]
    plt.bar(langs, students)
    # plt.xlabel("Energy Source")
    plt.ylabel("Confirmed Cases")
    # plt.title("Energy output from various fuel sources")
    plt.xticks(rotation=20)

    abspath = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(abspath + "/static/books_read.jpg")
    # plt.show()


def user_draw_barchar_address(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT  address,COUNT(*) FROM user GROUP BY address ")
    data = cur.fetchall()
    cur.close()
    sns.set()
    print(data)
    fig = plt.figure()
    # ax = fig.add_axes([0,0,1,1])
    langs = list(zip(*data))[0]
    
    students = list(zip(*data))[1]
    plt.bar(langs, students)
    # plt.xlabel("Energy Source")
    plt.ylabel("Number")
    # plt.title("Energy output from various fuel sources")
    plt.xticks(rotation=20)

    abspath = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(abspath + "/static/bar_address.jpg")
    # plt.show()


def user_pie_char(mysql):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    cur = mysql.connection.cursor()
    cur.execute("SELECT  department,COUNT(*) FROM user GROUP BY department ")
    data = cur.fetchall()

    labels = list(zip(*data))[0]
    sizes = list(zip(*data))[1]
    plt.figure()

    plt.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    abspath = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(abspath + "/static/pie_char.jpg")
    # plt.show()

