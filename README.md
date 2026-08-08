To run the code:<br>

Structure:<br>
├── data_acquisition.py       # Scraper for online MCSR API to generate mcsr_matches_dataset.csv    <br>
├── data_analysis.py          # Data cleaning and matrix exports<br>
├── visualization_generator.py # Visualization code to generate plots<br>
├── mcsr_matches_dataset.csv  # Collected dataset from data_acquisition.py<br>
├── results/                  # Generated plots<br>
│   ├── 1_median_time_heatmap.png<br>
│   ├── 2_forfeit_rate_heatmap.png<br>
│   ├── 3_rank_progression_lines.png<br>
│   ├── 4_time_distributions_boxplot.png<br>
│   └── 4_time_distributions_boxplot.png<br>
├── .gitignore                # Git ignore rules <br>
└── README.md                 # Project documentation<br>

Requirements:<br>
requests<br>
pandas<br>
numpy<br>
scipy<br>
matplotlib<br>
seaborn<br>

Install with: pip install requests pandas numpy scipy matplotlib seaborn<br>

Running the code (note that data_acquisition.py will take between 1-1.5 hours to finish):<br>
python data_acquisition.py<br>
python data_analysis.py<br>
python visualization_generator.py<br>
