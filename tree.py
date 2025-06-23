class TreeNode:
    def __init__(self, attribute=None, label=None):
        """
        Node of the decision tree.
        :param attribute: Symptom to split on (None for leaf).
        :param label: Disease label if leaf node.
        """
        self.attribute = attribute
        self.label = label
        self.yes = None  # child if symptom present
        self.no = None   # child if symptom absent