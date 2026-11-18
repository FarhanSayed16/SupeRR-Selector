# P.R.I.M.E.

## Pressure Reliability & Impact Measurement Engine

### Analytical Framework, Validation Rules and Development Direction

> **Core recommendation:** Use innings phase to define a player's role
> context, and use match-state variables to measure pressure. Evaluate
> performance against a comparable baseline, then adjust for sample size
> and uncertainty.

------------------------------------------------------------------------

## 1. Executive assessment of your handwritten ideas

Your notes propose dividing T20 batting into overs 1--6, 7--15 and
16--20, then examining how batters and bowlers perform in those
situations. You also want to identify batters who handle collapses,
players who play spin or pace well under pressure, bowlers who perform
in death overs, bowlers who defend low totals, and consistent
wicket-taking bowlers with good economy.

This is a good direction because it introduces context. A powerplay
opener, a middle-order stabiliser and a death-over finisher have
different jobs. Likewise, a bowler operating in the powerplay has a
different task from one bowling at the end of an innings.

The key correction is that **innings phase is not the same as
pressure**. Overs 16--20 are often high leverage, but not every death
over is a pressure situation. A team may be comfortably ahead.
Conversely, a team can be collapsing in the 9th over. P.R.I.M.E. must
measure both dimensions separately.

## 2. Convert your ideas into a two-layer model

  -----------------------------------------------------------------------
  Layer                   What it answers         Examples
  ----------------------- ----------------------- -----------------------
  **A. Role / innings     What job was the player Powerplay 1--6; middle
  phase**                 expected to perform?    7--15; death 16--20;
                                                  batting position;
                                                  pace/spin matchup.

  **B. Match pressure**   How difficult was the   Required run rate;
                          situation at that       wickets remaining;
                          moment?                 balls remaining;
                                                  score/target context;
                                                  recent wickets;
                                                  defending a low total.
  -----------------------------------------------------------------------

The player should be compared with others who faced broadly similar
roles and situations. This avoids rewarding someone simply because they
played more easy overs or penalising someone for being assigned a
difficult role.

## 3. Recommended T20 innings phases

  ------------------------------------------------------------------------
  Phase                            Overs Batting          Bowling
                                         responsibility   responsibility
  ---------------- --------------------- ---------------- ----------------
  **Powerplay**                     1--6 Get a controlled Take early
                                         start, exploit   wickets, limit
                                         field            boundary flow,
                                         restrictions,    control extras
                                         preserve wickets and scoring
                                         where needed.    rate.

  **Middle overs**                 7--15 Build the        Control the run
                                         innings, rotate  rate, create
                                         strike, manage   pressure through
                                         spin/pace        dots, take
                                         matchups,        wickets and
                                         prepare for the  prevent
                                         finish.          acceleration.

  **Death overs**                 16--20 Convert the      Restrict
                                         platform into    scoring, execute
                                         runs, finish     plans under high
                                         strongly, or     scoring
                                         rescue a low     pressure, take
                                         total.           wickets without
                                                          excessive
                                                          extras.
  ------------------------------------------------------------------------

## 4. Batting analysis: recommended dimensions

### 4.1 Powerplay batter (overs 1--6)

-   Measure strike rate, runs per ball, boundary percentage and dot-ball
    percentage.
-   Measure dismissal frequency (balls per dismissal), not just total
    runs.
-   Separate openers from non-openers where the sample permits.
-   Identify early-wicket situations: for example, the team losing
    multiple wickets early. Define the exact collapse rule before
    ranking.

### 4.2 Middle-over batter (overs 7--15)

-   Measure strike rotation, dot-ball avoidance, boundary conversion and
    strike rate.
-   Compare performance against spin and pace separately, but only when
    bowler-type labels are reliable.
-   Assess whether the batter stabilises an innings after a wicket or
    helps maintain the scoring rate.

### 4.3 Death-over batter (overs 16--20)

-   Measure death-over strike rate, runs per ball, boundary percentage
    and dismissal frequency.
-   Distinguish finishing a strong platform from rescuing a low-scoring
    or collapsing innings.
-   Use balls faced and innings count as minimum-sample checks; a few
    high-scoring balls should not create a top ranking.

### 4.4 Batting under pressure / during a collapse

-   Create a match-state pressure label using required run rate, wickets
    remaining, balls remaining and recent wicket loss.
-   Compare the batter's output in pressure situations with their own
    comparable non-pressure baseline.
-   Report both pressure performance and the number of pressure
    balls/innings. A high score from a tiny sample is not reliable
    evidence.

**Important:** "Most runs when the team is collapsing" should not be
judged by raw runs alone. A player may score 20 valuable runs while
wickets are falling, whereas another may score 35 after the match is
already under control. Context and contribution relative to expectation
matter.

## 5. Bowling analysis: recommended dimensions

### 5.1 Powerplay bowling

-   Economy rate, dot-ball percentage, boundary-conceded percentage and
    wickets per legal ball.
-   Separate wicket-taking impact from run containment; these are
    related but not identical skills.

### 5.2 Middle-over bowling

-   Economy and dot-ball percentage, plus wickets and boundary control.
-   Compare spin and pace categories only if the dataset has a
    trustworthy bowling-style mapping.
-   Evaluate whether the bowler slows scoring or takes wickets when the
    batting side is rebuilding.

### 5.3 Death-over bowling

-   Economy rate, boundary-conceded percentage, dot-ball percentage,
    wickets per legal ball and extras per over.
-   Compare death-over results with the bowler's own baseline and with
    other bowlers in the same phase.
-   Treat yorker execution as a separate skill only if delivery-level
    yorker labels or a validated proxy exist.

### 5.4 Defending a low total

-   Define "low total" relative to competition, season, venue and
    innings conditions; do not use one universal cutoff for every match.
-   Evaluate the bowling unit and individual bowlers separately. A
    bowler's figures are affected by the other end and the fielding
    team.
-   Measure runs conceded, wickets, dot balls and extras, while
    accounting for overs bowled and the quality of the chase situation.

### 5.5 Consistency and wicket-taking

-   Use economy and wicket-taking together, but keep them as separate
    metrics before combining them.
-   Measure consistency across matches, not only across deliveries
    pooled together.
-   A bowler with one exceptional match and several poor matches should
    not automatically outrank a consistently effective bowler.

**Caution on yorkers:** Do not infer that a delivery was a yorker merely
because it produced a dot ball or a wicket. If the supplied ball-by-ball
data does not explicitly identify yorkers, present yorker skill as "not
measurable from the available fields" rather than inventing a score.

## 6. How P.R.I.M.E. should define pressure

Pressure should be calculated from information available **at the start
of each delivery**, before the outcome of that delivery is known. This
prevents data leakage: the delivery's runs or wicket must not be used to
decide whether that same delivery was under pressure.

  --------------------------------------------------------------------------
  Pressure signal         Why it matters          Implementation note
  ----------------------- ----------------------- --------------------------
  **Required run rate /   A rising required rate  Use target and runs
  chase difficulty**      can increase batting    remaining divided by legal
                          urgency.                balls remaining; handle
                                                  revised targets and zero
                                                  balls safely.

  **Wickets remaining**   Few wickets left reduce Calculate from wickets
                          batting resources and   lost before the delivery.
                          increase collapse risk. 

  **Balls remaining /     The same score has      Keep phase as a separate
  innings stage**         different meaning early feature; do not use phase
                          and late.               alone as pressure.

  **Recent wicket         Consecutive or closely  Define a reproducible
  cluster**               spaced wickets can      rolling window and
                          indicate a collapse.    threshold; test
                                                  sensitivity.

  **Defending a low       The bowling side may be Define low relative to
  total**                 under pressure despite  competition/season/venue
                          a modest chase target.  and chase conditions.
  --------------------------------------------------------------------------

Recommended first version: create a transparent pressure score from
normalised match-state features, then test whether the score separates
situations that cricket analysts would reasonably regard as low, medium
and high pressure. Do not select weights only because they look
intuitive. Document the weights, test alternative weights and show how
rankings change.

For the chase, required run rate is a useful signal. For the first
innings, there is no chase required rate, so use a separate
first-innings pressure model based on wickets, balls, score relative to
a competition/venue/season par expectation, and recent wicket loss. Do
not force the chase formula onto first-innings data.

## 7. Metrics and fair comparisons

Use a metric set rather than a single raw statistic.

  -----------------------------------------------------------------------
  Player type             Core metrics            Contextual comparison
  ----------------------- ----------------------- -----------------------
  **Batters**             Runs per 100 balls      Compare by phase,
                          (strike rate); balls    batting role, pressure
                          per dismissal;          band, competition and
                          boundary%; dot-ball%;   season.
                          pressure vs baseline    
                          change.                 

  **Bowlers**             Runs conceded per 6     Compare by phase,
                          legal balls (economy);  pressure band, bowling
                          wickets per legal ball; role/type if available,
                          dot-ball%; boundary     competition and season.
                          conceded%; extras.      
  -----------------------------------------------------------------------

Use legal-ball counts correctly. Wides and no-balls affect runs and may
not count as legal balls; validate the supplied extras columns before
calculating overs or economy. Do not treat an extras-type code as an
actual number of runs. Also distinguish bowler-credited wickets from
run-outs and other dismissals not credited to the bowler.

## 8. Baseline and scoring approach

1.  Build a baseline for each competition/season and role-phase group.
    Keep IPL and T20I separate during initial analysis.
2.  For every player, calculate their performance in pressure
    deliveries/innings and in comparable non-pressure situations.
3.  Calculate a pressure-versus-baseline difference for each metric.
    Orient the metrics so that higher always means better before
    combining them.
4.  Standardise metrics within appropriate comparison groups so that one
    metric's scale does not dominate the score.
5.  Combine the standardised measures into separate batter and bowler
    scores. Do not use one common formula for both roles.
6.  Apply a reliability adjustment based on sample size, and publish the
    unadjusted score, adjusted score and sample count.
7.  Test rankings under alternative reasonable pressure thresholds and
    weights. Highlight players whose positions are unstable.

A simple reliability shrinkage concept is:

\[ `\text{Adjusted Score}`{=tex} = `\text{Group Baseline}`{=tex} +
`\text{Reliability}`{=tex}`\times`{=tex}(`\text{Player Score}`{=tex}-`\text{Group Baseline}`{=tex})
\]

where:

\[ `\text{Reliability}`{=tex} = `\frac{n}{n+k}`{=tex} \]

Here, (n) is the relevant sample size and (k) is a tuning constant
selected and justified using validation. This pulls small-sample results
towards the group baseline rather than treating them as certain.

Do not lock in arbitrary weights at the beginning. Start with
transparent candidate weights, run sensitivity analysis, and retain a
weighting scheme only if it produces defensible and stable results.

## 9. Dataset checks required before implementation

-   Confirm which competitions and seasons are actually present in
    `competitions.csv`; the challenge brief describes IPL and T20I data
    from 2022 onwards, but the CSV contents must establish the actual
    coverage.
-   Check `match_id` joins between `ball_by_ball` and `matches`, and
    `comp_id` joins to `competitions`.
-   Validate innings numbering, Super Overs, abandoned matches,
    incomplete innings and revised targets.
-   Inspect the meaning of every extras field. The preliminary
    inspection suggested `extras1_runs` may be a category/code field
    rather than a numeric run count; verify before using it.
-   Validate legal-ball logic, total runs, batter runs, bowler-conceded
    runs and wicket attribution against known match totals.
-   Check whether bowling style (spin/pace), yorker type, delivery
    length/line and fielding context are actually present. Do not assume
    they are.
-   Use actual participation records carefully; a player listed in a
    playing-eleven file may have a participation flag that needs
    filtering.
-   Check player identity mapping across competitions and teams so the
    same player is not accidentally split into multiple identities or
    merged with another player.
-   Record missing values, duplicate deliveries, unusual innings and
    matches with incomplete ball-by-ball coverage.

The current project pack contains six CSV datasets and no separate
standalone players table. Player identity and competition/team
associations therefore need to be assembled from the supplied mapping
and participation tables, with join keys validated.

## 10. Recommended development workflow

1.  **Step 1 --- Data audit:** Run the exploration notebook. Produce
    schema, missing-value, category, duplicate and join-coverage
    reports.
2.  **Step 2 --- Cricket data validation:** Reconcile selected matches'
    innings totals, legal balls, extras and wickets against match
    scorecards or trusted totals.
3.  **Step 3 --- Build delivery state:** For every delivery, calculate
    pre-delivery score, wickets lost, legal balls remaining, target/runs
    remaining where applicable, required rate and phase.
4.  **Step 4 --- Define pressure labels:** Create first-innings and
    chase pressure models separately. Start with interpretable
    low/medium/high bands.
5.  **Step 5 --- Create role-phase metrics:** Build batting and bowling
    tables split by phase, pressure band and competition.
6.  **Step 6 --- Compare with baseline:** Calculate pressure performance
    relative to comparable non-pressure performance and relevant group
    baselines.
7.  **Step 7 --- Reliability and ranking:** Apply minimum sample rules,
    reliability shrinkage, uncertainty intervals and sensitivity checks.
8.  **Step 8 --- Evidence and dashboard:** Show rankings with sample
    size, pressure opportunities, baseline, pressure performance,
    adjusted score and caveats.
9.  **Step 9 --- Methodology report:** Explain definitions, exclusions,
    calculations, limitations and why the final top 10 are defensible.

## 11. What to retain, modify or postpone from your notes

  ---------------------------------------------------------------------------
  Your idea               Decision                Recommended treatment
  ----------------------- ----------------------- ---------------------------
  Overs 1--6 / 7--15 /    **KEEP**                Use as the standard phase
  16--20                                          segmentation, with
                                                  phase-aware role
                                                  comparisons.

  Batters who score while **KEEP + DEFINE**       Define collapse using
  the team is collapsing                          pre-delivery wickets lost
                                                  and recent wicket cluster;
                                                  compare against baseline.

  Performance against     **KEEP IF DATA SUPPORTS Requires reliable
  spin and pace under     IT**                    bowler-type labels and
  pressure                                        enough sample in each
                                                  subgroup.

  Spinners performing in  **KEEP AS A             Interesting specialist
  death overs             SUB-ANALYSIS**          view, but enforce sample
                                                  thresholds and avoid
                                                  over-ranking tiny samples.

  Good start while        **REFINE**              Define low total relative
  defending a low total                           to
                                                  competition/season/venue;
                                                  evaluate the bowler and
                                                  team context separately.

  Good economy plus       **KEEP, BUT SEPARATE    Show economy and
  wickets                 FIRST**                 wicket-taking independently
                                                  before creating a combined
                                                  score.

  Yorkers in death overs  **POSTPONE UNLESS LABEL Do not infer yorkers from
                          EXISTS**                outcomes. Need
                                                  delivery-type data or a
                                                  validated annotation
                                                  source.

  Most consistent players **KEEP**                Measure match-to-match
                                                  variation and reliability,
                                                  not just aggregate totals.
  ---------------------------------------------------------------------------

## 12. Final recommended P.R.I.M.E. output

-   Top 10 batters and top 10 bowlers, each with a separate scoring
    model.
-   Role/phase breakdown: powerplay, middle overs and death overs.
-   Pressure breakdown: low, medium and high pressure, with clear
    definitions.
-   Pressure-vs-baseline comparison for every ranked player.
-   Sample size: matches, innings, pressure innings/deliveries and balls
    bowled/faced.
-   Reliability indicator and uncertainty range.
-   Competition and season coverage, with IPL and T20I initially
    analysed separately.
-   A transparent explanation of why each player ranks where they do.
-   A limitations section identifying unavailable features such as
    yorker labels or bowling style if the data does not contain them.

## 13. Immediate next actions for your current VS Code project

1.  Open `notebooks/01_data_exploration.ipynb` and run all cells using
    the project's virtual-environment kernel.
2.  Record the actual competition names/seasons and inspect category
    values for extras and dismissal fields.
3.  Do not start the final pressure score until legal-ball, extras,
    target and wicket logic are validated.
4.  In `notebooks/02_data_cleaning.ipynb`, create a clean delivery-level
    table with one row per valid delivery and documented exclusions.
5.  Then implement pressure-state features in
    `03_pressure_detection.ipynb`, before calculating player rankings.

The next checkpoint should be a validated data dictionary and a small
set of manually checked matches. Once those pass, the pressure model can
be implemented with much greater confidence.

## 14. Final verdict

**Your approach is worth adopting, but as a role-and-context layer
rather than the complete pressure model.**

Keep the phase segmentation and the player-skill questions. Improve them
by defining pressure from the match state, comparing like with like,
validating the raw cricket calculations, and adjusting for sample size.
This will make P.R.I.M.E. more precise, explainable and defensible for
the competition.

------------------------------------------------------------------------

*P.R.I.M.E. \| Analytical design note*
