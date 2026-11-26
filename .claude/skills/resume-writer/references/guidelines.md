# Full content guidelines

This is the complete set of content-level tips from the source guide, organized by
topic. **Deliberately excluded**: section 2 ("Resume structure and organization" —
headings, spacing, alignment, decoration, column count), section 8.1 ("ATS
formatting" — fonts, tables, images, symbols, PDF text-extraction), and section 9
("Visual design and formatting" — fonts, sizes, margins, colors). None of that is
controllable from the JSON content in this repo; it's owned entirely by the
`jsonresume-theme-compact` theme and Puppeteer's PDF rendering in `index.mjs`. Don't
try to apply those tips here — there's no lever in `resumes/*.json` that would do it.

For the achievement formula, action-verb table, quantification dimensions table,
and weak-vs-strong examples, see `toolkit.md` — this file cross-references it rather
than repeating the tables.

## 1. Positioning strategy

Decide this before writing anything:

- Write for the specific position/role this variant targets, not a complete life history.
- Think like a recruiter: they want evidence you can solve their problems, not a biography.
- Communicate value delivered, not duties held — what changed because the user worked there.
- Prioritize relevance over completeness — an older, more relevant job can outweigh a recent, less relevant one.
- Every section should reinforce one professional identity (Backend / Full Stack / DevOps / Computer Vision / etc.) rather than reading as "does everything."
- Seniority is demonstrated through complexity, autonomy, and ownership — not through the number of technologies listed.
- Where the facts support it, let the resume show progression: increasing responsibility, complexity, and independence over time.
- Assume a recruiter may only read the first third of the document — the summary and the top of the first job need to carry the most weight.

## 2. Professional summary (`basics.summary`)

Answers, in 2-4 sentences: who are you professionally, how experienced, strongest technical areas, what kind of problems you solve.

- Start with the professional title/positioning.
- Mention years of relevant experience when it's meaningful to the story.
- Name the strongest technical specialties for the target role.
- Work in one or two measurable achievements if they exist.
- Lead with professional strengths, not personality adjectives ("passionate", "hardworking").
- Tailor it per variant — don't reuse one generic summary across all of them.
- Avoid: "looking for opportunities" framing, unnecessary personal details, restating the entire skills section, unsupported claims ("world-class engineer").
- Prefer concrete evidence over subjective description (see the weak-vs-strong example in `toolkit.md`).

## 3. Professional experience (`work[]`)

The most important section — it should show the user has already solved problems like the ones this employer has.

- Use the achievement formula (Action + implementation + context + result) as a starting template — see `toolkit.md`.
- Describe accomplishments, not assigned tasks. State the problem, how it was solved, and what changed.
- Name the technologies that were genuinely load-bearing for the result, not every tool touched in passing.
- Quantify wherever a real number or defensible estimate exists — scale, performance, efficiency, quality, business impact, complexity, adoption, delivery (full dimension table in `toolkit.md`). Never invent a number (ground rule 1 in `SKILL.md`).
- Highlight: independent decisions, systems designed from scratch, architectural choices influenced, end-to-end ownership (design → deploy → maintain), cross-team collaboration, process/performance/reliability improvements, automation that removed manual work, and effects on real users or customers.
- Avoid: listing every small task, repeating the same achievement across multiple bullets, first-person pronouns.
- Verb tense: past tense for past roles, present tense only for the current role.
- Keep bullets to one or two lines; put the strongest achievement first in each entry.
- Use strong, specific action verbs (table in `toolkit.md`) — avoid "responsible for / worked on / helped with / participated in / involved in / assisted with," which tend to hide the actual contribution.

## 4. Technical skills (`skills[]`)

- Group into meaningful categories rather than one long flat list (see the example grouping in the original guide — languages, backend, frontend, databases, cloud/infra, tools).
- Put the most relevant categories and items first, especially ones named in a target job posting — only if genuinely true.
- Internally classify each skill as Core (used independently in production) / Intermediate (comfortable, less experience) / Familiar (understood, limited hands-on) to decide prominence and the `level` field — these labels don't need to appear verbatim in the JSON.
- Include architectural concepts and relevant infra/testing/cloud experience, not just language names.
- Avoid: listing every technology ever touched, proficiency percentage bars (not meaningful in this schema anyway), claiming expertise after one tutorial, repeating a skill across multiple categories, obsolete tech irrelevant to the target role.
- Use official technology names.
- Ground rule: every skill listed must be defensible in an interview.

## 5. Projects (`projects[]`)

- Prefer fewer, substantial projects with real engineering decisions over many trivial ones.
- Describe the problem solved and the interesting technical challenge — not just a tag list of technologies.
- Mention architecture when relevant, the user's individual contribution, measurable outcomes if any, and GitHub/demo links when public.
- Academic/research projects are fine to include when they demonstrate real engineering skill.
- Avoid projects unrelated to the target role unless they demonstrate a transferable capability.
- See the weak-vs-strong project description example in `toolkit.md`.

## 6. Education and certifications (`education[]`, `certificates[]`)

- Include institution, degree/area, and consistent date formats.
- Mention academic distinctions and relevant coursework, especially when professional experience is thin.
- Include real, completed certifications only — never present an unfinished one as complete.
- Don't list every course taken — only the ones that support the positioning.
- For an experienced engineer, education should occupy less space than professional experience; trim or drop older/less relevant academic detail before trimming real work achievements.

## 7. Keyword / ATS content matching (not formatting)

This is about which words appear in the content, not how the page is laid out (that part is excluded, see the top of this file).

- Identify the 4-5 most important requirements and explicit technology names in a target job posting.
- Weave them into summary and experience bullets *in context* — "Designed TypeScript-based Node.js microservices exposing REST APIs..." — not as a bare keyword dump.
- Prioritize required qualifications over optional/nice-to-have ones.
- Use the employer's terminology when it genuinely and accurately describes the user's experience.
- Never add a keyword or claim experience the user doesn't actually have, just to match a posting (ties to ground rule 1/3 in `SKILL.md`). Keyword stuffing without substance is explicitly a mistake to avoid, not a technique to use.

## 8. Contact info and personal details (`basics.*`)

What belongs in the JSON vs. what to leave out:

- Include: professional email, phone (with country code for international applications), LinkedIn, GitHub (for technical roles), portfolio URL if it adds real evidence, city/country.
- Verify every link actually resolves before treating a resume as finished.
- Use one consistent professional name across variants.
- Leave out: full residential address, national ID numbers, marital status, date of birth, other personal details that don't support the application.
- A profile photo (`basics.image`) is generally unnecessary for international software engineering applications — keep it only if local convention or the specific employer expects one.

## 9. Tailoring to a specific vacancy

- Analyze the posting first: top 4-5 requirements, explicitly named technologies, the underlying business problem.
- Move the most relevant work experience higher in emphasis (can't reorder which job came first in time, but can decide which bullets lead and which get cut).
- Rewrite the summary for this specific role rather than reusing another variant's.
- Reorder skill categories/keywords so the most relevant ones for this role come first.
- Reframe real achievements to emphasize the angle this employer cares about (e.g., the same project described for API architecture in a backend variant vs. end-to-end delivery in a full-stack variant) — adjust emphasis without changing the underlying truth.
- Drop irrelevant detail when space is limited rather than diluting the positioning by keeping everything.
- Name the resulting file to match this project's convention: snake_case, role-describing (`computer_vision.json`, not the person's name).

## 10. Common content mistakes to avoid

| Mistake | Why it hurts |
|---|---|
| Generic professional summary | Doesn't differentiate the candidate |
| Listing responsibilities instead of achievements | Doesn't demonstrate impact |
| Too many technologies listed | Makes real expertise unclear |
| Unquantified achievements where a number was available | Reduces credibility and specificity |
| Exaggerated proficiency | Creates problems in the interview |
| Unnecessary personal details | Wastes space without adding value |
| Irrelevant experience kept in | Dilutes the positioning |
| Fake or invented metrics | Damages credibility — never do this |
| Outdated information left in | Creates doubts about accuracy |
| Excessive length for the experience level | Buries the strongest achievements |

## 11. Advanced differentiation techniques

- **Show the full engineering lifecycle** when it's true: requirements → design → implementation → testing → deployment → monitoring → iteration — not just "developed a feature."
- **Name the hard part.** If the work involved distributed synchronization, offline-first design, high-throughput processing, complex integrations, database optimization, legacy modernization, event-driven architecture, real-time communication, infra automation, performance bottlenecks, security, or fault tolerance — say so and say why it was hard.
- **Use decision-making language** when the user actually made the call: "Designed the architecture for...", "Evaluated and selected...", "Proposed and implemented...", "Established a reusable framework...". Only when it's true that the user drove the decision, not just executed it.
- **Connect technical work to business impact** where a real connection exists (automation → lower operational cost, better API performance → better UX, reliability work → less downtime, internal tooling → team productivity). Don't invent a business number that was never measured.
- **Balance breadth and depth** — a long tech list shows neither; a combination of real production experience, architecture decisions, and a few substantial projects shows both.

## 12. Resume length and information density

Recommended page count by years of experience:

| Experience | Recommended length |
|---|---|
| Student / internship | 1 page |
| 0-3 years | 1 page |
| 3-7 years | 1-2 pages |
| 7-12 years | 2 pages |
| 12+ years | 2-3 pages if justified |

These are guidelines, not hard limits. `scripts/score_resume.py` (see `SKILL.md` step 6) checks a built resume against this table and measures how full the last page actually is.

- Don't artificially pad to fill a page, and don't cut a genuinely valuable achievement just to force-fit one page.
- Don't remove real content merely to hit a page count — but do cut repeated information, information that doesn't support the target positioning, and obsolete tech/projects before trimming anything that's still relevant.
- Prefer raising information density (tighter wording) over deleting a whole bullet, when that's enough.
- Every bullet should earn the space it occupies.

## 13. Building an achievement inventory

Useful technique when gathering missing information (ties into `SKILL.md` step 2 — ask, don't guess). For each job or project, the facts worth having before writing a bullet:

| Question | Example |
|---|---|
| What problem existed? | Manual operational workflows |
| What was the contribution? | Designed backend services |
| What technologies were used? | TypeScript, Node.js, GCP |
| How complex was it? | Multiple integrated microservices |
| What was the scale? | 10+ services |
| What changed afterward? | Reduced manual operations |
| What was owned, specifically? | Design through deployment |
| What makes it interesting? | Proposed event-driven architecture |

The same underlying facts can be described differently depending on which variant is being written (e.g., emphasize API/data design for a backend-flavored variant vs. end-to-end delivery for a full-stack one) — without changing what actually happened.

## 14. Pre-submission content checklist

Content-only subset of the guide's QA checklist (the formatting/ATS-document items — PDF text extraction, one-column layout, info not in images — are excluded; see the top of this file):

- The professional title/positioning matches the target role.
- The summary communicates the strongest qualifications for this role.
- The most relevant experience is emphasized, not necessarily just the most recent.
- Achievements read stronger than responsibility descriptions throughout.
- The experience shown demonstrates real ownership, not just task completion.
- Irrelevant information for this target role has been removed.
- Every technology listed is one the user could defend in an interview.
- Relevant architectural concepts are represented, not just language/tool names.
- Achievements are quantified wherever a real or defensible number exists.
- At least one genuinely complex engineering challenge is described somewhere.
- Projects demonstrate real technical ability, not a tech-stack tag list.
- Nothing is exaggerated beyond what's true.
- Contact details are correct and every link resolves.
- No spelling or grammar errors.
- Dates are consistent and in the same format throughout the file.
- Length is appropriate for years of experience (see §12) and `scripts/score_resume.py` doesn't flag room to shrink a page.
- The filename follows this repo's convention.
- The variant has actually been tailored to the target role/posting, not left generic.

## 15. The ten highest-priority principles

If only ten things from this whole file mattered, they'd be:

1. Lead with value: what you can contribute, not just who you are.
2. Replace responsibilities with concrete achievements.
3. Quantify impact wherever a real number exists.
4. Demonstrate ownership — conception through production, where true.
5. Show technical depth through real, specific challenges solved.
6. Tailor every variant — different roles deserve different emphasis.
7. Match the employer's real terminology naturally, never by stuffing keywords.
8. Keep it concise — every sentence should justify its presence.
9. Never exaggerate technologies, metrics, or responsibilities.
10. Make it scannable — the value should land within seconds.
