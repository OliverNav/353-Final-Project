To run the code:

Structure:
├── data_acquisition.py       # Scraper for online MCSR API to generate mcsr_matches_dataset.csv    
├── data_analysis.py          # Data cleaning and matrix exports
├── visualization_generator.py # Visualization code to generate plots
├── mcsr_matches_dataset.csv  # Collected dataset from data_acquisition.py
├── results/                  # Generated plots
│   ├── 1_median_time_heatmap.png
│   ├── 2_forfeit_rate_heatmap.png
│   ├── 3_rank_progression_lines.png
│   ├── 4_time_distributions_boxplot.png
│   └── 4_time_distributions_boxplot.png
├── .gitignore                # Git ignore rules 
└── README.md                 # Project documentation

Requirements:
requests
pandas
numpy
scipy
matplotlib
seaborn

Install with: pip install requests pandas numpy scipy matplotlib seaborn

Running the code:
python data_acquisition.py
python data_analysis.py
python visualization_generator.py
