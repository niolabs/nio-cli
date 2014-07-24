
class Execution(object):
    def __init__(self, execution):
        self.edges = {
            e['name']: e['receivers'] for e in execution
        }
        
    def add_edge(self, frm, to):
        frm_curr = self.edges.get(frm, [])
        if to not in frm_curr and to is not None:
            frm_curr.append(to)
        self.edges[frm] = frm_curr
            
    def rm_edge(self, frm, to):
        frm_curr = self.edges.get(frm, [])
        frm_curr = [t for t in frm_curr if t != to]
        self.edges[frm] = frm_curr

    def pack(self):
        return [{
            'name': e, 'receivers': self.edges[e]
        } for e in self.edges]

    def to_rows(self):
        header = ['Output Block']
        align = []
        rows = [align, header]
        for frm in self.edges:
            rows.append([frm] + self.edges[frm])

        max_len = max([len(r) for r in rows])
        rows[1] += list(range(max_len-1))
        rows[1:] = [r + [''] * (max_len - len(r)) for r in rows[1:]]
        return rows

