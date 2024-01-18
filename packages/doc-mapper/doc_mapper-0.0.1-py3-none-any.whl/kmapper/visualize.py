
from IPython.display import Javascript, HTML
import json

def convert_to_json(dendro:dict):
    def add_node(node):
        if isinstance(node, int):
            return {"name": str(node)}
        else:
            return {
                "name": "",
                "children": [add_node(child) for child in node]
            }
    return add_node(dendro)

def visualize(tree_data):
    # HTMLとJavaScriptコード
    html_script = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        /* スタイル定義（必要に応じてカスタマイズ） */
        .node circle {{
            fill: #fff;
            stroke: steelblue;
            stroke-width: 3px;
        }}
        .node text {{ font: 12px sans-serif; }}
        .link {{
            fill: none;
            stroke: #ccc;
            stroke-width: 2px;
        }}
    </style>
    </head>
    <body>
        <div id="tree-container"></div>
        <script src="https://d3js.org/d3.v5.min.js"></script>
        <script>
            var treeData = {json.dumps(tree_data)};

            var margin = {{top: 40, right: 120, bottom: 20, left: 120}},
                width = 960 - margin.right - margin.left,
                height = 800 - margin.top - margin.bottom;

            var treemap = d3.tree().size([height, width]);
            var nodes = d3.hierarchy(treeData, function(d) {{ return d.children; }});
            nodes = treemap(nodes);

            var svg = d3.select("#tree-container").append("svg")
                .attr("width", width + margin.right + margin.left)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            var g = svg.selectAll(".node")
                .data(nodes.descendants())
                .enter().append("g")
                .attr("class", function(d) {{
                    return "node" + (d.children ? " node--internal" : " node--leaf"); }})
                .attr("transform", function(d) {{
                    return "translate(" + d.y + "," + d.x + ")"; }});

            g.append("circle")
                .attr("r", 10);

            g.append("text")
                .attr("dy", ".35em")
                .attr("x", function(d) {{
                    return d.children ? -13 : 13; }})
                .style("text-anchor", function(d) {{
                    return d.children ? "end" : "start"; }})
                .text(function(d) {{ return d.data.name; }});

            svg.selectAll(".link")
                .data(nodes.descendants().slice(1))
                .enter().append("path")
                .attr("class", "link")
                .attr("d", function(d) {{
                    return "M" + d.y + "," + d.x
                        + "C" + (d.y + d.parent.y) / 2 + "," + d.x
                        + " " + (d.y + d.parent.y) / 2 + "," + d.parent.x
                        + " " + d.parent.y + "," + d.parent.x;
                }});
        </script>
    </body>
    </html>
    """

    # HTMLとJavaScriptをJupyterノートブックで表示
    return display(HTML(html_script))
