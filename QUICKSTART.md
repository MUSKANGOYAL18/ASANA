

**## Step 1: Install Dependencies**

cd asana
pip install -r requirements.txt
```

****Step 2: Configure API Key****

# Copy environment template
cp .env.example .env


```

## Step 3: Generate Database 

python src/main.py


**Output**: `output/asana_simulation.sqlite`

## Step 4: Validate

python src/utils/validate.py output/asana_simulation.sqlite

## step  5: to see database
install sqlite extension in VS Code










