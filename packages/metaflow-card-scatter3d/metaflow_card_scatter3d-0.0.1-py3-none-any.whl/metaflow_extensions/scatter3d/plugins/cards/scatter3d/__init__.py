import os
import json
import traceback

from metaflow.cards import MetaflowCard


ABS_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ABS_DIR_PATH, "base.html")
ASSET_PATH = os.path.join(ABS_DIR_PATH, "assets")


class Scatter3DCard(MetaflowCard):
    ALLOW_USER_COMPONENTS = True
    RUNTIME_UPDATABLE = True

    type = "scatter3d"

    def _html(self, config):
        # this function produces a html card by injecting data directly
        # in the html, so it doesn't need to be loaded externally.
        # Runtime data updates may override the data provided here.
        cfg = {}
        for key, val in config.items():
            cfg[f"config-{key}"] = json.dumps(val) if type(val) != str else val

        with open(TEMPLATE_PATH) as f:
            # besides data, we inject javascript dependencies in the html,
            # so it becomes a single self-contained file with no external
            # dependencies
            for asset in os.listdir(ASSET_PATH):
                fname, _ = asset.split(".")
                with open(os.path.join(ASSET_PATH, asset)) as a:
                    cfg[f"asset-{fname}"] = a.read()

            # use mustache / chevron template engine, which is bundled in Metaflow
            chevron = self._get_mustache()
            return chevron.render(f, cfg)

    def _check_data(self, data):
        title = data.get("title", "scatter3d")
        points = data.get("points", [[0, 0, 0]])
        classes = data.get("classes", [0])
        labels = data.get("labels", [""])
        colors = data.get("colors", ["#ffffff"])
        if len(points[0]) not in (2, 3):
            raise Exception("points must be a list of 2 or 3d lists")
        if any(len(p) != len(points[0]) for p in points):
            raise Exception("All points must have the same dimensionality")
        if len(classes) != len(points):
            raise Exception(
                "The length of the classes array must match the length of the points array"
            )
        if max(classes) >= len(colors):
            raise Exception(
                "The colors array needs to set a color for each class index"
            )
        if max(classes) >= len(labels):
            raise Exception(
                "The labels array needs to set a labels for each class index"
            )
        return {
            "title": title,
            "points": points,
            "classes": classes,
            "labels": labels,
            "colors": colors,
        }

    def _response(self, data):
        try:
            config = self._check_data(data)
        except:
            return (
                "<html><body><h1>Scatterplot failed</h1><br>"
                "<pre><code>%s</code></pre>" % traceback.format_exc()
            )
        else:
            return self._html(config)

    def render(self, task):
        # this method produces the final HTML card
        return self._response(self.runtime_data.get("user", {}))

    def render_runtime(self, task, data):
        # this method produces an intermediate HTML card,
        # which in this case is equal to the final one, just
        # with different data that's provided in the refresh()
        # call
        return self._response(data.get("user", {}))

    def refresh(self, task, data):
        # this method produces a data json (not html), which will
        # take care of runtime updates to the card
        try:
            return self._check_data(data.get("user", {}))
        except:
            # ignore invalid runtime data silently
            # we will get a proper error message in the end
            # once render() gets called
            pass


CARDS = [Scatter3DCard]
