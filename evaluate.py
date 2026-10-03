import csv
import time
from llm_engine import analyze_job


def normalize(s):
    """Lowercase, strip, and standardize a label string."""
    return (s or "").strip().lower()


def main():
    correct_risk = 0
    correct_flags = 0
    total = 0
    false_positives = 0
    legit_total = 0
    results = []

    print("=" * 70)
    print("FreelanceGuard Evaluation - 40 Test Cases")
    print("=" * 70)

    with open("test_cases.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            expected_risk = normalize(row["expected_risk_level"]).upper()
            expected_flags = set(
                normalize(x) for x in (row["expected_indicators"] or "").split(";") if x.strip()
            )

            try:
                result = analyze_job(row["text"])
                detected_risk = normalize(result.get("risk_level", "")).upper()
                detected_flags = set(
                    normalize(i.get("type", "")) for i in result.get("risk_indicators", [])
                )

                risk_match = detected_risk == expected_risk
                flags_match = expected_flags.issubset(detected_flags)

                if risk_match:
                    correct_risk += 1
                if flags_match:
                    correct_flags += 1

                # False positives: expected LOW but detected HIGH
                if expected_risk == "LOW":
                    legit_total += 1
                    if detected_risk == "HIGH":
                        false_positives += 1

                # Show detailed mismatch info
                mismatch_note = ""
                if not risk_match:
                    mismatch_note += f" [RISK: expected {expected_risk}, got {detected_risk}]"
                if not flags_match:
                    missing = expected_flags - detected_flags
                    extra = detected_flags - expected_flags
                    if missing:
                        mismatch_note += f" [MISSING: {','.join(sorted(missing))}]"
                    if extra:
                        mismatch_note += f" [EXTRA: {','.join(sorted(extra))}]"

                results.append({
                    "id": row["id"],
                    "expected": expected_risk,
                    "detected": detected_risk,
                    "risk_match": "OK" if risk_match else "FAIL",
                    "flags_match": "OK" if flags_match else "FAIL",
                })

                print(f"ID {row['id']:>2} | Exp: {expected_risk:<6} | Got: {detected_risk:<6} | Risk: {'OK' if risk_match else 'FAIL'} | Flags: {'OK' if flags_match else 'FAIL'}{mismatch_note}")
                time.sleep(0.5)  # avoid rate limits

            except Exception as e:
                print(f"ID {row['id']:>2} | ERROR: {e}")
                results.append({
                    "id": row["id"],
                    "expected": expected_risk,
                    "detected": "ERROR",
                    "risk_match": "FAIL",
                    "flags_match": "FAIL",
                })
                time.sleep(0.5)

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)
    print(f"Total test cases:                {total}")
    print(f"Risk Level Classification:       {correct_risk}/{total} ({correct_risk/total*100:.1f}%)")
    print(f"Red Flag Detection (subset):     {correct_flags}/{total} ({correct_flags/total*100:.1f}%)")
    if legit_total:
        print(f"False Positive Rate (on LOW):    {false_positives}/{legit_total} ({false_positives/legit_total*100:.1f}%)")
    else:
        print(f"False Positive Rate (on LOW):    N/A")
    print("=" * 70)

    # Save results to CSV for reference
    with open("evaluation_results.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "expected", "detected", "risk_match", "flags_match"])
        writer.writeheader()
        writer.writerows(results)
    print("\nDetailed results saved to: evaluation_results.csv")


if __name__ == "__main__":
    main()