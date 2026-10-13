# Nepal at UNGA 81: Mapping Diplomatic Engagements Through Public Data

## Project Overview

What can publicly documented diplomatic meetings and events tell us about Nepal's participation in the 81st United Nations General Assembly?

Following Nepal's participation in UNGA 81 in September 2026, I collected and analysed information shared through the Nepal Foreign Minister's public social media accounts.

I was particularly interested in the diplomatic engagements taking place beyond the formal speeches: who Nepal was meeting, which issues were discussed, and how the topics raised in diplomatic meetings compared with those discussed at multilateral events.

This project uses Python to clean, analyse and visualise these publicly documented engagements.

## Dataset

The dataset contains:

- **31 diplomatic meetings**
- **22 multilateral events**
- **53 documented engagements in total**

Information was collected primarily from the Foreign Minister's public Instagram and Facebook posts.

The data was organised into two CSV files:

- `data/meetings.csv`
- `data/events.csv`

The analysis uses categorised meeting types, geographic information, dates and discussion topics extracted from publicly available descriptions.

Individual engagements could contain multiple topics.

## Tools and Technologies

- **Python**
- **pandas** — data cleaning, transformation and analysis
- **Matplotlib and Seaborn** — data visualisation
- **Plotly** — geographic and interactive visualisation

## Key Findings

### 1. Geographic distribution

Europe accounted for the highest number of documented diplomatic meetings (10), followed by Asia (9). Engagements also involved representatives from Africa, North America, Oceania and international organisations.

### 2. Topics discussed

Bilateral relations was the most frequently documented topic in bilateral meetings, appearing in 24 of 26.

Flood recovery and climate also featured frequently, alongside education, tourism, regional cooperation, development and trade.

### 3. Bilateral meetings versus multilateral events

Climate appeared in approximately 23% of both meetings and multilateral events.

Flood recovery was documented more frequently in meetings (29%) than in events (18.2%).

UN reform showed the opposite pattern, appearing in 13.6% of events compared with 3.2% of meetings.

### 4. Diplomatic activity over time

25 September was the busiest day in the documented meeting records, with nine meetings.

Multilateral event activity was highest on 24 and 25 September, with six recorded events on each day.

## Methodology

1. Collected publicly available information about Nepal's diplomatic meetings and multilateral events.
2. Organised the information into structured CSV datasets.
3. Cleaned and standardised dates, categories and topic labels.
4. Analysed geographic distribution, meeting types, topic frequencies and daily activity.
5. Compared topic frequencies across meetings and multilateral events using percentages to account for differences in dataset size.
6. Created visualisations to communicate the findings.

## Limitations

This analysis is based on publicly documented engagements and should not be interpreted as a comprehensive account of Nepal's participation at UNGA 81.

The Foreign Minister reportedly referred to 80 engagements in a parliamentary address, while this dataset contains 53.

Additionally:

- Public social media posts do not necessarily capture every diplomatic engagement.
- Meeting descriptions may omit topics discussed privately.
- The frequency of a topic does not indicate its political importance.
- Participation in a discussion does not necessarily imply a commitment or policy outcome.

The findings therefore describe patterns in publicly communicated diplomatic activity rather than providing a definitive assessment of Nepal's foreign policy priorities.

## Project Structure

```text
UNGA/
├── data/
│   ├── meetings.csv
│   └── events.csv
├── figures/
├── main/
│   └── analysis.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Running the Analysis

Install the required Python packages:

```bash
python3 -m pip install -r requirements.txt
```

Run the analysis:

```bash
python3 main/analysis.py
```

## Further Reading

A longer discussion of the findings, motivation and limitations is available in my accompanying blog post: *What Following Nepal's Participation at UNGA 81 Revealed*.