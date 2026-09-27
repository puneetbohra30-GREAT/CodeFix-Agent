const API = "http://127.0.0.1:8000";
let language = "python";

const examples = {
  python: {
    code: `def average(nums):\n    return sum(nums) / len(numbers)\n\nprint(average([10, 20]))`,
    error: "NameError: name 'numbers' is not defined"
  },
  cpp: {
    code: `#include <iostream>\n\nint main() {\n    cout << "Hello CodeFix";\n    return 0;\n}`,
    error: "Compilation error: cout was not declared in this scope"
  },
  java: {
    code: `public class Main {\n    public static void main(String[] args) {\n        int[] arr = {10, 20, 30};\n        for (int i = 0; i <= arr.length; i++) {\n            System.out.println(arr[i]);\n        }\n    }\n}`,
    error: "ArrayIndexOutOfBoundsException"
  }
};

const $ = id => document.getElementById(id);

function loadExample() {
  $("code").value = examples[language].code;
  $("error").value = examples[language].error;
}
document.querySelectorAll(".lang").forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll(".lang").forEach(x => x.classList.remove("active"));
    btn.classList.add("active");
    language = btn.dataset.lang;
    loadExample();
  };
});
loadExample();

function setTimeline(count) {
  document.querySelectorAll("#statusList div").forEach((x,i) => x.classList.toggle("done", i < count));
}

$("debugBtn").onclick = async () => {
  setTimeline(1);
  $("resultStatus").textContent = "RUNNING";
  $("execution").textContent = "Agent is analyzing and executing...";
  try {
    const res = await fetch(`${API}/api/debug`, {
      method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({language, code:$("code").value, error:$("error").value})
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Debug failed");
    setTimeline(6);
    $("cycles").textContent = data.attempts;
    $("resultStatus").textContent = data.status.toUpperCase();
    $("errorType").textContent = data.error_type || "—";
    $("errorLine").textContent = data.line ?? "—";
    $("rootCause").textContent = data.root_cause;
    $("explanation").textContent = data.explanation;
    $("fixedCode").textContent = data.fixed_code;
    $("execution").textContent = data.success
      ? `✓ PASSED\n\n${data.execution_output || "(No stdout)"}`
      : `✗ NOT VERIFIED\n\n${data.execution_output || "No successful execution."}`;
    refreshHistory();
  } catch (e) {
    $("resultStatus").textContent = "ERROR";
    $("execution").textContent = e.message;
    setTimeline(0);
  }
};

$("zipInput").onchange = async e => {
  const file = e.target.files[0];
  if (!file) return;
  const form = new FormData();
  form.append("file", file);
  $("overall").textContent = "SCANNING";
  try {
    const res = await fetch(`${API}/api/project/scan`, {method:"POST", body:form});
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Scan failed");
    const h = data.health;
    $("files").textContent = h.files_scanned;
    $("lines").textContent = h.lines_scanned;
    $("errors").textContent = h.errors_found;
    $("fixed").textContent = h.errors_fixed;
    $("remaining").textContent = h.remaining;
    $("healthCycles").textContent = h.debug_cycles;
    $("tests").textContent = `${h.tests_passed} / ${h.tests_total}`;
    $("overall").textContent = h.overall_status;
    $("scanFiles").innerHTML = data.files.map(f =>
      `<div>📄 ${f.file} · ${f.language} · ${f.lines} lines</div>`
    ).join("");
  } catch (e) {
    $("overall").textContent = "ERROR";
    $("scanFiles").textContent = e.message;
  }
};

async function refreshHistory() {
  const res = await fetch(`${API}/api/history`);
  const data = await res.json();
  $("history").innerHTML = data.slice(0,8).map(x =>
    `<div class="history-item"><div><b>${x.language.toUpperCase()}</b> · ${x.status}</div><small>${x.attempts} cycle(s) · ${x.created_at}</small></div>`
  ).join("") || "<p class='muted'>No debug sessions yet.</p>";
}
$("refreshHistory").onclick = refreshHistory;
refreshHistory();
