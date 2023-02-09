// visualize.js

fetch('/data')
    .then(response => response.json())
    .then(data => {
        visualize(data);
        //document.getElementById('graph-container').innerHTML = JSON.stringify(data);
    })
    .catch(error => console.error(error));

function visualize(data) {
  // code to render the visualization using the 3d-force-graph library
  console.log(data['nodes']);
  console.log(data['links']);
  
  // Create a 3D force graph using the nodes and edges data
  const graph = ForceGraph3D()
    (document.getElementById('graph-container'))
    .graphData(data);

  // Render the graph in the container
  graph.d3Force('charge').strength(-240);

  graph.nodeRelSize(1);
  graph.nodeResolution(20);

  graph.linkWidth(4);
  //graph.linkResolution(1);

}
