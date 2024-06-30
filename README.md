# knowURsoil - GSC Soil Analyzer

## Overview

GSC Soil Analyzer is a web application developed for the Google Developers Solution Challenge 2024. It leverages advanced machine learning algorithms to analyze soil properties and provides personalized crop recommendations.

## Features

- **Soil Analysis**: Utilizes machine learning to assess soil quality.
- **Crop Recommendations**: Offers tailored crop suggestions based on soil data.

## Getting Started

### Prerequisites

- Python 3.9.13**************************
- Streamlit

### Installation

1. Clone the repository:
git clone https://github.com/denxxs/gsc-soilanalyzer.git

2. Install required packages:
pip install -r requirements.txt

3. Optional - Download the Client side app: if you are using our sensor raspberrypi4 with tcs3200 and dht11 sensors -- https://github.com/Quantum2511/gsc-client-side-knowURsoil


### Usage

To run the Streamlit application:
streamlit run app.py


## File Structure

- `app.py`: The main Streamlit application script.
- `Recommendation.py`: Script for generating crop recommendations.
- `cropRecommend.py`: Handles the model training for crop recommendations.
- `functions.py`: Contains helper functions used across the application.
- `config.py`: Configuration settings for the application.
- `models`: Stores the trained machine learning models.
- `data`: Contains datasets and data-related resources.
- `static`: Holds static files like images and CSS.
- `.env`: Environment variables for configuration.
- `.gitignore`, `.gcloudignore`: Configuration files for Git and Google Cloud.
- `.streamlit`: Streamlit specific configuration files.
- `requirements.txt`: Lists all Python dependencies.
- `app.yaml`: Configurations for Google App Engine deployment.

## Dataset

The project utilizes the [Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset) from Kaggle.

## Contributing

We welcome contributions. Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a Pull Request.

## License

[Specify the license, if applicable]

## Acknowledgments

- Google Developers Solution Challenge 2024
- Contributors and maintainers of this project
- Bhavya Chanana - https://www.linkedin.com/in/bhavya-chanana/ - https://github.com/bhavya-chanana
- Dennis Sagayanathan - https://www.linkedin.com/in/d3n/ - https://github.com/denxxs
