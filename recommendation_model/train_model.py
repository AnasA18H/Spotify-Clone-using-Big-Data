from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode
from pyspark.ml.recommendation import ALS
from pyspark.sql.functions import mean
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

# Initialize SparkSession
spark = (
    SparkSession.builder.appName("MusicRecommendation")
    .config(
        "spark.mongodb.input.uri",
        "mongodb://localhost:27017/fma_dataset.audio_features",
    )
    .config(
        "spark.mongodb.output.uri",
        "mongodb://localhost:27017/fma_dataset.features",
    )
    .getOrCreate()
)

# Load data from MongoDB
df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

# Explode the spectral_centroid array
df_spectral = df.selectExpr(
    "file_name as file_name_id",
    "track_id",
    "explode(spectral_centroid[0]) as spectral_centroid_val",
)

# Explode the zero_crossing_rate array
df_zero_crossing = df.selectExpr(
    "file_name as file_name_id",
    "explode(zero_crossing_rate[0]) as zero_crossing_rate_val",
)

# Explode the mfcc array
df_mfcc = df.selectExpr("file_name as file_name_id", "mfcc as mfcc_val")

# Join the DataFrames on track_id
df_combined = df_spectral.join(df_zero_crossing, "file_name_id")
df = df_combined.join(df_mfcc, "file_name_id")

df_final = df.groupBy("file_name_id", "track_id").agg(
    mean("zero_crossing_rate_val").alias("mean_zero_crossing_rate"),
    mean("spectral_centroid_val").alias("mean_spectral_centroid"),
)

assembler = VectorAssembler(
    inputCols=["mean_spectral_centroid", "mean_zero_crossing_rate"],
    outputCol="features",
)
df_final = assembler.transform(df_final)


df_final.show()
df_final = df_final.withColumn("track_id", col("track_id").cast("int"))
df_final = df_final.withColumn("file_name_id", col("file_name_id").cast("int"))
df_final = df_final.fillna({"file_name_id": 0})

train_data, test_data = df_final.randomSplit([0.5, 0.5], seed=42)

als = ALS(
    maxIter=10,
    regParam=0.01,
    userCol="track_id",
    itemCol="track_id",
    ratingCol="mean_spectral_centroid",  # Assuming features as ratings
    coldStartStrategy="drop",
)

# Fit the ALS model on the training data
model = als.fit(train_data)

predictions = model.transform(test_data)

# # Show some sample predictions
predictions.select("track_id", "file_name_id", "prediction").show()

evaluator = RegressionEvaluator(
    metricName="rmse", labelCol="mean_spectral_centroid", predictionCol="prediction"
)

rmse = evaluator.evaluate(predictions)
print("Root Mean Squared Error (RMSE) = " + str(rmse))

model.save("music_recommendation_model")

spark.stop()
