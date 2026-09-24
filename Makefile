install:
	pip install -r requirements.txt

dashboard:
	streamlit run app/dashboard.py

train:
	python src/training/train_classifier.py

test:
	pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
