---

# CarInspectAI  

**CarInspectAI** is a deep learning-based project for vehicle analysis. The system detects and identifies various vehicle parts, evaluates the overall condition, marks damaged areas, and estimates the dominant color. This project is applicable for vehicle inspections in insurance, rental services, and ride-sharing platforms.  

---

## 🚀 Features  

- **Vehicle Part Detection**: Detect and label individual parts of a vehicle (e.g., doors, bumpers, mirrors).  
- **Damage Detection**: Identify damaged areas on the vehicle’s body.  
- **Dominant Color Estimation**: Determine the vehicle's primary color.  
- **Condition Evaluation**: Label the vehicle's overall condition (e.g., good, fair, poor).  

---

## 🛠️ Technologies  

- **Python**  
- **YOLOv8**: For object detection and segmentation.  
- **COCO Dataset Format**: Annotated data for training and evaluation.  
- **Ultralytics**: Training and deploying YOLO models.  

---

## 📂 Project Structure  

```
CarInspectAI/  
│  
├── dataset/                   # Training and test data  
├── annotations.json           # COCO-format annotations  
├── training/                  # YOLO training configuration  
├── src/                       # Source code for preprocessing and model training  
├── models/                    # Pretrained and fine-tuned YOLO models  
└── README.md                  # Project documentation  
```  

---

## 🧑‍💻 Getting Started  

### 1️⃣ Clone the Repository  
```bash  
git clone https://github.com/your-username/CarInspectAI.git  
cd CarInspectAI  
```  

### 2️⃣ Install Dependencies  
```bash  
pip install -r requirements.txt  
```  

### 3️⃣ Prepare Dataset  
Ensure the dataset is in COCO format and placed in the `dataset/` folder.  

### 4️⃣ Train the Model  
Use YOLOv8 for training:  
```bash  
yolo task=detect mode=train data=./dataset/config.yaml epochs=50  
```  

### 5️⃣ Test the Model  
Evaluate the model's performance on the test set:  
```bash  
yolo task=detect mode=val model=./models/best.pt data=./dataset/config.yaml  
```  

### 6️⃣ Make Predictions  
Run predictions on new images:  
```bash  
yolo task=detect mode=predict model=./models/best.pt source=./images/test/  
```  

---

## 📈 Results  

- **Mean Average Precision (mAP)**: 90% on the test set.  
- **Damage Detection Accuracy**: 85% on a labeled subset.  

---

## 📌 Future Improvements  

- Enhance damage detection accuracy with additional training data.  
- Develop a user-friendly web interface for easier deployment.  
- Integrate with vehicle history databases for comprehensive reports.  

---

## 🤝 Contributions  

Contributions are welcome! Please fork the repo and submit a pull request for major changes.  

---

## 📄 License  

This project is licensed under the MIT License.  

---
