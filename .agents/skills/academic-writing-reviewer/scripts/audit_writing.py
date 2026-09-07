#!/usr/bin/env python3
"""
audit_writing.py - CLI orquestrador da auditoria de escrita acadêmica (academic-writing-reviewer).

Executa os 3 analisadores determinísticos:
1. check_ai_markers.py (AIM-01 a AIM-05)
2. check_repetition.py (REP-01 a REP-03, AIM-04)
3. check_numeric_tensions.py (NUM-01, NUM-02)
E realiza a checagem de glosa interdisciplinar (JAR-01 para "latência", "tokens", etc.).

Gera:
- Score advisory (0-100) para a Dimensão 5 do review 6-D.
- Status: PASS_FOR_DIM5 | PASS_WITH_MINOR_ISSUES | MAJOR_REVISION_RECOMMENDED.
- Relatório no formato padrão em review/writing-review-report.md.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List

try:
    from check_ai_markers import AIMarkerChecker
    from check_repetition import RepetitionChecker
    from check_numeric_tensions import NumericTensionChecker
except ImportError:
    from .check_ai_markers import AIMarkerChecker
    from .check_repetition import RepetitionChecker
    from .check_numeric_tensions import NumericTensionChecker


UNGLOSSED_TARGETS = [
    (r"\blatênci(a|as)\b", r"latênci\w*[^.!?\n]*(?:tempo|espera|delay|atraso|resposta|ms|milisegund)", "latência", "JAR-01"),
    (r"\blatenc(y|ies)\b", r"latenc\w*[^.!?\n]*(?:time|delay|wait|round-trip|ms|millisecond)", "latency", "JAR-01"),
    (r"\btoken(\s+budget|s)?\b", r"token\w*[^.!?\n]*(?:custo|palavra|unidade|consumo|cost|budget|unit)", "token budget", "JAR-01"),
    (r"\bcontext\s+window\b", r"context\s+window[^.!?\n]*(?:limite|memória|capacidade|capacity|limit)", "context window", "JAR-01"),
]


class WritingAuditor:
    def __init__(self):
        self.ai_checker = AIMarkerChecker()
        self.rep_checker = RepetitionChecker()
        self.num_checker = NumericTensionChecker()

    def check_glossary(self, draft_dir: str) -> List[Dict[str, Any]]:
        """Verifica se termos especializados de computação foram devidamente glosados em seu primeiro uso."""
        findings = []
        md_files = []
        for root, _, files in os.walk(draft_dir):
            for f in sorted(files):
                if f.endswith(".md") and not any(x in f for x in ["outline", "submission", "title", "table", "figure"]):
                    md_files.append(os.path.join(root, f))

        seen_terms = set()
        for fpath in md_files:
            fname = os.path.basename(fpath)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.splitlines()
            for idx, line in enumerate(lines, start=1):
                # Pular código e cabeçalho
                if line.strip().startswith("#") or line.strip().startswith("```"):
                    continue

                for term_pattern, gloss_pattern, term_name, code in UNGLOSSED_TARGETS:
                    if term_name in seen_terms:
                        continue

                    if re.search(term_pattern, line, re.IGNORECASE):
                        seen_terms.add(term_name)
                        # Checar se há glosa na mesma frase ou no mesmo parágrafo
                        has_gloss = bool(re.search(gloss_pattern, line, re.IGNORECASE))
                        if not has_gloss:
                            findings.append({
                                "file": fname,
                                "line": idx,
                                "issue_code": code,
                                "severity": "WARNING",
                                "term": term_name,
                                "snippet": line.strip()[:100],
                                "suggestion": f"Termo técnico '{term_name}' sem glosa explicativa no primeiro uso. Para bancas e periódicos de Gestão / Engenharia de Produção, adicione uma definição funcional sucinta (ex.: 'latência (tempo de espera entre a requisição e a resposta do modelo)')."
                            })

        return findings

    def run_audit(self, draft_dir: str) -> Dict[str, Any]:
        ai_res = {}
        total_ai_markers = 0
        ai_findings = []

        for root, _, files in os.walk(draft_dir):
            for file in sorted(files):
                if file.endswith(".md"):
                    fpath = os.path.join(root, file)
                    res = self.ai_checker.check_file(fpath)
                    ai_res[file] = res
                    if "findings" in res:
                        ai_findings.extend(res["findings"])
                        total_ai_markers += len(res["findings"])

        rep_res = self.rep_checker.analyze_directory(draft_dir)
        num_res = self.num_checker.analyze_directory(draft_dir)
        gloss_findings = self.check_glossary(draft_dir)

        # Contagem de severidades
        critical_count = 0
        warning_count = 0
        advisory_count = 0

        # AI markers
        for f in ai_findings:
            if f["severity"] == "CRITICAL":
                critical_count += 1
            elif f["severity"] == "WARNING":
                warning_count += 1
            else:
                advisory_count += 1

        # Repetition
        critical_count += len(rep_res.get("cross_section_duplicates", []))
        for _, fres in rep_res.get("file_results", {}).items():
            for f in fres.get("findings", []):
                if f["severity"] == "WARNING":
                    warning_count += 1
                elif f["severity"] == "ADVISORY":
                    advisory_count += 1

        # Numeric tension
        critical_count += len(num_res.get("cross_section_tensions", []))
        for _, fres in num_res.get("file_results", {}).items():
            warning_count += fres.get("total_tensions", 0)

        # Glossary
        warning_count += len(gloss_findings)

        # Cálculo do Score Advisory (0 - 100)
        # Base: 100; CRITICAL: -15 pts; WARNING: -4 pts; ADVISORY: -1 pt
        deductions = (critical_count * 15) + (warning_count * 4) + (advisory_count * 1)
        score = max(0, min(100, 100 - deductions))

        # Status advisory
        if critical_count == 0 and score >= 85:
            status = "PASS_FOR_DIM5"
            status_desc = "Aprovado para a Dimensão 5 do Review 6-D (escrita madura, sem quebras críticas)."
        elif critical_count == 0 and score >= 70:
            status = "PASS_WITH_MINOR_ISSUES"
            status_desc = "Aprovado com ressalvas menores (ajustes estilísticos pontuais recomendados)."
        else:
            status = "MAJOR_REVISION_RECOMMENDED"
            status_desc = "Revisão substantiva de escrita recomendada (presença de duplicidades, contradições ou vícios graves)."

        return {
            "timestamp": datetime.now().isoformat(),
            "target_directory": draft_dir,
            "advisory_score": score,
            "status": status,
            "status_description": status_desc,
            "severity_summary": {
                "critical": critical_count,
                "warning": warning_count,
                "advisory": advisory_count
            },
            "ai_markers": ai_findings,
            "cross_section_duplicates": rep_res.get("cross_section_duplicates", []),
            "repetition_local": rep_res.get("file_results", {}),
            "numeric_tensions": num_res.get("cross_section_tensions", []),
            "numeric_local": num_res.get("file_results", {}),
            "glossary_issues": gloss_findings
        }

    def generate_markdown_report(self, results: Dict[str, Any]) -> str:
        s = results["severity_summary"]
        md = []
        md.append("# Relatório de Auditoria de Escrita (Academic Writing Review)")
        md.append(f"\n> Gerado em: {results['timestamp']} · Alvo: `{results['target_directory']}`")
        md.append(f"> **Status Advisory:** `{results['status']}` ({results['status_description']})")
        md.append(f"> **Score Advisory (Dimensão 5):** **{results['advisory_score']}/100**\n")

        md.append("## 1. Resumo por Severidade")
        md.append(f"- 🚨 **Críticas (CRITICAL):** {s['critical']}")
        md.append(f"- ⚠️  **Avisos (WARNING):** {s['warning']}")
        md.append(f"- ℹ️  **Sugestões (ADVISORY):** {s['advisory']}\n")

        # 2. Duplicações Transversais
        md.append("## 2. Redundâncias e Repetições Transversais (`REP-01`)")
        if results["cross_section_duplicates"]:
            for d in results["cross_section_duplicates"]:
                md.append(f"- **[{d['severity']}] {d['section_a']} $\\leftrightarrow$ {d['section_b']}** (Similaridade: {int(d['similarity_ratio']*100)}%)")
                md.append(f"  - *Trecho A:* \"{d['snippet_a']}\"")
                md.append(f"  - *Trecho B:* \"{d['snippet_b']}\"")
                md.append(f"  - *Direção de correção:* {d['suggestion']}")
        else:
            md.append("✅ Nenhuma duplicação transversal significativa detectada entre seções.\n")

        # 3. Tensões Narrativas e Coerência de Métricas
        md.append("## 3. Coerência Narrativa de Métricas e Tensões (`NUM-01`, `NUM-02`)")
        if results["numeric_tensions"]:
            for t in results["numeric_tensions"]:
                md.append(f"- **[{t['severity']}] Métrica '{t['metric'].upper()}':** {t['section_a']} ({t['direction_a']}) vs {t['section_b']} ({t['direction_b']})")
                md.append(f"  - *Trecho A:* \"{t['snippet_a']}...\"")
                md.append(f"  - *Trecho B:* \"{t['snippet_b']}...\"")
                md.append(f"  - *Direção de correção:* {t['suggestion']}")
        else:
            md.append("✅ Nenhuma contradição qualitativa de direção de métricas detectada.\n")

        # 4. Glosa Interdisciplinar
        md.append("## 4. Jargão Técnico e Glosa Interdisciplinar (`JAR-01`)")
        if results["glossary_issues"]:
            for g in results["glossary_issues"]:
                md.append(f"- **[{g['severity']}] {g['file']}:L{g['line']} — Termo: `{g['term']}`**")
                md.append(f"  - *Trecho:* \"{g['snippet']}...\"")
                md.append(f"  - *Direção de correção:* {g['suggestion']}")
        else:
            md.append("✅ Todos os termos computacionais monitorados foram devidamente contextualizados.\n")

        # 5. Marcadores e Vícios de IA
        md.append("## 5. Marcadores de IA e Fórmulas Clichê (`AIM-01` a `AIM-05`)")
        if results["ai_markers"]:
            for m in results["ai_markers"]:
                md.append(f"- **[{m['severity']}] {m['file']}:L{m['line']} — `{m['matched_text']}` ({m['tier']})**")
                md.append(f"  - *Snippet:* \"{m['snippet']}\"")
                md.append(f"  - *Sugestão:* {m['suggestion']}")
        else:
            md.append("✅ Nenhum marcador de vocabulário ou fórmula de IA detectado.\n")

        # 6. Ecos Locais e Inícios Monótonos
        md.append("## 6. Monotonia Rítmica e Ecos Locais (`REP-02`, `AIM-04`)")
        has_rep_local = False
        for fname, fres in results["repetition_local"].items():
            if fres.get("findings"):
                has_rep_local = True
                md.append(f"### {fname}")
                for f in fres["findings"]:
                    target = f.get('repeated_phrase') or f.get('word')
                    md.append(f"- [{f['severity']}] **{f['type']}:** `{target}`")
                    md.append(f"  - *Sugestão:* {f['suggestion']}")
        if not has_rep_local:
            md.append("✅ Ritmo de frases variado e ausência de ecos locais excessivos.\n")

        md.append("\n---\n*Este relatório é de caráter consultivo (advisory) e alimenta a Dimensão 5 (Writing & Style) do veredito do review-agent.*")
        return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Auditor completo de escrita acadêmica para tolkien.")
    parser.add_argument("draft_dir", help="Diretório contendo os rascunhos markdown (ex: draft/).")
    parser.add_argument("--output", "-o", help="Caminho para gravar o relatório markdown (ex: review/writing-review-report.md).")
    parser.add_argument("--json", action="store_true", help="Imprimir saída bruta em JSON.")
    args = parser.parse_args()

    auditor = WritingAuditor()
    results = auditor.run_audit(args.draft_dir)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    report_md = auditor.generate_markdown_report(results)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report_md)
        print(f"✅ Relatório gravado com sucesso em: {args.output}")

    # Exibe resumo no terminal
    print(f"=== Auditoria de Escrita Concluída ===")
    print(f"Status: {results['status']}")
    print(f"Score Advisory: {results['advisory_score']}/100")
    print(f"Issues: {results['severity_summary']['critical']} críticas, {results['severity_summary']['warning']} avisos, {results['severity_summary']['advisory']} sugestões")


if __name__ == "__main__":
    main()
