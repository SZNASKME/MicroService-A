# Data Analytics Microservice - คู่มือการใช้งาน

## ภาพรวม

ฉันได้สร้าง **Data Analytics Microservice** ที่ครอบคลุมและแยกตาม feature ต่างๆ สำหรับการวิเคราะห์ข้อมูลดังนี้:

## 📁 โครงสร้างไฟล์

```
MicroService-A/
├── app.py                          # ไฟล์หลักของ microservice
├── config.py                       # การตั้งค่าต่างๆ
├── requirements.txt                # Python dependencies
├── README.md                       # เอกสารประกอบ
├── package.json                    # ข้อมูล metadata ของโปรเจค
├── Dockerfile                      # สำหรับ containerization
├── docker-compose.yml              # สำหรับ deployment stack
├── setup.bat/.sh                   # สคริปต์ติดตั้ง
├── test_api.py                     # ทดสอบ API แบบครบถ้วน
├── simple_test.py                  # ทดสอบ API แบบง่าย
├── auto_label_microservice.py      # ไฟล์เดิม (สำหรับอ้างอิง)
└── features/                       # โฟลเดอร์ features หลัก
    ├── __init__.py
    ├── data_processor.py           # 📊 ประมวลผลข้อมูล
    ├── statistical_analyzer.py     # 📈 วิเคราะห์เชิงสถิติ
    ├── visualization_service.py    # 📋 การแสดงผลและกราฟ
    ├── ml_predictor.py             # 🤖 Machine Learning
    ├── data_validator.py           # ✅ ตรวจสอบคุณภาพข้อมูล
    └── report_generator.py         # 📄 สร้างรายงาน
```

## 🚀 Features หลัก

### 1. **Data Processing** (`data_processor.py`)
- **อัปโหลดไฟล์**: รองรับ CSV, JSON, Excel
- **ทำความสะอาดข้อมูล**: จัดการ missing values, duplicates
- **ตรวจสอบข้อมูล**: ให้ข้อมูลเบื้องต้นเกี่ยวกับ dataset

### 2. **Statistical Analysis** (`statistical_analyzer.py`)
- **Descriptive Statistics**: mean, median, std, skewness, kurtosis
- **Correlation Analysis**: Pearson, Spearman correlations
- **Hypothesis Testing**: t-test, chi-square, ANOVA
- **Outlier Detection**: IQR, Z-score methods

### 3. **Visualization Service** (`visualization_service.py`)
- **Chart Generation**: line, bar, scatter, pie, heatmap
- **Interactive Dashboards**: multiple charts in one view
- **Export Options**: PNG, PDF, SVG formats

### 4. **Machine Learning** (`ml_predictor.py`)
- **Model Training**: Random Forest, Logistic Regression, SVM
- **Predictions**: classification และ regression
- **Model Evaluation**: accuracy, cross-validation scores
- **Feature Importance**: การวิเคราะห์ความสำคัญของตัวแปร

### 5. **Data Validation** (`data_validator.py`)
- **Quality Assessment**: completeness, accuracy, consistency
- **Schema Validation**: ตรวจสอบโครงสร้างข้อมูล
- **Anomaly Detection**: ตรวจจับค่าผิดปกติ
- **Business Rules**: ตรวจสอบกฎทางธุรกิจ

### 6. **Report Generation** (`report_generator.py`)
- **Comprehensive Reports**: รายงานแบบครอบคลุม
- **Multiple Formats**: PDF, HTML, DOCX, JSON
- **Scheduled Reports**: รายงานอัตโนมัติตามกำหนดเวลา
- **Custom Templates**: เทมเพลตรายงานที่ปรับแต่งได้

## 🔗 API Endpoints

### ✅ System Health
```
GET /health - ตรวจสอบสถานะระบบ
```

### 📊 Data Processing
```
POST /api/v1/data/upload - อัปโหลดข้อมูล
POST /api/v1/data/clean - ทำความสะอาดข้อมูล
```

### 📈 Statistical Analysis
```
POST /api/v1/analysis/descriptive - วิเคราะห์เชิงสถิติ
POST /api/v1/analysis/correlation - วิเคราะห์ความสัมพันธ์
```

### 📋 Visualization
```
POST /api/v1/visualization/chart - สร้างกราฟ
POST /api/v1/visualization/dashboard - สร้าง dashboard
```

### 🤖 Machine Learning
```
POST /api/v1/ml/train - ฝึกสอนโมเดล
POST /api/v1/ml/predict - ทำนายผลลัพธ์
```

### ✅ Data Validation
```
POST /api/v1/validation/quality - ตรวจสอบคุณภาพข้อมูล
POST /api/v1/validation/schema - ตรวจสอบ schema
```

### 📄 Report Generation
```
POST /api/v1/reports/generate - สร้างรายงาน
POST /api/v1/reports/export - export รายงาน
```

## 💻 การติดตั้งและรัน

### วิธีที่ 1: Manual Installation
```bash
# ติดตั้ง dependencies
pip install flask pandas numpy scikit-learn requests python-dateutil

# รันโปรแกรม
python app.py
```

### วิธีที่ 2: ใช้ Setup Scripts
```bash
# Windows
setup.bat

# Linux/Mac
./setup.sh
```

### วิธีที่ 3: Docker
```bash
# Build และรัน
docker-compose up --build
```

## 🧪 การทดสอบ

### ทดสอบแบบง่าย
```bash
python simple_test.py
```

### ทดสอบแบบครบถ้วน
```bash
python test_api.py
```

### ทดสอบ manually
```bash
# Health check
curl http://localhost:5000/health

# หรือเปิดในเว็บเบราว์เซอร์
http://localhost:5000/health
```

## 📝 ตัวอย่างการใช้งาน

### 1. วิเคราะห์เชิงสถิติ
```json
POST /api/v1/analysis/descriptive
{
  "columns": ["revenue", "profit", "customers"]
}
```

### 2. สร้างกราฟ
```json
POST /api/v1/visualization/chart
{
  "chart_type": "bar",
  "config": {
    "title": "Sales Performance",
    "width": 800,
    "height": 600
  }
}
```

### 3. ฝึกสอนโมเดล ML
```json
POST /api/v1/ml/train
{
  "model_type": "classification",
  "algorithm": "random_forest",
  "model_name": "sales_predictor"
}
```

## 🔧 Technology Stack

- **Backend Framework**: Flask
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Statistics**: SciPy
- **Visualization**: Matplotlib, Plotly (optional)
- **Containerization**: Docker
- **API Testing**: Requests

## 📈 สถานะปัจจุบัน

✅ **ใช้งานได้แล้ว**:
- ✅ Data processing features
- ✅ Statistical analysis
- ✅ Machine learning capabilities
- ✅ Data validation
- ✅ Report generation (logic)
- ✅ API endpoints ครบถ้วน
- ✅ Error handling
- ✅ Logging system
- ✅ Docker support

🔄 **สำหรับการพัฒนาต่อ**:
- Authentication & Authorization
- Database integration
- Advanced visualization (ต้องติดตั้ง matplotlib, plotly)
- Real-time data processing
- API documentation (Swagger)
- Comprehensive testing suite

## 🎯 การใช้งานจริง

Microservice นี้พร้อมใช้งานสำหรับ:
- 📊 Data analysis pipelines
- 🤖 ML model serving
- 📈 Business intelligence dashboards
- 📄 Automated reporting systems
- ✅ Data quality monitoring

Service รันอยู่ที่: **http://localhost:5000**

สามารถเริ่มใช้งานได้ทันทีหลังจากรัน `python app.py` ✨
