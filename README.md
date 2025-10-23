# QGIS Elevation Profile Plotter Plugin

The **Elevation Profile Plotter** is a QGIS plugin that allows users to generate 2D elevation profiles along user-defined paths. By extracting elevation data from a Digital Elevation Model (DEM), the plugin provides a clear visualization of terrain variation and key metrics such as maximum, minimum, and mean elevation.

![Screenshot 2022-07-01 232525](https://github.com/user-attachments/assets/9d54fdfb-63fc-4bb9-a67f-b64c22a0ad13)

---

## ⚙️ Features

- **DEM Data Extraction**: Reads elevation values from a loaded Digital Elevation Model (DEM) raster layer.
- **2D Elevation Profile**: Plots a cross-sectional view of terrain elevation along a defined path.
- **Key Metrics Visualization**: Automatically calculates and displays maximum, minimum, and mean elevations along the profile.
- **Graphical Output**: Uses Matplotlib (`pyplot`) for generating clear and customizable elevation plots.

---

## 🚀 Workflow

The plugin automates the elevation profiling process using QGIS processing tools:

1. **Input**: User provides a DEM raster layer, a point vector layer (defining the path), and a sample interval in meters.
2. **Path Creation**: The `qgis:pointstopath` tool generates a line feature from the input points.
3. **Point Generation**: `native:pointsalonglines` creates evenly spaced sample points along the line.
4. **Elevation Sampling**: `saga:addrastervaluestopoints` collects Z-values (elevation) from the DEM at the generated points.
5. **Plotting**: Collected elevations and distances are plotted as an elevation profile using Matplotlib.

---

## 🛠️ Requirements & Development

- **GIS Software**: QGIS (Quantum GIS)
- **Scripting Language**: Python
- **GUI Development**: Qt Designer (`.ui` files)
- **Plugin Tools**: QGIS Plugin Builder

### Core Libraries

- `qgis.core` – GIS calculations and data handling  
- `PyQt` – GUI management  
- `matplotlib.pyplot` – Elevation profile plotting  

---

## 📝 Usage

1. Install the plugin in QGIS via the **Plugin Manager** or manually place the plugin folder in the QGIS plugins directory.
2. Open the plugin dialog from the QGIS interface.
3. Select the **DEM raster layer** to extract elevation data.
4. Select the **Point Layer** defining the profile path (ensure points are ordered correctly).
5. Enter the **sample interval** (in meters) between points.
6. Click **OK** to generate and display the elevation profile.

---

This plugin streamlines terrain analysis in QGIS, providing a simple yet powerful tool for visualizing elevation changes along any path.
