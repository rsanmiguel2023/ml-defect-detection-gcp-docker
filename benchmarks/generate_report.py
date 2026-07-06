"""
Generate a polished Markdown performance report from benchmark outputs.

Usage:
    python -m benchmarks.generate_report
"""

from pathlib import Path

from benchmarks.report_sections import (
    api_performance,
    batch_performance,
    benchmark_metadata,
    benchmark_methodology,
    conclusions,
    executive_summary,
    framework_comparison,
    future_enhancements,
    generated_artifacts,
    limitations,
    load_benchmark_data,
    model_performance,
    performance_assessment,
    performance_baseline,
    recommendations,
    test_environment,
)


def generate_performance_report() -> Path:
    docs_dir = Path("docs")
    docs_dir.mkdir(parents=True, exist_ok=True)

    data = load_benchmark_data()

    sections = [
        "# Performance Benchmark Report",
        executive_summary(data),
        test_environment(data),
        benchmark_methodology(),
        performance_assessment(data),
        api_performance(data),
        batch_performance(data),
        model_performance(data),
        framework_comparison(data),
        performance_baseline(),
        recommendations(),
        conclusions(),
        limitations(),
        future_enhancements(),
        benchmark_metadata(data),
        generated_artifacts(),
    ]

    content = "\n\n---\n\n".join(sections)

    output_path = docs_dir / "PERFORMANCE.md"
    output_path.write_text(content, encoding="utf-8")

    print(f"Performance report generated at: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_performance_report()
