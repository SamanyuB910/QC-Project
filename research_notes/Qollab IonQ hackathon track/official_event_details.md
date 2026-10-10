# Official Event Details: Georgia Tech Qiskit Fall Fest 2026 and the Qollab × IonQ Hackathon Track (qhackathon-gt.lovable.app)

Research date: 2026-10-07 (a Wednesday). All "days away" figures count from 2026-10-07.

Method note: the lovable.app site is server-side rendered, so the full page text was in the HTML (fetched with curl on 2026-10-07). The JS bundles (`/assets/routes-DgnzXnGM.js`, `/assets/SiteHeader-CXf-G3de.js`) were also checked for links and strings that do not render, which is how the Google Form registration link was found. The Qollab pages (qollab.xyz) are also server-rendered and were read directly. LinkedIn content came through a fetch-and-summarize tool and was not read verbatim, so treat it as lower confidence. Longer passages are closely paraphrased here; short rule statements are given near-verbatim. Each source URL has the exact wording.

---

## 1. Who organizes it, what is the host institution, when and where is it, and what is the full schedule?

### Takeaway
The event is **Georgia Tech Qiskit Fall Fest 2026**, run by the Georgia Tech quantum computing student club. The club calls itself "Quantum Computing @ GT" and also "Quantum Computing Association" or QCA. "GT" is confirmed as Georgia Institute of Technology in Atlanta by the site itself, by IBM's official Fall Fest directory, and by Qollab's node list. Fall Fest runs **October 1–16, 2026** in a hybrid format, with most sessions online. Inside it, the **Qollab × IonQ 48-hour online hackathon** runs **Fri Oct 9, 7:00 PM ET to Sun Oct 11, 7:00 PM ET**. As of Oct 7, Qollab registration closes **tomorrow, Thu Oct 8 at 11:00 AM ET**.

### Cited Findings

**Organizer and host institution (GT verified, not assumed)**
- The page title reads "Georgia Tech Qiskit Fall Fest 2026 | Quantum Computing @ GT". The meta description calls the event the "Georgia Tech Qiskit Fall Fest and Qollab × IonQ hackathon". The schema.org JSON-LD lists the organizer as the organization "Quantum Computing @ GT", linked to linkedin.com/company/georgiatech-quantum, and the location as "Georgia Institute of Technology, Atlanta, GA, US". — [GT Fall Fest site](https://qhackathon-gt.lovable.app/)
- The "Event organiser" block describes Quantum Computing @ GT as the quantum computing student association at the Georgia Institute of Technology, which runs workshops, talks and hackathons. The footer reads "Quantum Computing Student Association at Georgia Institute of Technology" and "© 2026 Quantum Computing @ GT". — [GT Fall Fest site](https://qhackathon-gt.lovable.app/)
- The Participant Terms & Conditions name the organizer as the "Quantum Computing Association" and call the event a "student-focused quantum computing hackathon". The Code of Conduct names "The Quantum Computing Association at Georgia Tech". — [Terms & Conditions](https://qhackathon-gt.lovable.app/terms-and-conditions); [Code of Conduct](https://qhackathon-gt.lovable.app/code-of-conduct)
- The "Event partners" block lists "IBM & IonQ". — [GT Fall Fest site](https://qhackathon-gt.lovable.app/)
- IBM's official Qiskit Fall Fest event directory has an entry for "Georgia Institute of Technology", location Georgia, United States. It links to https://qhackathon-gt.lovable.app/, gives a start date of 2026-10-08T22:30Z (6:30 PM ET Oct 8), and is tagged "Club members", "Public", "University students", "In person & virtual". This confirms the site is IBM's registered Georgia Tech Fall Fest host page. — [IBM Fall Fest events directory](https://www.ibm.com/quantum/events/fall-fest-2026) (record found in the page's embedded data; the page's `<title>` still says "Fall Fest 2025")
- Qollab's hackathon node list includes "Georgia Tech" (Atlanta, United States). Qollab's front-end data lists the participating entity "Quantum Computing Association" (id `gtqca`) under the georgia-tech node. Note that the "Quantum Computing Student Association" in Qollab's list belongs to UCLA, not Georgia Tech. — [Qollab hackathon page](https://qollab.xyz/programs/hackathon)
- The LinkedIn page "Quantum Computing @ GT" (about 339 followers, Atlanta) gives its website as gatechquantum.com and describes itself as providing resources for students entering quantum computing research and industry. — [LinkedIn: georgiatech-quantum](https://www.linkedin.com/company/georgiatech-quantum/) (via summarizer)
- gatechquantum.com is a minimal page headed "Welcome to the Quantum Computing Association at Georgia Tech" (domain label gatechqca.com), with tabs "Intro To QC", "Speakers", "Resources", "QCA @ GT". — [gatechquantum.com](https://www.gatechquantum.com)
- A Georgia Tech College of Computing listing from 2023 describes QCA as Georgia Tech's combined undergraduate and graduate quantum computing club, with weekly meetings and IBMQ programming sessions. — [GT CoC event listing](https://www.cc.gatech.edu/events/2023/05/11/gt-quantum-computing-association-weekly-meeting) (via search summary)

**Format and location**
- The hero line reads "Online and in person at Georgia Tech". The schedule note says all times are Eastern Time (Atlanta), most sessions will be online, and joining links and in-person locations will be added as they are confirmed. Many sessions are still "To be announced" for location. — [GT site schedule](https://qhackathon-gt.lovable.app/#schedule)
- The JSON-LD lists eventAttendanceMode = MixedEventAttendanceMode (hybrid). — [GT Fall Fest site](https://qhackathon-gt.lovable.app/)
- The Qollab × IonQ hackathon itself is online: Qollab's FAQ says it runs virtually over 48 hours, and university nodes may plan in-person events at their discretion, such as sharing local results or demoing projects. — [Qollab How it works FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)

**Key dates (GT site "At a glance / Key dates") with status as of 2026-10-07**

| Date (2026, ET) | Event | Status vs. Oct 7 |
|---|---|---|
| Mon Sep 28, 11:00 AM | Qollab registration opens | PAST (9 days ago) |
| Tue Sep 29, 1:00 PM | Optional AMA with the Qollab hackathon committee (Qollab site only) | PAST |
| Thu Oct 1, 7:00 PM | Fall Fest begins | PAST (6 days ago) |
| **Thu Oct 8, 11:00 AM** | **Qollab registration closes** | **UPCOMING: tomorrow (1 day; under 24 h depending on current time)** |
| **Fri Oct 9, 7:00 PM** | **Qollab × IonQ hackathon begins** | **UPCOMING: 2 days** |
| **Sun Oct 11, 7:00 PM** | **Qollab × IonQ submissions close** | **UPCOMING: 4 days** |
| Fri Oct 16, 4:00 PM | Georgia Tech Demo Day | UPCOMING: 9 days |
— [GT site key dates](https://qhackathon-gt.lovable.app/#key-dates); AMA from [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works)

**Full schedule (GT site "Schedule" table; all ET)**

| Date | Time | Session | Track | Attendance / notes | Status |
|---|---|---|---|---|---|
| Sep 28 | 11:00 AM | Qollab × IonQ registration opens | Qollab × IonQ | Online through Qollab. Complete the GT form, then the separate Qollab registration | Past |
| Oct 1 | 7:00–8:00 PM | Fall Fest introduction and beginner notebook (IBM's "Sample, Then Diagonalize" notebook) | IBM / BasQ | TBA | Past |
| Oct 8 | 11:00 AM | Qollab registration closes | Qollab × IonQ | Online through Qollab. This is the Qollab deadline, not a common GT registration deadline | 1 day |
| Oct 8 | 5:45–8:00 PM | Basque Quantum Challenge: introduction to BasQ materials and its three challenges | IBM / BasQ | TBA | 1 day |
| Oct 8 | 7:00 PM | Guest session with James Weaver, IBM Quantum: Qiskit ecosystem, Fall Fest notebooks, hackathon project guidance, live Q&A | IBM / BasQ | Virtual | 1 day |
| Oct 9 | 6:00 PM | Intermediate notebook (IBM's "Molecules as Bitstrings") | IBM / BasQ | TBA | 2 days |
| Oct 9 | 7:00 PM | Qollab × IonQ hackathon kickoff: the official 48-hour project competition begins | Qollab × IonQ | Online through Qollab | 2 days |
| Oct 9 | 8:00 PM | James Weaver, IBM Quantum: brief intro to quantum computing and Qiskit | IBM / BasQ | Virtual | 2 days |
| Oct 10 | TBA | Advanced notebook ("The Full SQD Pipeline") and project work | General | TBA | 3 days |
| Oct 11 | 7:00 PM | Qollab × IonQ submission deadline: all projects must be submitted by then | Qollab × IonQ | Submit online through Qollab | 4 days |
| Week of Oct 12 | TBA | Local judging: eligible GT projects reviewed using the official judging criteria | Qollab × IonQ | No participant attendance required | ~5–9 days |
| Oct 16 | 4:00–6:00 PM | Georgia Tech Demo Day: project presentations and GT recognition, explicitly not the submission deadline | General | TBA | 9 days |
| Week of Oct 19 | TBA | Qollab global winners announced, separately from GT Demo Day | Qollab × IonQ | Online announcement | ~12–16 days |
— [GT site schedule](https://qhackathon-gt.lovable.app/#schedule); times cross-checked against the site's Google Calendar links (e.g., hackathon window 20261009T230000Z–20261011T230000Z = 7 PM EDT to 7 PM EDT; Demo Day 20:00–22:00Z = 4–6 PM EDT)

- The site's callout says the submission deadline is October 11 at 7:00 PM ET, and that Demo Day on October 16 is a presentation event, not the submission deadline. — [GT site](https://qhackathon-gt.lovable.app/#schedule)
- The site also says challenge themes and problem statements will be shared before the hackathon begins, following each sponsor's release schedule, and that materials will be linked there as they become available. — [GT site](https://qhackathon-gt.lovable.app/#schedule)
- Qollab's official timeline matches: registration opens Sep 28 11:00 ET; optional AMA Sep 29 13:00 ET; registration closes Oct 8 11:00 ET; build window Oct 9 19:00 ET to Oct 11 19:00 ET (the submission deadline); local judging complete week of Oct 12; global judging complete and global and local winners announced week of Oct 19. — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms); [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works)
- Mentor live windows are on Oct 10–11, with async help in the event Slack. — [Qollab Mentors](https://qollab.xyz/programs/hackathon/mentors)

**Registration process (GT + Qollab)**
- Step 1 (everyone): complete the Georgia Tech registration form to reserve a spot and receive event correspondence. The site gates this behind a checkbox, "I have read and agree to the Code of Conduct and Participant Terms & Conditions", then a "Continue to registration" button that opens https://forms.gle/CidJNXfkszjCYijR7. — [GT site #register](https://qhackathon-gt.lovable.app/#register) (link found in `/assets/routes-DgnzXnGM.js`)
- Step 2 (Qollab × IonQ only): you must also register on Qollab. The site says completing the GT form does not register you for the partner competition. Both are due by Oct 8, 11:00 AM ET. — [GT site](https://qhackathon-gt.lovable.app/#register)
- The GT Google Form ("Registration Form", "Welcome to the Qiskit Fall Fest 2026") has 7 pages. Page 1 asks for: Full Name (required), Preferred Name, Email (required), Phone (optional), Institute/Org affiliation (required), Current role (Student/Employed/Founder/Other, required), GT Email if GT student (optional), Major/Field (required), Expected graduation month/year (required), LinkedIn (required), GitHub (required). Pages 2–7 were not viewed, and nothing was submitted. — [GT registration Google Form](https://forms.gle/CidJNXfkszjCYijR7)
- Qollab registration mechanics: one person registers the team as captain, giving the team name, node, track (student/professional) and up to three teammates; to compete solo, register a team of one. Teammates sign in to Qollab with the email the captain entered and accept on the registration page; no email is sent to them. Each person can be on only one team. Captains may withdraw and re-register until Oct 8 11:00 ET; after that, changes go to hello@qollab.xyz. — [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works)
- Attendee check-in: Fall Fest session attendees must complete the "required IBM attendee check-in" through a QR code or ibm.biz/IBMQFF26. — [GT site #attendee-info](https://qhackathon-gt.lovable.app/#attendee-info)
- A separate "Get event updates" sign-up form (Name, Email, optional question) collects people who want locations, joining links and schedule updates. It writes to a Supabase backend. — [GT site](https://qhackathon-gt.lovable.app/)

**Contact info and channels**
- The footer says accommodation requests and questions go to the organizing team through LinkedIn (linkedin.com/company/georgiatech-quantum). The footer's "Instagram" and "Discord" links are placeholders (`href="#"`), so no Discord or Instagram URL is published. — [GT site](https://qhackathon-gt.lovable.app/) (verified in `SiteHeader-CXf-G3de.js`)
- The Code of Conduct reporting email and the T&C accessibility contact both read "To be announced". — [Code of Conduct](https://qhackathon-gt.lovable.app/code-of-conduct); [T&C §11](https://qhackathon-gt.lovable.app/terms-and-conditions)
- Qollab-side contacts: hello@qollab.xyz (general, team changes, disqualification appeals) and privacy@qollab.xyz. After registration, the local organizing team invites participants to a node Slack channel, and there is a global support Slack channel for platform, submission or hardware questions. — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)

### Inferences
- "Quantum Computing @ GT", "Quantum Computing Association (QCA) at Georgia Tech" and "Quantum Computing Student Association at Georgia Institute of Technology" appear to be names for the same Georgia Tech student club. It is a student org and not an official university department; no Georgia Tech institutional news page about the event was found.
- The Qollab registration deadline (Oct 8, 11:00 AM ET) is the critical near-term action item. Anyone not registered on Qollab by then cannot enter the prize-bearing track.
- The GT form has no stated closing date ("This is the Qollab deadline, not a common Georgia Tech registration deadline"), but Qollab × IonQ participants need both registrations done by Oct 8.

### Gaps
- **Conflicting dates and earlier versions.** A LinkedIn post (read via summarizer, posted about Oct 5) reportedly gave the Qollab registration close as "Tuesday, October 6, 11:00 ET" and IBM Qiskit Fall Fest as "October 8–11". A Sep 7 Quantum Zeitgeist article also said Oct 6 and put the AMA in the week of Oct 5. The current official GT and Qollab pages both say **Oct 8, 11:00 ET** and Sep 29 for the AMA. The deadline was likely extended or revised; treat the official pages as authoritative, but this is unverified. — [LinkedIn](https://www.linkedin.com/company/georgiatech-quantum/); [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/)
- The GT T&C gives "Event dates October 9–11, 2026", while the homepage says Fall Fest runs October 1–16. IBM's directory lists a start of Oct 8 at 6:30 PM ET. The window depends on which document you read.
- The schedule lists two James Weaver sessions: Oct 8 at 7:00 PM ET, which overlaps the 5:45–8:00 PM BasQ session, and Oct 9 at 8:00 PM ET. It is unclear whether both will happen or one is a leftover from a reschedule.
- No in-person venue (building or room) has been published for any session. Most locations are "To be announced".
- The code of conduct reporting email, accessibility contact, Discord and Instagram links are all unpublished.
- A LinkedIn post (via summarizer) mentions a Sept 3 interest meeting (6–7 PM, Room 1232, U.A. Whitaker Bldg). No organizer names or team roster are on the event site.

---

## 2. What tracks exist, and what exactly does the site say about the Qollab × IonQ track?

### Takeaway
There are two tracks. **Track 01, IBM Qiskit / BasQ** offers guided IBM notebooks, the Basque Quantum Challenge, speaker sessions and Demo Day, with no guaranteed monetary prize. **Track 02, Qollab × IonQ** is a 48-hour online project competition using Qiskit on IonQ's quantum simulator, run through the Georgia Tech node of Qollab's global distributed hackathon. It is governed entirely by Qollab's official rules, has three themes (Quantum Impact, Quantum Playground, Quantum Unlocked), and offers up to US$10,000 cash plus compute credits.

### Cited Findings

**Track 01: IBM Qiskit / BasQ (GT site card, near-verbatim)**
- Activities and format: guided Qiskit notebooks, BasQ challenges, a virtual speaker session, project work, and Demo Day.
- Experience needed: no prior quantum experience; sessions progress from beginner to advanced material.
- Team requirements: no additional team requirement has been confirmed for this track.
- Awards or recognition: no guaranteed monetary prize; any additional recognition will be announced by the organisers.
- Additional registration: none beyond the common GT Fall Fest registration. The card links to the "Official Qiskit Fall Fest 2026" page (ibm.com/quantum/events/fall-fest-2026).
— [GT site #tracks](https://qhackathon-gt.lovable.app/#tracks)
- Notebooks named on the schedule: "Sample, Then Diagonalize" (beginner, Oct 1), "Molecules as Bitstrings" (intermediate, Oct 9), "The Full SQD Pipeline" (advanced, Oct 10). BasQ = the "Basque Quantum Challenge", with "three challenges" (Oct 8). — [GT site schedule](https://qhackathon-gt.lovable.app/#schedule)
- The T&C say recognition for the Georgia Tech/Qiskit track may include participation or completion certificates, project recognition and other non-monetary awards. — [T&C §3.1](https://qhackathon-gt.lovable.app/terms-and-conditions)

**Track 02: Qollab × IonQ (GT site card, near-verbatim)**
- Activities and format: "A 48-hour project competition using Qiskit on IonQ's quantum simulator."
- Experience needed: all experience levels are welcome; choose from Quantum Impact, Quantum Playground or Quantum Unlocked "when themes are released."
- Team requirements: "Work solo or in a team of up to four through the Georgia Tech node."
- Awards or recognition: global, specialty and conditional local Qollab awards (detailed in section 5).
- Additional registration: complete both the GT form and the official Qollab registration by October 8 at 11:00 AM ET.
— [GT site #tracks](https://qhackathon-gt.lovable.app/#tracks)
- The GT site's "Participation checklist" (verbatim items):
  1. Work solo or in a team of up to four
  2. Participate through the Georgia Tech node
  3. Create the project during the official hackathon window
  4. Publish a runnable project on Qollab
  5. Use Qiskit on IonQ's quantum simulator
  6. Release the project under the MIT License
  The checklist links to "Full Qollab participation rules" (qollab.xyz/programs/hackathon/terms). — [GT site #tracks](https://qhackathon-gt.lovable.app/#tracks)
- The hero banner says you can compete for up to US$10,000 in cash, plus compute credits, through the Qollab × IonQ track. — [GT site](https://qhackathon-gt.lovable.app/)
- The GT T&C (calling it the "IONQ/Qollab Track") say the track is governed by Qollab's official rules and terms. All monetary prizes, hardware credits, merchandise and other awards are provided and administered by the partner, not provided or guaranteed by the Quantum Computing Association. QCA does not determine prize amounts, eligibility, selection, distribution, taxation or fulfillment. Where a requirement concerns the IONQ/Qollab competition, Qollab's rules govern. — [T&C §3.2, §4](https://qhackathon-gt.lovable.app/terms-and-conditions)

**The global event the track feeds into (Qollab official pages)**
- Qollab bills the event as the "QOLLAB | IONQ — Global quantum hackathon" and "Quantum's biggest build weekend". It says Qollab, IonQ and partners are organizing the largest distributed global quantum hackathon: a 48-hour race starting October 9 to build open-source quantum projects. The footer tagline reads "48H · OCT 09–11 ET · EVERYWHERE · IN PARTNERSHIP WITH IONQ". — [Qollab hackathon](https://qollab.xyz/programs/hackathon)
- Qollab says every location runs the same 48 hours and the same rubric, and judging starts at the local node before top projects go to the global panel. It currently lists "24 nodes · 25 locations · 10 countries", including UCLA, Georgia Tech, Colorado School of Mines, SJSU, FIU, CMU, NYU Tandon, Dartmouth, Toronto, Sherbrooke, Waterloo, Aalto, Barcelona and IIIT Dharwad. A Sep 7 article reported 21 nodes, so the count grew. — [Qollab hackathon](https://qollab.xyz/programs/hackathon); [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/)
- Qollab's official theme definitions, closely paraphrased (the GT site only names them):
  - **Quantum Impact**: solve real-world problems with quantum plus classical computing. Take on a real challenge in logistics, manufacturing, space, finance, energy or another industry using a hybrid quantum-classical approach. Choose a relevant public dataset, build a strong classical baseline, identify where a quantum subroutine makes a difference, and show measurable gains such as solution quality, efficiency or accuracy.
  - **Quantum Playground**: use quantum computing to build something playful, artistic or unexpected, such as a game, music, art or an interactive experience. Superposition, interference, entanglement or measurement must be essential to the piece, beyond simply generating randomness.
  - **Quantum Unlocked**: make the hardest ideas in quantum computing click. Pick a timely topic such as error correction, fault tolerance, quantum networking or algorithms, and teach it through an interactive demo, game, animation, visualization or GUI.
  - Projects outside all three themes are still eligible for placement (1st/2nd/3rd) and node-level prizes, but not for theme specialty awards.
  — [Qollab Rules & terms: Themes](https://qollab.xyz/programs/hackathon/terms)
- Theme choice: registration asks which theme you are leaning toward, but the answer is optional and non-binding. You declare a project's theme at submission and can change it until the Oct 11 deadline. — [Qollab How it works FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- Problem statements: the GT site says challenge themes and problem statements will be shared before the hackathon following sponsors' release schedules. As of Oct 7, the Qollab rules page already contains the three theme briefs above. No additional IonQ-specific problem statement was found. — [GT site](https://qhackathon-gt.lovable.app/#schedule); [Qollab terms](https://qollab.xyz/programs/hackathon/terms)

**Resources provided (Qollab × IonQ)**
- Qollab's free simulators, including IonQ's quantum simulator, run in the browser on Qollab. — [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works)
- Primer: Qollab's "Programming your first quantum circuits" course gets you to a running circuit on the IonQ simulator in six short lessons. — [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works)
- Mentors are recruited by Qollab and IonQ: researchers, engineers and graduate students covering areas such as QAOA and variational methods, error mitigation, chemistry, finance, optimization and tooling. Each gives at least two one-hour live windows on Oct 10–11 plus optional async Slack help, and teams pick mentors by area from a mentor schedule. — [Qollab Mentors](https://qollab.xyz/programs/hackathon/mentors)
- Communication is on Slack: a node channel for local logistics and a global support channel. — [Qollab How it works FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- Platform constraints: local simulators accept any number of jobs per run, but IonQ backends accept one job per run, so everything an IonQ run measures must go in one circuit. Nothing persists between runs, so ship saved states as project files. Network access is limited to GET requests to CORS-enabled servers. Keep API keys out of code because code is public. — [Qollab How it works FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- The GT T&C say access to quantum hardware, cloud resources and APIs is not guaranteed, and participants should not rely on a specific hardware backend as their only way to complete a project. — [T&C §16](https://qhackathon-gt.lovable.app/terms-and-conditions)
- GT-side resources: IBM notebooks, BasQ challenges and the James Weaver (IBM Quantum) sessions, including hackathon project guidance (Oct 8). — [GT site schedule](https://qhackathon-gt.lovable.app/#schedule)

### Inferences
- The GT Qollab × IonQ track is not a separate GT competition. It is the Georgia Tech node of Qollab's global hackathon, so GT participants compete locally against other GT-node entries and then globally.
- The six-item GT checklist is a condensed version of Qollab's longer submission requirements (section 3). Qollab's rules are binding where they differ.

### Gaps
- No GT-specific problem statement, IonQ-authored challenge text or GT-specific bonus prizes were found, although Qollab notes that local teams may add their own bonus prizes.
- The names of specific IonQ, Qollab or GT mentors assigned to the GT node are not published.

---

## 3. What are the rules: eligibility, team size, prior work, IP, required deliverables, code of conduct?

### Takeaway
For the Qollab × IonQ track: entrants must be 18+ and based in one of 45 eligible countries (the US included). Students and professionals are both allowed, and teams of 1–4 compete at a single node. Qiskit projects must be built during the Oct 9–11 window, though existing code, AI tools and forks are allowed if disclosed. Projects must be published and runnable on Qollab under the MIT license, with a project page, a 2–3 minute public demo video and the attribution line "This effort is supported by Qollab & IonQ". The GT Fall Fest itself is open to anyone and free, under GT's own T&C and Code of Conduct.

### Cited Findings

**Eligibility**
- GT site: "Free to join and open to anyone curious about quantum. No prior experience is required." — [GT site](https://qhackathon-gt.lovable.app/)
- GT T&C §2: participants may be affiliated with Georgia Tech or another university, organization or community, where the track permits. Participants must meet any track-specific eligibility requirements, and registration does not guarantee participation if capacity or eligibility limits apply. — [T&C](https://qhackathon-gt.lovable.app/terms-and-conditions)
- Qollab: participants must be at least 18. No prior quantum experience is needed, though some Python experience helps. Participants must be based in an eligible country: Argentina, Australia, Austria, Barbados, Belgium, Brazil, Bulgaria, Canada, Chile, Colombia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, India, Indonesia, Ireland, Israel, Italy, Japan, Latvia, Lithuania, Luxembourg, Malaysia, Malta, Mexico, Netherlands, New Zealand, Norway, Poland, Portugal, Romania, Singapore, Slovakia, South Korea, Spain, Sweden, Switzerland, the United Kingdom and the United States. Others can email hello@qollab.xyz before Oct 8. — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms); [Qollab FAQ](https://qollab.xyz/programs/hackathon)
- Qollab tracks: a **student team** requires every member to be enrolled in an undergraduate or graduate program at the node university (here, Georgia Tech). All other teams, including mixed student and professional teams, register as **professional** and still associate with a node. Everyone on a team competes at the same node; mixed-node teams are not allowed. Both tracks use the same rubric and compete for the same awards. — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)
- Qollab: enrollment at a university is not required. Professionals or students at non-participating universities choose a node, ideally the nearest one geographically or one they are affiliated with, for example as alumni. — [Qollab FAQ](https://qollab.xyz/programs/hackathon); [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)

**Team size and entries**
- The size limit is solo or up to 4 members (GT site: "solo or in a team of up to four"). — [GT site](https://qhackathon-gt.lovable.app/#tracks); [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)
- Each person may be on only one team. A team may submit up to 5 projects, each judged separately, and awards are per project. — [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works)

**Submission requirements and deliverables (Qollab official list)**
- Every project must: use the Qiskit framework; follow industry best practices on UI accessibility; run on Qollab's free simulators, including IonQ's quantum simulator; be published and runnable on Qollab.xyz under an MIT license before the deadline; have a Qollab project page covering what it does, what problem it explores, how to run it, and enough to understand, replicate or extend it; be built during the hackathon window; and include a 2–3 minute demo video at a public link that opens without sign-in. — [Qollab Rules & terms: Submission requirements](https://qollab.xyz/programs/hackathon/terms)
- On running: judges run every project on a free local simulator, and results from IonQ simulators or hardware neither add nor subtract points. A project that runs on an IonQ simulator must fit one job per run. — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms); [Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- On the demo video: a screen recording with voiceover is enough, and you do not have to appear on camera. Host it on YouTube, Loom, Vimeo or Google Drive with anyone-with-link access. — [Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- On code location: the project must be public and runnable on Qollab, where judges open the page, read the code and press Run. An external frontend or backend may support it, but that repo must be public, require no sign-in, be MIT-licensed, list its dependencies and contain no secrets. — [Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- On the submission process: the team captain submits from the Qollab registration page between Oct 9 19:00 ET and Oct 11 19:00 ET, and may edit until the deadline. After the deadline, entries can be withdrawn but not edited or added. Partial or rough projects are still eligible. — [Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- "Beyond the tutorial bar": each submission must go beyond a reference implementation or tutorial exercise and show at least one of the following: a novel application or problem context; a technical extension (e.g., noise/error mitigation, parameter optimization, comparative benchmarking); or an original analytical or educational contribution. Panels may score a submission 0 on Novelty & Creativity and Technical Execution if it fails this bar. — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)
- Slides are not listed as a required deliverable anywhere. GT Demo Day (Oct 16) is a "presentation event", but no format or slide requirement is published. — [GT site](https://qhackathon-gt.lovable.app/#schedule)

**Prior work, AI use and originality**
- Qollab: projects must be substantially new work built during the window. Using AI, open-source libraries, prior tutorials or Qollab templates as a starting point is "fine and encouraged" when disclosed, and judging is based on what the team adds. Teams must disclose on the project page what existed before the window and credit sources such as forks, templates, repos or tutorials. Disqualifying conduct includes submitting a pre-existing project as new; copying code, circuits or text without attribution; using a template without disclosure; and substantially identical submissions from multiple teams. — [Qollab Rules & terms: Originality](https://qollab.xyz/programs/hackathon/terms); [Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- GT T&C §5: previously created work may only be used where the track rules permit, and significant pre-existing components may need to be identified. §7: AI tools are allowed where track rules permit, and participants remain responsible for accuracy, originality and attribution. — [T&C](https://qhackathon-gt.lovable.app/terms-and-conditions)

**IP and licensing; participant obligations**
- GT T&C §6: participants keep ownership of IP they independently create, unless partner or platform terms say otherwise, and participation does not transfer IP to QCA. — [T&C](https://qhackathon-gt.lovable.app/terms-and-conditions)
- Qollab participant obligations: release code and documentation under the MIT license; keep projects available on Qollab for 12 months; include the attribution "This effort is supported by Qollab & IonQ"; and provide a payment method in case of a monetary award. Award winners additionally agree to let Qollab and IonQ feature their work, profile and node in PR and marketing, take sole responsibility for tax reporting, and post at least once on social media about participating. — [Qollab Rules & terms: Participant obligations](https://qollab.xyz/programs/hackathon/terms)
- Projects stay live and forkable on Qollab for at least 12 months. — [Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)

**Disputes, disqualification, force majeure**
- All scoring and award decisions are final. The only appeal is against disqualification: a written appeal to hello@qollab.xyz within 24 hours of notification, decided within 5 business days by a reviewer separate from the panel. Disqualified awards and advancement slots are withdrawn, not reassigned. Paid awards must be returned within 30 days if a disqualification happens later. — [Qollab Rules & terms: Appeals](https://qollab.xyz/programs/hackathon/terms)
- For a platform or simulator outage over 12 hours during the build window, Qollab may extend the deadline proportionally for all nodes or accept late submissions with an outage-impact statement. — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)

**Code of Conduct (GT, effective Oct 1, 2026)**
- The code applies to everyone (hackers, mentors, judges, organizers, speakers, volunteers, sponsors) in all event spaces: venues, Discord/Slack, video calls, workshops, social events and submission platforms. It expects participants to be respectful, collaborate in good faith, respect differences and respect boundaries. Unacceptable behavior is listed: harassment, discrimination, unwelcome sexual conduct, stalking, inappropriate content, slurs, doxxing, disruption, and unauthorized access to others' accounts or compute. A "Project Integrity" section requires crediting teammates and sources, no plagiarism, following rules on pre-existing work and AI, academic-integrity policies, and IP and licensing terms. Reports go to the organizers (email "To be announced") or in person to any organizer. Consequences run from a warning up to removal, disqualification, a ban from future QCA events, or referral to Georgia Tech authorities. Retaliation is prohibited. — [Code of Conduct](https://qhackathon-gt.lovable.app/code-of-conduct)
- Qollab: a standard hackathon code of conduct applies at every node. Local organizers enforce it on-site, and Qollab handles platform-level and cross-node issues. — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)

**Other GT T&C points**
- §10: the event may be photographed or recorded for promotional purposes. §12: participants are responsible for backups, deadlines and account security, and organizers are not liable for lost work. §14: QCA may change the schedule, format, deadlines and venues, communicating significant changes through official channels. §18: submitting the registration form constitutes agreement to the T&C and Code of Conduct. — [T&C](https://qhackathon-gt.lovable.app/terms-and-conditions)

### Inferences
- A GT student team in which every member is enrolled at Georgia Tech should register on Qollab as a **student** team at the Georgia Tech node. Any non-GT or professional member makes the team "professional", though it can still compete at the GT node.
- Since IonQ hardware or simulator results are not scored and judges run projects on a free local simulator, projects should run cleanly on the free simulator first, and any IonQ run should be a single circuit per run.
- Under-18 participants can join GT Fall Fest sessions but are ineligible for the Qollab × IonQ competition.

### Gaps
- The GT site states no rules on eligibility levels (undergrad, grad, high school) or age for Track 01.
- Pages 2–7 of the GT Google Form (which may contain further consent, eligibility or track questions) were not viewed.

---

## 4. What are the judging criteria and weightings, and who are the judges?

### Takeaway
Every Qollab × IonQ submission is scored on four criteria: **Novelty & Creativity, Technical Execution, Impact Potential and Documentation Quality**. Local node panels score first and top scorers go to a global panel that re-scores on the same rubric. **No numeric weightings are published.** No judges are named; the local panel includes a faculty or staff judge plus Qollab and IonQ representatives.

### Cited Findings
- Qollab says every submission is judged on the same four criteria: Novelty & creativity, Technical execution, Impact potential and Documentation quality. Local judges score first, and top scorers advance to a global panel that re-scores with the same rubric. — [Qollab How it works: Judging](https://qollab.xyz/programs/hackathon/how-it-works#judging)
- The Rules & terms describe a common rubric focused on "Novelty & Creativity, Technical Execution, Impact Potential and Documentation Quality". — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)
- Tutorial-bar rule: panels may give 0 on Novelty & Creativity and Technical Execution to submissions that do not go beyond a tutorial or reference implementation. — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)
- Judges press Run on a free simulator, and whether a project ran on hardware or a simulator is not scored. — [Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- The local round is judged by a local panel that includes a faculty or staff judge, alongside Qollab and IonQ representatives. — [Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- Local node process: with fewer than 10 projects, the panel evaluates all entries and advances the top 3 to global judging. With 10 or more, the panel gives local awards to the top 3, and all three advance. Either way, each node may advance up to one project per global specialty award (Most Novel / Creative, Best of Theme, Most Impact, Best Documentation). — [Qollab Rules & terms: Award structure](https://qollab.xyz/programs/hackathon/terms)
- GT site: local judging happens in the week of Oct 12, needs no participant attendance, and reviews eligible GT projects using the official judging criteria. — [GT site schedule](https://qhackathon-gt.lovable.app/#schedule)
- GT T&C §8: judges are expected to disclose conflicts of interest, and partner tracks may use the partner's own judging procedures. — [T&C](https://qhackathon-gt.lovable.app/terms-and-conditions)
- Scoring decisions are final, apart from disqualification appeals. — [Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- A secondary source summarizes the criteria as novelty, performance, what the work changes, and clarity of writing. — [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/)

### Inferences
- With no published weights, the four criteria should be treated as roughly co-equal. Documentation Quality is both a rubric criterion and a specialty award, so a strong Qollab project page and README have outsized value.
- GT Demo Day (Oct 16) is not part of Qollab judging; local judging is in the week of Oct 12, before Demo Day.

### Gaps
- No numeric weights, point scales or sub-criteria are published.
- No judge names (GT faculty or staff, Qollab or IonQ representatives) or global panel members are published.
- How Track 01 (IBM/BasQ) projects are judged or recognized at Demo Day is not specified.

---

## 5. What prizes exist for each track and overall?

### Takeaway
Only the Qollab × IonQ track carries monetary prizes, all paid by the partner and not GT. **Global:** 1st $10,000 + $20,000 compute; 2nd $5,000 + $15,000 compute; 3rd $2,500 + $10,000 compute. There are **six specialty awards** of $500 + $5,000 compute each. **GT local-node awards** of $500/$300/$200 + $5k/$3k/$2k compute apply only if the GT node receives at least 10 eligible submissions. Global top-3 teams also get IonQ mentorship and expedited IonQ interview access. Track 01 has no guaranteed monetary prize.

### Cited Findings
- GT site, Qollab × IonQ prizes: first place US$10,000 + US$20,000 compute credits; second US$5,000 + US$15,000; third US$2,500 + US$10,000. These apply only to the Qollab × IonQ track and are governed by the official Qollab rules. — [GT site Awards](https://qhackathon-gt.lovable.app/#tracks)
- Specialty awards: each is US$500 cash plus US$5,000 compute credits. Categories are Most Novel / Creative, Most Impact, Best Documentation, Quantum Impact, Quantum Playground and Quantum Unlocked, the last three being "Best of theme" awards. A single project can win both specialty and placement awards. — [GT site](https://qhackathon-gt.lovable.app/#tracks); [Qollab How it works: Awards](https://qollab.xyz/programs/hackathon/how-it-works)
- Georgia Tech local-node awards: if the node has **10 or more eligible submissions**, 1st/2nd/3rd receive US$500/$300/$200 cash plus US$5,000/$3,000/$2,000 compute credits. If GT has fewer than 10, the top three advance directly to global judging and no standard local cash awards apply. — [GT site](https://qhackathon-gt.lovable.app/#tracks); [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)
- Additional benefits for the global top three teams:
  - IonQ mentorship: three structured one-to-one sessions with IonQ engineers within 12 months.
  - Expedited IonQ interview access for 12 months: internship and early-career applicants skip initial screening and get a first conversation with the hiring manager, and professionals may be considered for one aligned role. Employment is not guaranteed.
  - Featured placement on Qollab.
  — [Qollab How it works: Awards](https://qollab.xyz/programs/hackathon/how-it-works)
- Qollab Fellows: Qollab may invite selected participants to be Fellows from November to April. The role pays cash and includes compute credits for research and a small grant pool. It is run by Qollab separately from IonQ's awards. — [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works)
- Discretionary extras: select teams may receive additional funds or compute at the discretion of Qollab, IonQ or sponsors, and university nodes are encouraged to add supplemental student-specific prizes. — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)
- Students and professionals compete in the same prize pools. — [Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- Track 01 (IBM Qiskit / BasQ) does not guarantee a monetary prize. Recognition may include participation or completion certificates and project recognition. — [GT site](https://qhackathon-gt.lovable.app/#tracks); [T&C §3.1](https://qhackathon-gt.lovable.app/terms-and-conditions)
- A secondary source says compute is IonQ hardware time used through the platform and has no cash equivalent. — [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/)
- The GT T&C say QCA does not provide, guarantee or determine Qollab/IonQ prizes, and winners are responsible for tax reporting. — [T&C §3.2](https://qhackathon-gt.lovable.app/terms-and-conditions); [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)

### Inferences
- For a GT team, the realistic paths are: (a) a top-3 GT local finish, which pays cash only if GT reaches 10 or more eligible submissions and advances to global either way; (b) advancement as the GT node's candidate for a specialty award; and (c) a global placement or specialty win.
- The maximum for a single project is a global placement plus one or more specialty awards. For example, 1st place plus two specialties would be $11,000 cash plus $30,000 compute.

### Gaps
- Whether GT will reach the 10-submission threshold is unknown; no registration counts are published.
- No GT-specific supplemental prizes have been announced for either track.
- The official pages do not state the form or expiry of compute credits.

---

## 6. Is there a past edition (e.g., 2025), and what happened?

### Takeaway
No evidence was found of a prior Georgia Tech Qiskit Fall Fest or a prior Qollab × IonQ global hackathon. The 2026 Qollab × IonQ event appears to be the first edition. Qollab and IonQ did collaborate earlier on Qollab's "Creative Challenge" (second annual edition, announced March 2026), which is a different program. Georgia Tech's QCA has existed since at least 2023.

### Cited Findings
- The GT event site has no references to past editions, past winners or a 2025 event. — [GT site](https://qhackathon-gt.lovable.app/)
- The LinkedIn page (via summarizer) shows no posts about a 2025 Fall Fest or earlier hackathon. Recent posts announce hosting Qiskit Fall Fest 2026 with IBM Quantum (about 2 months ago), a Sept 3 interest meeting mentioning a hackathon sponsored by IBM and IonQ, and a Fall Fest / IonQ × Qollab schedule post (about Oct 5). — [LinkedIn](https://www.linkedin.com/company/georgiatech-quantum/)
- Web searches for a Georgia Tech Qiskit Fall Fest in 2024 or 2025, or a QCA hackathon, returned no matching event pages or winners. — searches on 2026-10-07 (no source found)
- Qollab's hackathon pages are written as a new event, with no references to prior editions or past winners. — [Qollab hackathon](https://qollab.xyz/programs/hackathon)
- Earlier IonQ–Qollab collaboration: IonQ announced a partnership with Qollab's second annual "Creative Challenge" (search-result title only; not fetched). — [IonQ news](https://ionq.com/news/ionq-partners-with-qollabs-creative-challenge-advancing-creative-quantum-innovation)
- Qiskit Fall Fest context: IBM's program is a set of student-organized events on campuses in October–November. The 2026 theme celebrates "a decade of quantum on the cloud", and IBM reports more than 32,000 participants and 150 organizers in 2025. — [IBM Qiskit Fall Fest 2026 blog](https://www.ibm.com/quantum/blog/qiskit-fall-fest-2026)
- QCA has been active since at least 2023, when it held weekly meetings with IBMQ programming sessions per a GT College of Computing listing. A qBraid blog post names "Georgia Tech Quantum Computing Association" leaders Zhixin (Jack) Song and Rasmit Devkota. That post was seen only as a search snippet and its date is unverified. — [GT CoC event listing](https://www.cc.gatech.edu/events/2023/05/11/gt-quantum-computing-association-weekly-meeting); [qBraid blog](https://www.qbraid.com/blog-posts/qbraid-alliance-unites-quantum-computing-across-universities)

### Inferences
- This appears to be the first Georgia Tech Qiskit Fall Fest with a Qollab × IonQ partner track. No historical winners, judging patterns or prize-take data exist for calibration.

### Gaps
- Whether Georgia Tech hosted any earlier Qiskit Fall Fest event (2021–2025) could not be confirmed or ruled out. IBM's past host lists are paginated or dynamic and were not fully searchable.
- The current officer roster and event lead names for QCA are not on the event site. The qBraid leader names are unverified for 2026.
