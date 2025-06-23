from pywebio.input import actions
from pywebio.output import put_markdown, put_text, put_loading, clear, style
from time import sleep
from loader import load_and_prepare
from id3 import build_tree


class DiseasePredictorApp:
    def __init__(self, dataset_file='Training.csv'):
        self.dataset_file = dataset_file
        self.root = None
        self.symptoms = []

    def run(self):
        put_markdown("# Disease Predictor from Symptoms")
        put_text("Predict possible disease using ID3 decision tree.")
        put_markdown("---")
        try:
            df_long, self.symptoms = load_and_prepare(self.dataset_file)
        except FileNotFoundError as err:
            clear()
            put_markdown("## Error: Dataset Not Found")
            style(put_text(str(err)), 'color:red')
            return
        with put_loading():
            sleep(1)
        clear()
        used = {s: False for s in self.symptoms}
        self.root = build_tree(df_long, self.symptoms, used)
        self._traverse(self.root)

    def _traverse(self, node):
        while node.attribute:
            clear()
            put_markdown(f"# Do you have symptom: *{node.attribute}*?")
            ans = actions(buttons=['Yes', 'No'])
            node = node.yes if ans == 'Yes' else node.no
        clear()
        put_markdown("# Prediction Result")
        if node.label:
            put_markdown(f"## Predicted Disease: *{node.label}*")
        else:
            put_markdown("### Could not determine disease.")
        put_text("Consult a professional for accurate diagnosis.")