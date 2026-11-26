---
name: resume-writer
description: Write, edit, and create tailored variants of job resumes stored in this repo's resumes/*.json files (JSON Resume schema, built into PDFs by index.mjs via the jsonresume-theme-compact theme). Use whenever the user wants to update an existing resume, add a new job/project/achievement, rewrite a summary, reorganize skills, tailor a resume to a specific job posting or role, or create a new resume variant (backend, full-stack, devops, computer vision, etc.). Also trigger when the user pastes or describes a job posting and asks how their resume should change, or asks which existing resume variant best fits a role. Make sure to use this skill even for small-sounding edits like "update my resume, I got a new job" or "add this project to my CV" — not just full rewrites. Always ask the user for missing achievement details, metrics, dates, or employer facts rather than inventing them.
---

# Resume Writer

## Repo context

Resumes live as JSON Resume documents in `resumes/*.json`, validated against `schema.json`. Every `.json` file in `resumes/` is a real, independently buildable resume variant — running `node index.mjs` (or `npm run build`) renders **all** of them to `output/*.pdf` via Puppeteer and the `jsonresume-theme-compact` theme (see `index.mjs`); passing a name (`node index.mjs full_stack`) builds just one. There is no "master resume" file — the four existing variants (`auxiliar_almacen_farmacia.json`, `computer_vision.json`, `data_engineer.json`, `full_stack.json`) collectively are the closest thing to a full inventory of the user's work history, and each other's best source of achievements that could be reframed for a new role.

Because layout, fonts, margins, columns, ATS-parsing structure, and visual design are entirely owned by the theme package (not by the JSON content), **ignore every tip about visual formatting, fonts, page layout, or ATS document structure** — none of that is yours to control here. Your job is purely the *content*: what goes in `basics.summary`, `work[].highlights`, `skills[]`, `projects[]`, etc., and how it's worded.

`references/guidelines.md` has the full content-tip reference this skill is built from — positioning, summary, experience, skills, projects, education, keyword tailoring, contact info, per-vacancy tailoring, common mistakes, advanced techniques, length/density, and a pre-submission checklist. The workflow below is the condensed, actionable version of it; open the reference file when you want the fuller rationale or a tip that isn't spelled out below.

## Ground rules

These override convenience every time:

1. **Never invent a fact.** A metric, employer name, date, outcome, or technology that isn't already in one of the `resumes/*.json` files or stated by the user in this conversation must be asked about, not guessed. A plausible-sounding number is worse than no number — it's the fastest way to lose credibility in an interview.
2. **Reframe, don't fabricate.** You can change emphasis, ordering, and wording for a target role, but the underlying facts (what was built, for whom, with what result) must stay true to what the user actually did.
3. **Every skill listed must be defensible in an interview.** If it's unclear whether the user has real hands-on experience with something (vs. having seen it once), ask rather than assume.

## Workflow

### 1. Identify the task

- **Editing an existing file** (new job, new project, promotion, correction) → find which `resumes/*.json` it belongs in. If the change is relevant to the user's professional story generally (e.g. a new job), consider whether it should also be reflected in *other* variants that cover overlapping history — ask the user if unsure.
- **Creating a new variant for a role/job posting** → ask the user which existing variant is the closest starting point (look at the role titles and content yourself first and suggest one), then copy it as the base. While tailoring, also look across the *other* variants for achievements, projects, or skills that are more relevant to this new target role than what's in the base file — pull them in and reframe them, since they're true facts about the same person, just differently emphasized.
- **Given a job posting or description** → before writing, extract: the 4-5 most important requirements, the explicit technology/tool names mentioned, and the underlying business problem the role is meant to solve. These drive what gets emphasized and which keywords get woven into the summary and highlights (naturally — never as a stuffed keyword list, see tip in `references/toolkit.md`).

### 2. Gather missing information — ask, don't guess

Read the relevant existing variant(s) first. Then, before writing anything new, check whether you actually have what you need for each new or changed bullet:

- A concrete **outcome or metric** for the achievement (if genuinely unmeasured, a qualitative scope indicator is fine — but ask whether one exists before assuming there isn't one)
- The **technologies actually used**, not just the general domain
- **Dates** (start/end, even approximate)
- **Employer/project name** and what the company/product does, if not obvious
- The **user's actual role** in it (sole owner vs. contributor vs. team effort)

Ask in one batch where possible rather than drip-feeding questions. It's fine to propose a draft bullet with a placeholder like `[metric?]` and ask the user to fill it in, rather than blocking entirely on a back-and-forth.

### 3. Write the content

Map the guide's content principles onto the actual JSON fields:

- **`basics.summary`** — 2-4 sentences: professional title/positioning first, years of relevant experience, strongest technical specialties, one or two measurable achievements. Tailor it to the target role each time; don't reuse one generic summary across variants. Avoid generic filler ("passionate developer", "looking for opportunities") and unsupported claims ("world-class").
- **`work[].highlights`** — one bullet per accomplishment, not per task. Use the achievement formula — **Action + technical implementation + context + result** — as a starting template, not a rigid requirement every bullet must hit all four parts of. Lead with a strong action verb (see `references/toolkit.md`), avoid weak framing like "responsible for" / "helped with" / "worked on". Quantify wherever a real number or defensible scope estimate exists (see the quantification dimensions table in the toolkit). Order bullets strongest-first. Use past tense for past roles, present tense only for the current role.
- **`skills[]`** — group by meaningful category (languages, backend, cloud/infra, tools, etc.), most-relevant-to-the-target-role categories and items first. Internally weigh each skill as Core / Intermediate / Familiar (production-independent vs. comfortable vs. limited exposure) to decide prominence and `level`, even though those exact labels don't need to appear in the JSON. Never pad the list with everything the user has ever touched — ties back to ground rule 3.
- **`projects[]`** — prefer fewer, substantial projects that show real engineering decisions over a long list of trivial ones. Describe the problem solved and the interesting technical challenge, not just a tech-stack tag list.
- **`work`/`education`/`awards`** ordering — reverse chronological, most relevant near the top; this repo's schema order already reflects that convention in existing files, so follow it.
- Weave the job posting's real keywords/technologies into summary and highlights naturally (in context, not as a bare list) when the user genuinely has that experience — never add a keyword the user can't back up.
- Keep every bullet earning its place: cut anything that doesn't support the target positioning, rather than keeping it just to fill space.

### 4. Make the edit

- Match `schema.json` field names and the structure already used in sibling files exactly.
- Update `meta.lastModified` to today's date.
- For a new variant, name the file in the same snake_case, role-describing style as the existing ones (`computer_vision.json`, `full_stack.json`, `data_engineer.json`) — not the person's name.
- Keep dates, date formats, and structure consistent with the rest of the file and with sibling resumes.

### 5. Build and verify

After editing, confirm the JSON actually renders:

```
node index.mjs <filename-without-.json>
```

This builds just that one resume to `output/<filename>.pdf`. Report the output path, and flag any render/build error rather than assuming it worked.

### 6. Score length against the guide's table

The guide ties recommended page count to years of experience (student/0-3yr → 1 page, 3-7yr → 1-2, 7-12yr → 2, 12+yr → 2-3). Run the bundled scorer to check the built PDF against that table and to catch a common side-effect of editing: a resume that spills a line or two onto an otherwise-empty extra page.

```
python3 .claude/skills/resume-writer/scripts/score_resume.py <filename-without-.json>
```

It builds the resume (unless `--skip-build` is passed and the PDF already exists), reads `pages` from `pdfinfo`, computes years of experience from the earliest `work[].startDate` to the latest `endDate` (or today if ongoing), and renders the last page to measure how far down the content actually goes (`last_page_occupancy_pct`). Requires `pdfinfo`/`pdftoppm` (poppler/xpdf tools) and Python's Pillow — both are already present in this environment.

Read `could_likely_shrink_a_page` in the output: if the resume runs to N pages but the last page is mostly blank (default threshold 40% occupancy), that's a sign some earlier section can be tightened to reclaim a page, not that the content is actually dense enough to need N pages.

When trimming to reclaim a page, follow the guide's length-and-density rules rather than just cutting until it fits:

- Don't artificially fill a page that doesn't need it, and don't remove a genuinely valuable achievement just to force-fit one page — length should follow content, not the other way around.
- Look for repeated information first (the same accomplishment restated in two places) before cutting anything new.
- When something has to go, prioritize by relevance to the resume's target role, not recency — a less relevant recent bullet can go before a more relevant older one.
- Prefer tightening wording to raise information density (cut words, not substance) over deleting whole bullets, if that's enough to close the gap.
- Remove obsolete technologies or projects that no longer support the current positioning rather than thinning every bullet a little.
- Re-run the scorer after trimming — don't assume a page was actually saved.

### 7. Before calling it done

Quick content-only pass (visual/ATS-layout items are out of scope here, see Repo context):

- Does the summary's positioning match the target role?
- Is the strongest achievement first, in each experience entry you touched?
- Is every new bullet an accomplishment, not a restated responsibility?
- Is every number either real or explicitly confirmed by the user as a defensible estimate?
- Is everything newly listed something the user could speak to in an interview?
- Did you avoid introducing any fact that wasn't already in a resume file or given by the user?

See `references/toolkit.md` for the action-verb table, quantification dimensions, and weak-vs-strong examples to pull from while drafting, and `references/guidelines.md` for the complete tip reference behind this workflow.
