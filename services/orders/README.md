# Data Analytics Microservice

## รายละเอียด

Microservice สำหรับการวิเคราะห์ข้อมูล (Data Analytics) ที่ประกอบด้วยหลาย features หลัก:

### Features หลัก

1. **Data Processing** (`features/data_processor.py`)
   - อัปโหลดและประมวลผลไฟล์ข้อมูล (CSV, JSON, Excel)
   - ทำความสะอาดข้อมูล (Data Cleaning)
   - ตรวจสอบคุณภาพข้อมูล

2. **Statistical Analysis** (`features/statistical_analyzer.py`)
   - การวิเคราะห์เชิงสถิติเบื้องต้น (Descriptive Statistics)
   - การวิเคราะห์ความสัมพันธ์ (Correlation Analysis)
   - การทดสอบสมมติฐาน (Hypothesis Testing)
   - การตรวจจับค่าผิดปกติ (Outlier Detection)

3. **Visualization Service** (`features/visualization_service.py`)
   - สร้างกราฟและแผนภูมิต่างๆ
   - สร้าง Dashboard แบบ Interactive
   - Export ภาพในรูปแบบต่างๆ

4. **Machine Learning** (`features/ml_predictor.py`)
   - ฝึกสอนโมเดล Machine Learning
   - ทำนายผลลัพธ์
   - ประเมินประสิทธิภาพโมเดล

5. **Data Validation** (`features/data_validator.py`)
   - ตรวจสอบคุณภาพข้อมูล
   - ตรวจสอบ Schema ของข้อมูล
   - ตรวจจับความผิดปกติ
   - ตรวจสอบ Business Rules

6. **Report Generation** (`features/report_generator.py`)
   - สร้างรายงานแบบครอบคลุม
   - Export รายงานในรูปแบบต่างๆ (PDF, HTML, DOCX)
   - จัดตารางเวลารายงานอัตโนมัติ

## API Endpoints

### Data Processing
- `POST /api/v1/data/upload` - อัปโหลดข้อมูล
- `POST /api/v1/data/clean` - ทำความสะอาดข้อมูล

### Statistical Analysis
- `POST /api/v1/analysis/descriptive` - วิเคราะห์เชิงสถิติ
- `POST /api/v1/analysis/correlation` - วิเคราะห์ความสัมพันธ์

### Visualization
- `POST /api/v1/visualization/chart` - สร้างกราฟ
- `POST /api/v1/visualization/dashboard` - สร้าง Dashboard

### Machine Learning
- `POST /api/v1/ml/train` - ฝึกสอนโมเดล
- `POST /api/v1/ml/predict` - ทำนายผลลัพธ์

### Data Validation
- `POST /api/v1/validation/quality` - ตรวจสอบคุณภาพข้อมูล
- `POST /api/v1/validation/schema` - ตรวจสอบ Schema

### Report Generation
- `POST /api/v1/reports/generate` - สร้างรายงาน
- `POST /api/v1/reports/export` - Export รายงาน

## การติดตั้งและรันโปรแกรม

### 1. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 2. รันโปรแกรม

```bash
python app.py
```

โปรแกรมจะรันที่ `http://localhost:5000`

### 3. ทดสอบ Health Check

```bash
curl http://localhost:5000/health
```

## โครงสร้างไฟล์

```
MicroService-A/
├── app.py                          # Main application file
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
├── auto_label_microservice.py      # Original simple service
└── features/                       # Feature modules
    ├── __init__.py
    ├── data_processor.py           # Data processing features
    ├── statistical_analyzer.py     # Statistical analysis
    ├── visualization_service.py    # Visualization and charts
    ├── ml_predictor.py            # Machine learning
    ├── data_validator.py          # Data validation
    └── report_generator.py        # Report generation
```

## ตัวอย่างการใช้งาน

### อัปโหลดข้อมูล
```bash
curl -X POST -F "file=@data.csv" http://localhost:5000/api/v1/data/upload
```

### วิเคราะห์เชิงสถิติ
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"columns": ["column1", "column2"]}' \
     http://localhost:5000/api/v1/analysis/descriptive
```

### สร้างกราฟ
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"chart_type": "bar", "config": {"title": "Sample Chart"}}' \
     http://localhost:5000/api/v1/visualization/chart
```

## การพัฒนาต่อ

1. เพิ่ม Authentication และ Authorization
2. เชื่อมต่อกับฐานข้อมูลจริง
3. เพิ่ม Caching สำหรับประสิทธิภาพ
4. เพิ่ม Error Handling ที่ครอบคลุมมากขึ้น
5. เพิ่ม Unit Tests และ Integration Tests
6. เพิ่ม API Documentation ด้วย Swagger/OpenAPI
7. เพิ่ม Monitoring และ Logging

## Technologies Used

- **Flask** - Web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning
- **Matplotlib/Seaborn** - Data visualization
- **Plotly** - Interactive visualizations
- **SciPy** - Scientific computing
