# Contribution
This project exists thanks to the extraordinary people who contributed to it.
-  Muhammad Daniyal Haider (i222042@nu.edu.pk)
-  Muhammad Anas Khan (i221987@nu.edu.pk)

# Music Recommendation System README

## Importance
This repository hosts a sophisticated Music Recommendation System designed to suggest songs to users based on their listening history. Leveraging Apache Spark for data processing, Apache Kafka for real-time streaming, and MongoDB for data storage, this system offers scalability, efficiency, and real-time recommendation capabilities similar to leading platforms like Spotify.

## Advantages
- **Personalized Recommendations**: By analyzing user listening history and preferences, the system provides personalized song recommendations tailored to individual tastes.
- **Real-time Updates**: Utilizing Apache Kafka for streaming ensures that recommendations are continuously updated in real-time as new data becomes available.
- **Scalability**: The use of distributed computing with Apache Spark enables the system to handle large volumes of data and user requests, making it scalable to accommodate growing user bases.
- **Efficient Data Processing**: With Apache Spark's powerful processing capabilities, the system can efficiently extract features from audio files and train recommendation models in parallel, leading to faster processing times.
- **Flexible Architecture**: The modular architecture of the system allows for easy integration with other components or services, facilitating customization and expansion based on specific requirements.
- **User Engagement**: The web interface provides an interactive platform for users to discover new music and engage with the system, enhancing user satisfaction and retention.

## Usage
To effectively utilize this Music Recommendation System, follow these steps:

1. **Set up Dependencies**: Ensure you have the necessary dependencies installed:
    - Apache Spark: Download and install from [Apache Spark Downloads](https://spark.apache.org/downloads.html)
    - Apache Kafka: Obtain from [Apache Kafka Downloads](https://kafka.apache.org/downloads)
    - MongoDB: Download and install from [MongoDB Downloads](https://www.mongodb.com/try/download/community)
    - Python 3.x: Install from [Python Downloads](https://www.python.org/downloads/)
    - Required Python libraries: Install using pip:
        ```bash
        pip install pyspark librosa pymongo
        ```

2. **Clone the Repository**: Clone this repository to your local machine:
    ```bash
    git clone <repository_url>
    ```

3. **Start MongoDB**: Start MongoDB service:
    ```bash
    sudo service mongod start  # for Linux
    ```

4. **Start PySpark**: Launch PySpark:
    ```bash
    pyspark
    ```

5. **Start Kafka Zookeeper**: Run Kafka Zookeeper:
    ```bash
    bin/zookeeper-server-start.sh config/zookeeper.properties
    ```

6. **Start Kafka Server**: Launch Kafka Server:
    ```bash
    bin/kafka-server-start.sh config/server.properties
    ```

7. **Data Processing**: Execute `audio_processing.py` to extract audio features and store them in MongoDB.

8. **Real-time Streaming**: Use Kafka for real-time streaming of data.

9. **Spark Processing**: Run `music_recommendation.py` to process data stored in MongoDB, train a recommendation model using ALS, and save the model.

10. **Website Deployment**: Deploy the website for user interaction and song recommendations. Integrate it with Kafka for real-time updates and Spark for recommendation queries.

11. **Interact with the System**: Users can receive song recommendations based on their listening history via the website, which continuously updates recommendations in real-time.

Ensure all dependencies are properly configured and integrated for seamless functionality.

## Functionality
- **Data Extraction and Feature Engineering**: `audio_processing.py` extracts features like MFCC, spectral centroid, and zero-crossing rate from audio files and stores them in MongoDB.
- **Real-time Streaming**: Apache Kafka facilitates real-time streaming of data, ensuring prompt processing of new listening data.
- **Recommendation Model Training**: Apache Spark's ALS algorithm trains a recommendation model using the extracted audio features. The trained model provides personalized song recommendations.
- **Website Design**: The system includes a web interface similar to Spotify, enabling users to interact and receive song suggestions based on their listening history.

## Dependencies
- Apache Spark
- Apache Kafka
- MongoDB
- Python 3.x
- PySpark
- Librosa
- PyMongo

Ensure all dependencies are properly configured and integrated for seamless functionality.

## Additional Information
- Customize the website design and user interface to align with preferences and requirements.
- Monitor system logs and error messages to troubleshoot any issues.
- For support, contact `Your Email`.

## Contributors
- `Sahil Kumar` - `i222048@nu.edu.pk`
- `Muhammad Daniyal Haider` - `i222042@nu.edu.pk`
- `Muhammad Anas Khan` - `i221987@nu.edu.pk`
- `Additional contributrion are welcomed fell free to use it.`

## License
This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- Mention any acknowledgments or credits for libraries, tutorials, or inspirations used in the project.
