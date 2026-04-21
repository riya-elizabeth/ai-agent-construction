import csv
import json
from agent.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()

# Load ground truth
questions = []
with open("evaluation/ground_truth.csv", "r", encoding="utf-8-sig", errors="replace") as f:
    reader = csv.DictReader(f)
    for row in reader:
        questions.append(row)

print(f"Loaded {len(questions)} questions\n")
print("="*60)

results = []
for i, q in enumerate(questions):
    print(f"\n[{i+1}/{len(questions)}] {q['question'][:70]}...")
    result = pipeline.ask(q['question'])
    
    results.append({
        "question": q["question"],
        "expected": q["expected_answer"],
        "got": result["response"],
        "answered": result["answered"],
        "sources": result["sources"]
    })
    
    print(f"Answered: {result['answered']}")
    print(f"Sources:  {result['sources']}")

# Save results for review
with open("evaluation/quick_results.json", "w") as f:
    json.dump(results, f, indent=2)

# Basic stats
answered = sum(1 for r in results if r["answered"])
unanswered = len(results) - answered
print("\n" + "="*60)
print(f"RESULTS SUMMARY")
print(f"Total questions:  {len(results)}")
print(f"Answered:         {answered} ({answered/len(results)*100:.1f}%)")
print(f"Unanswered:       {unanswered} ({unanswered/len(results)*100:.1f}%)")
print(f"\nFull results saved to evaluation/quick_results.json")
print("Review that file to manually score correctness.")
