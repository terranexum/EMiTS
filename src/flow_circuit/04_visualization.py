import gds2webgl

# Load the GDSII file
gds = gds2webgl.GDSII("layout.gds")

# Generate the HTML page with WebGL visualization
html = gds.generate_html()

# Write the HTML to a file
with open("visualization.html", "w") as f:
    f.write(html)
