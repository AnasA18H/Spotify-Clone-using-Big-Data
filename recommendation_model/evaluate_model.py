from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALSModel
from pyspark.ml.evaluation import RegressionEvaluator

# Create SparkSession
spark = SparkSession.builder.appName("ModelEvaluation").getOrCreate()

# Load test data from MongoDB into a Spark DataFrame
test_data = (
    spark.read.format("com.mongodb.spark.sql.DefaultSource")
    .option("uri", "mongodb://localhost:27017/fma_dataset.audio_features_test")
    .load()
)

# Load the trained model
saved_model_path = "path/to/saved/model"
model = ALSModel.load(saved_model_path)

# Make predictions on the test data
predictions = model.transform(test_data)

# Define evaluator
evaluator = RegressionEvaluator(
    metricName="rmse", labelCol="rating", predictionCol="prediction"
)

# Evaluate the model using RMSE
rmse = evaluator.evaluate(predictions)
print("Root Mean Squared Error (RMSE) = ", rmse)

# Stop the SparkSession
spark.stop()
