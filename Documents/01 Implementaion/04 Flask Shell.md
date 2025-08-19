```bash
flask shell
```  
```bash
from app import app, db
from database import AlertThreshold, AlertLog

with app.app_context():
    db.create_all()
    # Optional: Add an initial threshold again if it was not created
    if not AlertThreshold.query.first():
        initial_threshold = AlertThreshold(location_name="Rajaram Bridge", parameter="FLOW", threshold_value=50000.0, is_active=True)
        db.session.add(initial_threshold)
        db.session.commit()
        print("Initial alert threshold added.")
```  