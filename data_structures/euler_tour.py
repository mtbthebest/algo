class EulerTour(object):

    def __init__(self, tree):
        self.tree = tree

    def execute(self):
        if not self.tree.is_empty():
            self.tour(self.tree.get_root(), 0, [])

    def tour(self, node, depth, path):
        self.hook_previsit(node, depth, path)
        results = []
        path.append(0)

        for c in self.tree.children(node):
            results.append(self.tour(c, depth + 1, path))
            path[-1] += 1
        path.pop()

        return self.hook_postvisit(node, depth, path, results)

    def hook_previsit(self, node, depth, path):
        pass

    def hook_postvisit(self, node, depth, path, results):
        pass


class BinaryEulerTour(EulerTour):

    def tour(self, node, depth, path):
        results = [None, None]
        self.hook_previsit(node, depth, path)
        if (left := self.tree.get_left(node)) is not None:
            path.append(0)
            results[0] = self.tour(left, depth + 1, path)
            path.pop()
        self.hook_invisit(path, depth, path)

        if (right := self.tree.get_right(node)) is not None:
            path.append(1)
            results[1] = self.tour(right, depth + 1, path)
            path.pop()

        return self.hook_postvisit(node, depth, path, results)

    def hook_invisit(self, node, depth, path):
        pass