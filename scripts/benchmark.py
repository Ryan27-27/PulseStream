import argparse
import subprocess
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10000)
    args = parser.parse_args()

    subprocess.run(
        ["python", "scripts/generate_events.py", "--count", str(args.count)],
        check=True,
    )

    start = time.perf_counter()
    subprocess.run(["python", "scripts/run_spark_job.py"], check=True)
    elapsed = time.perf_counter() - start

    print(f"dataset_size={args.count}")
    print(f"spark_runtime_seconds={elapsed:.3f}")


if __name__ == "__main__":
    main()
