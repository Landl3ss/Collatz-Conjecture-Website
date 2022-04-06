import sqlite3

# The database that holds all the numbers found.
'''
id                  (str)            id is the number in question
previous_even       (str)            the even number that brought to this number
previous_odd        (str)            the odd number that brought to this number
next                (str)            the next number that will be brought up
step_count          (int)            the number of steps going to the loop 1 being the base (hope to find a new loop)
loop_number         (int)            typically the loop will be 1 but if there is a new loop it will use the number that starts the loop again
'''
# db = sqlite3.connect('numbers.db')
# cur = db.cursor()

class AppAccess:

    def __init__(self):
        self.access = None


    def factor(self, num: int) -> list:
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()

        # even
        if num % 2 == 0:
            x = int(num / 2)
            cur.execute('UPDATE positive_numbers SET next=%s WHERE id=%s' % (str(x), str(num)))

            db.commit()
            db.close()
            return [x, True]
        # odd
        else:
            x = int((3 * num) + 1)
            cur.execute('UPDATE positive_numbers SET next=%s WHERE id=%s' % (str(x), str(num)))

            db.commit()
            db.close()
            return [x, False]


    def search(self, num: int) -> bool:
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()

        # Searching for the number in question
        try:
            exists = cur.execute('SELECT id FROM positive_numbers WHERE id=%s' % str(num)).fetchone()[0]
        except:

            db.close()
            return False

        db.close()
        return True


    def line(self, num):
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()

        points = [int(num)]

        # l[0] is next number, l[1] is loop_number
        l = cur.execute('SELECT next,loop_number FROM positive_numbers WHERE id=%s' % str(num)).fetchall()[0]
        next = l[0]
        loop = l[1]
        while int(next) != int(loop):
            points.append(int(next))
            next = int(cur.execute('SELECT next FROM positive_numbers WHERE id=%s' % str(next)).fetchall()[0][0])

        db.close()
        points.append(1)
        d = {int(num) : {'line' : points, 'count': len(points)}}
        return d


    def addin(self, num: int) -> int:
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()

        # num is current number
        x = factor(num)
        # next number
        n = x[0]

        # n is in the database already
        if search(n):
            if x[1]:
                cur.execute('UPDATE positive_numbers SET previous_even=%s WHERE id=%s' % (str(num), str(n)))
            else:
                cur.execute('UPDATE positive_numbers SET previous_odd=%s WHERE id=%s' % (str(num), str(n)))

            # s [0]step_count l [1]loop_number
            sl = cur.execute('SELECT step_count, loop_number FROM positive_numbers WHERE id=%s' % str(n)).fetchone()
            step = sl[0]
            loop = sl[1]
            step += 1
            previous = [None, None]
            while True:
                cur.execute('UPDATE positive_numbers SET step_count=%i, loop_number=%i WHERE id=%s' % (step, loop, str(num)))
                db.commit()

                pre = cur.execute('SELECT previous_even, previous_odd FROM positive_numbers WHERE id=%s' % str(num)).fetchone()

                if search(pre[0]):

                    e = cur.execute('SELECT step_count FROM positive_numbers WHERE id=%s' % pre[0]).fetchone()[0]
                    if not e:

                        num = pre[0]
                        step += 1

                elif search(pre[1]):

                    o = cur.execute('SELECT step_count FROM positive_numbers WHERE id=%s' % pre[1]).fetchone()[0]
                    if not o:

                        num = pre[1]
                        step += 1

                else:

                    db.close()
                    return 0

                if previous == [pre[0], pre[1]]:

                    db.close()
                    return 0

                previous = [pre[0], pre[1]]

        # n is not in the database already
        else:

            if x[1]:
                cur.execute('INSERT INTO positive_numbers (id, previous_even) VALUES (%s, %s)' % (str(n), str(num)))
            else:
                cur.execute('INSERT INTO positive_numbers (id, previous_odd) VALUES (%s, %s)' % (str(n), str(num)))

            db.commit()
            db.close()
            return n


    def missing_numbers(self):
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()
        seq = cur.execute('SELECT id FROM positive_numbers ORDER BY CAST(id AS Numeric(10,0))').fetchall()
        last = int(seq[-1][0])
        missing = []
        s = [int(seq[i][0]) for i in range(0, len(seq))]
        for j in range(1, last + 1):
            if j not in s:
                missing.append(j)

        db.close()
        return missing


    def found(self):
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()
        a = cur.execute('SELECT id FROM positive_numbers').fetchall()
        db.close()
        return (len(a))


    def everything(self) -> dict:
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()
        raw = cur.execute('SELECT id,next,step_count FROM positive_numbers WHERE id NOT IN ("1","2","4") ORDER BY CAST(id AS Numeric(10,0)) LIMIT 10').fetchall()
        data = {4: {'next' : 2, 'count' : 3}, 2: {'next' : 1, 'count' : 2}, 1: {'next' : None, 'count' : 1}}
        for i in range(len(raw)):
            c = True
            key = raw[i][0]
            next = raw[i][1]
            count = raw[i][2]
            while c:
                data[int(key)] = {'next' : int(next), 'count' : int(count)}
                key = next
                next = cur.execute('SELECT next FROM positive_numbers WHERE id=%s' % (str(key))).fetchone()[0]
                count -= 1
                if int(key) in data:
                    c = False

        db.close()
        return data


    def nod(self):
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()
        num = int(cur.execute('SELECT id FROM positive_numbers WHERE previous_even IS NULL AND previous_odd IS NULL ORDER BY CAST(id AS Numeric(10,0)) DESC').fetchone()[0])
        while True:
            num += 1
            if not self.search(num):
                num -= 1
                ncl = cur.execute('SELECT step_count,next,loop_number FROM positive_numbers WHERE id=%s' % (str(num))).fetchall()[0]
                db.close()
                return [num, ncl[0], ncl[1], ncl[2]]


    def branches(self):
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()

        raw = cur.execute('SELECT id FROM positive_numbers WHERE previous_even NOT NULL AND previous_odd NOT NULL AND NOT id="4" ORDER BY step_count DESC').fetchall()
        splits = []
        for i in range(len(raw)):
            splits.append(int(raw[i][0]))

        db.close()
        return splits


    def traceback(self):
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()
        splits = self.branches()

        def back(entry, lines):
            db = sqlite3.connect('numbers.db')
            cur = db.cursor()

            lines.append(int(entry))
            x = cur.execute('SELECT previous_even, previous_odd FROM positive_numbers WHERE id=%s' % (str(entry))).fetchall()[0]
            if (x[0] == None and x[1] == None) or (x[0] != None and x[1] != None):
                return
            elif x[0] != None:
                back(x[0], lines)
            else:
                back(x[1], lines)

            db.close()
            return

        lines = {}
        for i in splits:
            eo = cur.execute('SELECT previous_even, previous_odd FROM positive_numbers WHERE id=%s' % (str(i))).fetchall()[0]
            lines[i] = {'even' : [], 'odd' : []}
            back(eo[0], lines[i]['even'])
            back(eo[1], lines[i]['odd'])

        re = []
        for i in lines:
            temp = []
            for even in range(len(lines[i]['even']) - 1, -1 , -1):
                temp.append(lines[i]['even'][even])
            temp.append(i)
            if len(temp) > 1:
                re.append(temp)
            temp = []
            for odd in range(len(lines[i]['odd']) - 1, -1 , -1):
                temp.append(lines[i]['odd'][odd])
            temp.append(i)
            if len(temp) > 1:
                re.append(temp)

        graph_lines = []
        for i in range(len(re)):
            temp = []
            for j in re[i]:
                temp.append(j)
            while True:
                next_unit = temp[-1]
                i += 1
                if i >= len(re):
                    temp.append(8)
                    temp.append(4)
                    temp.append(2)
                    temp.append(1)
                    graph_lines.append(temp)
                    break
                if re[i][0] == next_unit:
                    for j in range(1, len(re[i])):
                        temp.append(re[i][j])

        l = {}
        for i in graph_lines:
            t = cur.execute('SELECT previous_even, previous_odd FROM positive_numbers WHERE id=%s' % i[0]).fetchall()
            if t[0] == (None, None):
                l[i[0]] = {'line': i, 'count': len(i)}

        db.close()
        return l

    def largest(self):
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()

        large = cur.execute('SELECT id FROM positive_numbers ORDER BY CAST(id AS Numeric(10,0)) DESC').fetchone()[0]
        step = cur.execute('SELECT step_count FROM positive_numbers ORDER BY step_count DESC').fetchone()[0]

        db.close()
        return [large, step]


    def deets(self, num):
        d = self.line(num)
        p = d[int(num)]['line']
        c = d[int(num)]['count']
        l = p[-1]

        db = sqlite3.connect('numbers.db')
        cur = db.cursor()
        pre = cur.execute('SELECT previous_even, previous_odd FROM positive_numbers WHERE id=%s' % (str(num))).fetchall()[0]
        same = cur.execute('SELECT id FROM positive_numbers WHERE step_count=%i AND NOT id=%s' % (int(c), str(num))).fetchall()

        s = []
        for i in same:
            s.append(int(i[0]))

        print(s)
        details = {
            'number': num,
            'count': c,
            'steps': p,
            'loop': l,
            'previous_even': pre[0],
            'previous_odd': pre[1],
            'same_count': s
                }

        db.close()
        return details


    def max_step_count(self):
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()

        data = cur.execute('SELECT step_count FROM positive_numbers ORDER BY step_count DESC').fetchone()[0]

        db.close()
        return data

# db.close()

# for number in range(51, 101):
#     db = sqlite3.connect('numbers.db')
#     cur = db.cursor()
#     data1 = cur.execute('SELECT id FROM positive_numbers WHERE id').fetchall()
#     data = []
#     for i in data1:
#         data.append(int(i[0]))

#     if number not in data:
#         print(f'{number} not in the data base')
#         cur.execute('INSERT INTO positive_numbers (id) VALUES (%s)' % (str(number)))

#         db.commit()
#         db.close()

#         n = number
#         while n != 0:
#             n = addin(n)



class TreeData:

    def __init__(self):
        self.name = None


    def equal_steps(self, num):
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()

        s = cur.execute('SELECT step_count FROM positive_numbers WHERE id=%s' % str(num)).fetchall()[0]
        idnext = cur.execute('SELECT id,next FROM positive_numbers WHERE step_count=%i' % int(s[0])).fetchall()

        steps = s[0]
        data = []
        for i in idnext:
            data.append(i)

        while steps > 3:
            steps -= 1
            idnext = cur.execute('SELECT id,next FROM positive_numbers WHERE step_count=%i' % int(steps)).fetchall()

            for i in idnext:
                data.append(i)

        db.close()

        return data


    def lines(self, num):
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()

        n = cur.execute('SELECT id,next FROM positive_numbers WHERE id=%s' % str(num)).fetchall()

        data = [n[0][0]]

        now = n[0][1]
        while now != '4':
            data.append(now)
            now = cur.execute('SELECT next FROM positive_numbers WHERE id=%s' % str(now)).fetchall()[0][0]

        db.close()

        data.append('4')
        data.append('2')
        data.append('1')

        return data


    def everything(self):
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()

        data = cur.execute('SELECT id,next,previous_even,previous_odd FROM positive_numbers WHERE id NOT IN ("4","2","1")').fetchall()

        db.close()
        return data


    def step_graph(self, count):
        db = sqlite3.connect('numbers.db')
        cur = db.cursor()

        data = {'8': '4', '4': '2', '2': '1', '1': '4'}
        c = int(count)

        while c > 4:
            raw = cur.execute('SELECT id,next FROM positive_numbers WHERE step_count=%i' % c).fetchall()
            for i in range(len(raw)):
                    data[raw[i][0]] = raw[i][1]
            c -= 1

        db.close()

        return data
