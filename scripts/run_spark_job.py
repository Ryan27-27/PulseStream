from pathlib import Path
import json
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main():
    input_path = "data/raw/events.jsonl"
    output_path = "data/curated/events"
    report_path = Path("data/reports/summary.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    spark = (
        SparkSession.builder
        .appName("PulseStreamAnalytics")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )

    df = spark.read.json(input_path)
    df = (
        df.withColumn("event_timestamp", F.to_timestamp("event_timestamp"))
        .withColumn("event_date", F.to_date("event_timestamp"))
        .dropDuplicates(["event_id"])
    )

    df.write.mode("overwrite").partitionBy("event_date", "region").parquet(output_path)

    summary = (
        df.agg(
            F.count("*").alias("total_events"),
            F.sum(F.when(F.col("status") == "delivered", 1).otherwise(0)).alias(
                "delivered_events"
            ),
            F.sum(F.when(F.col("status") == "failed", 1).otherwise(0)).alias(
                "failed_events"
            ),
            F.avg("latency_ms").alias("average_latency_ms"),
            F.expr("percentile_approx(latency_ms, 0.50)").alias("p50_latency_ms"),
            F.expr("percentile_approx(latency_ms, 0.95)").alias("p95_latency_ms"),
            F.expr("percentile_approx(latency_ms, 0.99)").alias("p99_latency_ms"),
        )
        .collect()[0]
        .asDict()
    )

    total = summary["total_events"] or 0
    delivered = summary["delivered_events"] or 0
    summary["delivery_rate"] = delivered / total if total else 0.0

    report_path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(json.dumps(summary, indent=2, default=str))
    spark.stop()


if __name__ == "__main__":
    main()
