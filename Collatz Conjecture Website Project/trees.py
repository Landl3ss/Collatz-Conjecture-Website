import graphviz
from sql_data import TreeData

class Trees:
    def __init__(self):
        self.name = None


    # def color(self, dec):
    #     if dec > 16777215:
    #         dec -= 16777215
    #     h = hex(dec)[2:].upper()
    #     if len(h) < 6:
    #         c = '#' + ('0' * (6 - len(h))) + str(h)
    #     else:
    #         c = '#' + str(h)
    #     return c


    def whole_tree(self, highlighted_number, delete):
        # base = 1943797
        if delete:
            name = "delete"
        else:
            name = "whole_tree"
        dot = graphviz.Graph(filename=name, format='png')
        dot.attr('node', shape='circle', style='filled')
        dot.attr('graph', rankdir='TB')

        raw = TreeData().everything() # [0] is the number, [1] is the next number, [2] is the previous_even, [3] is the previous_odd

        dot.node(str(highlighted_number), fillcolor='#1DA8F5', color='black')
        dot.node('4')
        dot.node('2')
        dot.node('1')

        for i in range(len(raw) - 1, -1, -1):
            if str(raw[i][0]) != str(highlighted_number):
                dot.node(str(raw[i][0]))

        for i in raw:
            dot.edge(str(i[0]), str(i[1]))

        dot.edge('4', '2')
        dot.edge('2', '1')
        dot.edge('1', '4')

        dot.render(f'static/trees/{name}').replace('\\', '/')
        return name + '.png'


    def equal_tree(self, highlighted_number):
        name = 'delete'
        data = TreeData().equal_steps(highlighted_number)

        dot = graphviz.Graph(filename=name, format='png')
        dot.attr('node', shape='circle', style='filled')
        dot.attr('graph', rankdir='TB')

        for i in data:
            dot.node(str(i[0]))

        dot.node(str(highlighted_number), fillcolor='#1DA8F5', color='black')

        for i in data:
            dot.edge(str(i[0]), str(i[1]))

        dot.render(f'static/trees/{name}').replace('\\', '/')
        return name + '.png'


    def line_tree(self, highlighted_number):
        name = 'delete'
        data = TreeData().lines(highlighted_number)

        dot = graphviz.Graph(filename=name, format='png')
        dot.attr('node', shape='circle', style='filled')
        dot.attr('graph', rankdir='LR')

        dot.node(str(data[0]))

        for i in range(1, len(data)):
            dot.node(str(data[i]))
            dot.edge(str(data[i - 1]), str(data[i]))

        dot.render(f'static/trees/{name}').replace('\\', '/')
        return name + '.png'


    def steps(self, count):
        name = 'delete'
        data = TreeData().step_graph(count)

        dot = graphviz.Graph(filename=name, format='png')
        dot.attr('node', shape='circle', style='filled')
        dot.attr('graph', rankdir='TB')

        for i in data:
            dot.node(i)

        for x in data:
            dot.edge(x, data[x])

        dot.render(f'static/trees/{name}').replace('\\', '/')

        return name + '.png'