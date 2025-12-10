# **Automated Construction Site Layout Generator**  

This project was developed in collaboration with Daniel Tavares dos Anjos (https://github.com/danieltanjos) for the *Computational Tools for Civil Engineering* course at the **Federal University of Santa Catarina (UFSC), Brazil**.  

The goal is to automate the generation of construction site layouts, ensuring compliance with **NR18 safety regulations** and optimizing the spatial arrangement of essential site elements such as storage, restrooms, and dining areas.  

## **Project Overview**  

This Python-based application generates optimized construction site layouts using a **genetic algorithm**. It takes into account:  
- Site dimensions (width and height)  
- Number of workers  
- Safety standards (NR18)  
- Essential site elements (storage, restrooms, dining areas)  

The final layout is exported as a **DXF file**, which can be opened and edited in CAD software such as AutoCAD or LibreCAD.  

## **Main Features**  

### **Graphical User Interface (customtkinter)**  
- Simple interface for entering project parameters  
- Selection of required site elements  
- Directory selection for saving the generated DXF file  

### **Optimized Layout via Genetic Algorithm**  
- Uses an evolutionary approach to find the best spatial arrangement  
- Prevents overlapping blocks and ensures logical placement  

### **DXF File Generation**  
- Automatically generates a DXF file with the final layout  
- Ensures CAD compatibility for further adjustments  

---

## **Project Structure**  

```
📁 automated-construction-site  
│── 📄 gui.py       # Graphical User Interface (Tkinter-based)  
│── 📄 regiao.py    # Genetic Algorithm & Site Layout Logic  
│── 📄 cad.py       # DXF File Generation (ezdxf Library)  
│── 📄 main.py      # Main script to run the application  
```

---

## **How to Run the Project**  

### **1. Install Dependencies**  
Make sure you have **Python 3.12.4** installed, then run:  
```bash
pip install ezdxf customtkinter
```

### **2. Clone the Repository & Navigate to Folder**  
```bash
git clone https://github.com/danieltanjos/automated-construction-site.git  
cd automated-construction-site  
```

### **3. Run the Application**  
```bash
python main.py
```

### **4. Use the Interface**  
1. Fill in the required fields (site dimensions, workers, etc.)  
2. Select the elements to include (storage, restrooms, etc.)  
3. Choose a directory for saving the DXF file  
4. Click "Execute" to generate the layout  

---

## **Example Usage**  

### **Input Parameters:**  
- **Project Name:** Example Project  
- **Site Dimensions:** 100m x 50m  
- **Number of Workers:** 30  
- **Selected Blocks:** Storage, Restrooms, Dining Area  

### **Generated Output:**  
A **DXF file** containing the optimized construction site layout is saved in the selected directory.  

---

## **Future Improvements**  

- Refine the genetic algorithm for better optimization  
- Add more block types, such as offices and resting areas  
- Fix potential layout bugs, including block overlap and zero-score generations  
- Improve DXF output by adjusting scale and layout for better visualization  
- Convert the project into a standalone executable (.exe)  

---

## Author
João Vitor Ferreira Pedro
Engineering Student at UFSC
GitHub: https://github.com/jvfpedro

Daniel Tavares dos Anjos
Engineering Student at UFSC
GitHub: https://github.com/danieltanjos

---

**Federal University of Santa Catarina (UFSC)**  
**Civil Engineering - CTC**  
**Course: Computational Tools for Civil Engineering**  
