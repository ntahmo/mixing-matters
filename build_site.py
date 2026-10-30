from pathlib import Path
import re, html, json
from markdown_it import MarkdownIt
from jinja2 import Template
root=Path(__file__).parent
md=MarkdownIt('commonmark',{'html':True,'linkify':True}).enable('table')
chapters={}
def chapter(slug,title,subtitle,body): chapters[slug]=(title,subtitle,body)
chapter('01-why-mixing','Why mixing matters','Start with people and encounters, not matrices.',r'''
## Begin with an ordinary question
Imagine two communities, each with 100 people. People in both communities average two meaningful contacts per week. Would an infection spread in the same way? **Not necessarily.** In the first community everyone meets within a small, stable circle. In the second, people routinely connect otherwise separate circles. The number of contacts is the same, but the routes available to an infection are different.

A mixing model makes a disciplined statement about **who interacts with whom**. It does not by itself tell us whether an interaction transmits infection. That requires a separate description of infectiousness, susceptibility, duration, protection, and the kind of encounter.

<div class="callout"><strong>Keep three questions apart.</strong> <ol><li><em>How many interactions?</em> Contact rate.</li><li><em>With whom?</em> Mixing pattern.</li><li><em>What happens during an interaction?</em> Transmission process.</li></ol></div>

## Not every connection means the same thing
An age-stratified respiratory model might count conversational or close-proximity contacts. An HIV model might count partnerships, and additionally the sex acts occurring within a partnership. A network model might record whether a relationship exists and how long it lasts. An agent-based model might generate encounters in schools, workplaces, households, or venues. These can all be called *mixing*, but the **unit** must be stated first.

The POLYMOD study demonstrated that contact opportunities vary substantially by age and setting, and that contact surveys can help inform transmission models [Mossong et al., 2008](../references.html#mossong2008). Sexual partnership models have long represented differences by age and sexual activity [Garnett & Anderson, 1993](../references.html#garnett1993).

## Two illustrative worlds

| World | Contact rate | Pattern | Possible implication |
|---|---|---|---|
| Stable circles | 2 contacts/person/week | Mostly within circles | Clusters may remain comparatively separated |
| Bridges between circles | 2 contacts/person/week | Frequent cross-circle contacts | Infection can connect otherwise separated groups |

These are illustrative mechanisms, **not** predictions for a named population. The effect depends on biology and the rest of the model.

## What a mixing matrix contributes
Suppose we divide a population into groups A and B. A row of a mixing matrix answers: “Of all interactions made by a member of group A, what fraction involve someone from A, and what fraction involve someone from B?” If the row is `[0.75, 0.25]`, three in four interactions go to A and one in four to B. It says nothing yet about how many total contacts group A has.

The next chapters translate this everyday idea into population counts, partnership opportunities, equations, and checks. You can learn the principles without knowing calculus.

### Check your understanding
<details><summary>Is having more partners the same as assortative mixing?</summary><p>No. A person can have many partners without preferring partners who also have many partners. Rate and preference are distinct.</p></details>
''')
chapter('02-language','The vocabulary of mixing','Groups, rates, probabilities, and flows—without hidden notation.',r'''
## Start with four groups
Our recurring fictional example has two characteristics: activity, high (H) or low (L); and meeting context, physical (P) or virtual (V). This produces **HP, LP, HV, LV**. These labels are placeholders for educational use. They are not categories that every real population must use.

| Symbol | Plain-language interpretation | Example |
|---|---|---|
| Nᵢ | People in group *i* | 100 people in HP |
| cᵢ | Partnership ends contributed per person per year | 4 for HP |
| Qᵢ = Nᵢcᵢ | Total partnership ends contributed by group *i* | 400 for HP |
| Mᵢⱼ | Fraction of group *i*'s ends aimed at group *j* | 0.20 |
| Fᵢⱼ = QᵢMᵢⱼ | Directed count of partnership ends from *i* to *j* | 80 |

**Why “partnership ends”?** In an undirected two-person partnership, each partner contributes one end. If there are 100 within-group partnerships in a closed population, they contribute **200 ends**, not 100. A partnership between different groups contributes one end to each group. This convention makes reciprocity transparent.

## A small numerical example
Assume a group contains 100 people, each contributing four partnership ends per year. Then `Q = 100 × 4 = 400` ends/year. If 20% are directed toward another group, `F = 400 × 0.20 = 80` ends/year. This is not necessarily 80 new, distinct people: repeated partnerships, duration, and relationship definitions must be handled separately.

### Conditional probabilities, not person-level labels
`M_HP,LV` means the fraction of opportunities offered by HP whose partners are in LV. It is **not** the proportion of LV people in the whole population, nor the probability that an HP person ever has an LV partner.

## Three units that must agree

1. **Population:** people.
2. **Contact rate:** partnership ends per person per unit time.
3. **Flow:** partnership ends per unit time.

If rates are per year while infectious periods are coded in weeks, the epidemic model will be inconsistent even if the mixing matrix is perfect.

## Different model families, same bookkeeping
Contact matrices for respiratory infections often use *contacts per person per day*, not partnership shares. If `Cᵢⱼ` is such a matrix, consistency for undirected contacts is `Nᵢ Cᵢⱼ = Nⱼ Cⱼᵢ`. For partnership shares `Mᵢⱼ`, the corresponding condition is `QᵢMᵢⱼ = QⱼMⱼᵢ`. A model must not substitute one interpretation for the other [Arregui et al., 2018](../references.html#arregui2018).

<div class="callout"><strong>Stop and ask:</strong> Does my rate count people, encounters, partnerships, sex acts, or relationship-years? Write the answer at the top of the model specification.</div>

<details><summary>Are HP and LV actual partner-meeting venues?</summary><p>No. They are <em>individual-level model strata</em>. A partnership initiated online does not imply that both partners primarily meet partners online. This distinction matters when interpreting survey variables.</p></details>
''')
chapter('03-opportunities','From populations to opportunity shares','Calculate the denominators before deciding how people mix.',r'''
## Work the numbers by hand
Consider this **synthetic** population. People in high-activity groups contribute more partnership ends per person than those in low-activity groups.

| Group | People Nᵢ | Rate cᵢ/year | Ends Qᵢ=Nᵢcᵢ | Share Qᵢ/Q |
|---|---:|---:|---:|---:|
| HP | 100 | 4 | 400 | 36.36% |
| LP | 200 | 1 | 200 | 18.18% |
| HV | 50 | 4 | 200 | 18.18% |
| LV | 300 | 1 | 300 | 27.27% |
| **Total** | **650** | | **1,100** | **100%** |

The **joint distribution of partnership opportunities** is the last column. That is what proportionate partnership selection uses—not the distribution of people.

## Why count opportunities instead of people?
HP contains 100 of 650 people (15.4%), yet offers 400 of 1,100 ends (36.4%). Selecting a random *person* and selecting a random *partnership end* are different experiments. The difference is consequential for sexually transmitted infections.

## Margins are not the joint distribution
Add across activity: `Q_H = Q_HP + Q_HV = 600` and `Q_L = 500`. Add across typology: `Q_P = Q_HP + Q_LP = 600` and `Q_V = 500`.

The proportion of high-activity ends within physical networks is `400 / 600 = 66.7%`; within virtual networks it is `200 / 500 = 40%`. **These distributions differ.** This does not invalidate mixing. It means that multiplying marginal activity and typology shares would ignore their association.

<div class="equation" role="math" aria-label="Joint opportunity share">Joint share for HP = Q<sub>HP</sub>/Q = 400/1100 = 0.3636</div>
<div class="equation" role="math" aria-label="Incorrect independent marginal product">Product of margins = (Q<sub>H</sub>/Q)(Q<sub>P</sub>/Q) = (600/1100)² = 0.2975</div>

## What can data actually tell you?
Individual-level program records can sometimes estimate counts by activity and meeting context. But they may not represent all people in the target population; testing and service use are selective. Additionally, `cᵢ` often needs a distinct survey or literature estimate. Report both the source of `Nᵢ` and the source of `cᵢ`, and propagate uncertainty where necessary.

## Try it
Change the HP rate from four to eight in the [interactive explorer](../explorer.html). The HP opportunity share increases even though its population stays at 100. Then compare proportionate and preferred mixing.

<details><summary>What if a group has zero opportunities?</summary><p>The fraction Fᵢⱼ/Qᵢ is undefined when Qᵢ=0. A robust implementation removes inactive groups from the current mixing system or handles them explicitly; it must not silently divide by zero.</p></details>
''')
chapter('04-proportionate','Proportionate mixing, step by step','Your safest baseline—and a useful mathematical reference point.',r'''
## The underlying experiment
Imagine putting every partnership end from every group into one large pool. To choose a partner for an end from HP, draw from the pool in proportion to how many ends each group contributes. The resulting destination probability does **not** depend on whether the starting end comes from HP, LP, HV, or LV.

<div class="equation" role="math">M<sub>ij</sub> = Q<sub>j</sub> / Q, &nbsp; where Q = Σ<sub>k</sub>Q<sub>k</sub></div>

With the synthetic opportunity vector `[400, 200, 200, 300]`, every row of the matrix is:

| From ↓ / To → | HP | LP | HV | LV |
|---|---:|---:|---:|---:|
| HP | 0.364 | 0.182 | 0.182 | 0.273 |
| LP | 0.364 | 0.182 | 0.182 | 0.273 |
| HV | 0.364 | 0.182 | 0.182 | 0.273 |
| LV | 0.364 | 0.182 | 0.182 | 0.273 |

## Why every row sums to one
Each row adds `(400+200+200+300)/1100 = 1`. The entries are probabilities of **where an end goes**, conditional on its starting group.

## Why reciprocity holds automatically
For any pair `i,j`, the flow from i to j equals `Qᵢ(Qⱼ/Q) = QᵢQⱼ/Q`. Swap the indices and you get the same expression. The equality is algebraic; it does not depend on the actual sizes of the four groups.

<div class="equation" role="math">Q<sub>i</sub>M<sub>ij</sub> = Q<sub>i</sub>Q<sub>j</sub>/Q = Q<sub>j</sub>M<sub>ji</sub></div>

## Is this the same as completely random contacts?
Not always. The phrase *random mixing* is used inconsistently across fields. Here it means **proportionate selection among partnership opportunities** with no extra preference based on group labels. It does not imply that each person has the same rate, and it does not represent household persistence or concurrency. Always state the mathematical definition.

## When this baseline is helpful
It is a transparent benchmark when partner-to-partner data are unavailable. It isolates the consequences of unequal group sizes and unequal rates before introducing assortativity. A difference in the high-activity distribution across meeting contexts is entirely compatible with this baseline.

## Limits
Proportionate mixing might underrepresent within-age contacts, repeated partners, venue segregation, household structure, or geographic separation. Evidence from social-contact diaries and sexual partnership studies motivates exploring richer structures when the research question demands them [Mossong et al., 2008](../references.html#mossong2008); [Garnett & Anderson, 1993](../references.html#garnett1993).

<details><summary>Why are there nonzero HP-to-HP flows?</summary><p>Because proportionate selection includes all available ends, including same-group ends. Zero assortativity is not the same as forced disassortativity.</p></details>
''')
chapter('05-reciprocity','Reciprocity without mystery','Check flows rather than guessing whether probabilities should match.',r'''
## A partnership has two ends
Take two groups: A offers 100 ends/year and B offers 200. If A allocates 40% of its ends toward B, that produces **40 A→B ends/year**. To balance them, B must allocate **20%** of its ends toward A, because `200 × 0.20 = 40`.

<div class="equation" role="math">Q<sub>A</sub>M<sub>AB</sub> = Q<sub>B</sub>M<sub>BA</sub></div>

The probabilities are allowed to differ. What must match is the *count* of ends on both sides of the same undirected cross-group partnerships.

## Three independent checks

| Test | Formula | What failure means |
|---|---|---|
| Valid shares | Every Mᵢⱼ ≥ 0 and ≤ 1 | Impossible probability |
| Row totals | Σⱼ Mᵢⱼ = 1 | Not all ends allocated, or too many |
| Reciprocity | QᵢMᵢⱼ = QⱼMⱼᵢ | Different numbers of ends claim the same cross-group partnerships |

For computation, define `Fᵢⱼ = QᵢMᵢⱼ`. Check that `F` is symmetric and its row sums equal `Q`.

## Why checking after a simulation is too late
You can create and validate a mixing matrix **before** any infection compartments or ODEs exist. If the matrix is recalculated because population sizes change, repeat the checks at each recalculation. [Arregui et al. (2018)](../references.html#arregui2018) explain why transporting contact matrices to a new demographic population requires care.

## A trap: symmetrizing is not enough
A tempting fix is `F* = (F + Fᵀ)/2`. That makes `F*` symmetric, but it **usually changes the row totals**. Dividing rows of `F*` by their old `Q` then breaks normalization. We need both symmetry **and** the correct margins, for example by choosing a construction that ensures both or using an appropriate symmetric balancing algorithm.

## When strict reciprocity is not appropriate
The standard identity assumes *undirected two-person encounters inside a closed modeled interaction system* with consistent counting units. It may not directly apply to (a) one-way information exposure, (b) directed transmissions such as needle sharing specified directionally, (c) encounters with partners outside the represented population, or (d) surveys with missing/unequal reporting. In those settings describe the interaction process and boundary explicitly rather than forcing inappropriate equality.

## The useful distinction
Empirical observations determine possible *rates* and provide evidence about partner choice. **Reciprocity is a structural consistency condition** for the relevant type of partnership. Observed diary counts can be noisy and nonreciprocal, and methods may reconcile them while acknowledging uncertainty.

<details><summary>Can I check reciprocity with only N and c?</summary><p>No. N and c give the margins Q, but you also need a proposed or estimated M. You can inspect Q before modeling; reciprocity becomes testable once you have M.</p></details>
''')
chapter('06-assortativity','Assortativity and preferred mixing','Build preferences without losing the mathematical safeguards.',r'''
## What does assortativity mean?
Assortativity means that partners with some shared feature interact **more frequently than predicted by the chosen baseline**. High within-group contact alone does not prove assortativity: a group that offers most opportunities would have many within-group partnerships even under proportionate mixing.

## Standard preferred mixing
A simple established construction blends exact-group matching with proportionate selection:

<div class="equation" role="math">M<sub>ij</sub> = ε 1(i=j) + (1−ε) Q<sub>j</sub>/Q, &nbsp; 0 ≤ ε ≤ 1</div>

The symbol `1(i=j)` equals one when the start and destination are the same joint group, otherwise zero. Interpret ε as the **weight of the exact-group matching component**, not as the observed percentage of same-group partnerships.

| ε | Effect |
|---|---|
| 0 | Fully proportionate |
| 0.4 | 40% exact-group preference component + 60% proportionate component |
| 1 | Every end is matched within its joint group |

## Work an HP-to-LV example
HP offers 400 ends, LV offers 300, and total Q is 1,100. With `ε = 0.4`, HP-to-LV has no exact-group contribution, so `M_HP,LV = 0.6 × 300/1100 ≈ 0.1636`. The resulting HP→LV flow is `400 × 0.1636 ≈ 65.45` ends/year. Reverse selection gives `M_LV,HP = 0.6 × 400/1100 ≈ 0.2182`, and `300 × 0.2182 ≈ 65.45` ends/year.

Notice again: the probabilities are different, the partnership counts agree.

## Why preferred mixing is reciprocal
For i ≠ j, the flow is `(1−ε)QᵢQⱼ/Q` in either direction. For i=j, reciprocity is trivial. Each row sums to `ε+(1−ε)=1`. Thus the core checks hold **by construction** for any positive opportunity distribution.

## An important limitation for multiple strata
Exact-group matching means **HP prefers HP**, not simply “people in physical networks prefer people in physical networks.” A match must share *both* activity and context. The equation therefore cannot distinguish a preference for the same activity from a preference for the same meeting context. That motivates the next chapter.

## What about ε > 1?
Not in this formulation. A mixture weight is a probability-like coefficient constrained to `[0,1]`. Other assortativity formulations use unconstrained affinity coefficients, but they have a different interpretation; never reuse the same symbol as though it represented the same parameter.

<details><summary>Could ε be negative for disassortative mixing?</summary><p>Not in the standard convex-mixture formula above. Disassortative models require a different valid construction and explicit feasibility checks.</p></details>
''')
chapter('07-two-axes','Two characteristics, one mixing matrix','Independent preferences, joint distributions, and the staged-selection trap.',r'''
## The three questions people often confuse
1. **Are the characteristics associated?** For example, is high activity more common in physical than virtual networks? This concerns the joint opportunity distribution `Qᵣₘ`.
2. **Do partners prefer matching activity?** This concerns activity assortativity.
3. **Do partners prefer matching meeting context?** This concerns context assortativity.

Answering “yes” to question 2 does not imply “yes” or “no” to question 1. The data distribution and preference mechanism are different objects.

## The independence trap
At zero assortativity, fully proportionate mixing should assign `Qᵣ′ₘ′/Q` to each destination stratum. Multiplying `Qᵣ′/Q` by `Qₘ′/Q` only recovers that joint share when activity and context are independent **among partnership ends**.

Take the synthetic distribution `[400,200,200,300]`. The true HP opportunity share is `400/1100 ≈ 0.364`; the product of marginal shares gives `(600/1100)(600/1100) ≈ 0.298`. The difference is meaningful and does not disappear just because both preferences are called “independent.”

## Does selecting typology first make mixing dependent?
A joint selection probability always has the chain-rule identity `P(r′,m′|r,m) = P(m′|r,m) × P(r′|m′,r,m)`. We could write the same distribution activity-first. **An ordering of symbols does not by itself represent behavioral timing.** Dependence enters when we constrain the conditional probabilities to depend on previous choices in a particular way.

## A reciprocal alternative: balanced symmetric affinities
Suppose we want separate preferences for sharing activity and sharing meeting context without assuming independence of those characteristics in the population. Define the *unnormalized* symmetric partnership-flow weights:

<div class="equation" role="math">W<sub>ij</sub> = (Q<sub>i</sub>Q<sub>j</sub>/Q) × exp[θ<sub>r</sub> 1(r<sub>i</sub>=r<sub>j</sub>) + θ<sub>m</sub> 1(m<sub>i</sub>=m<sub>j</sub>)]</div>

These weights favour matching activity if `θᵣ>0` and matching typology if `θₘ>0`. They are not probabilities. We then solve for positive scaling factors `aᵢ` such that:

<div class="equation" role="math">F<sub>ij</sub> = a<sub>i</sub> W<sub>ij</sub> a<sub>j</sub>, &nbsp; Σ<sub>j</sub>F<sub>ij</sub> = Q<sub>i</sub>, &nbsp; M<sub>ij</sub> = F<sub>ij</sub>/Q<sub>i</sub></div>

Because W is symmetric and both ends receive scaling, F remains symmetric: reciprocity holds. This is related to the general literature on matrix scaling with prescribed margins [Rothblum & Schneider, 1989](../references.html#rothblum1989). Its row sums are explicitly constrained to Q. When both θ values are zero, the solution is proportionate mixing. The [explorer](../explorer.html) implements this **illustrative two-axis construction**. Its θ values are *log-affinity parameters*, not equivalent to the earlier ε.

## Independent preferences versus staged preferences
It is possible to specify a staged conditional model, but we must solve the same flow constraints. The earlier “typology first, then activity” tree was useful pedagogically; without proper balancing, however, its naive probabilities could fail the proportionate limit or reciprocity. **Do not use an unchecked product of marginal preference kernels as a final model.**

<div class="callout"><strong>Takeaway:</strong> Different activity distributions within contexts are allowed. Use their joint opportunities, and construct the final flow matrix so it is symmetric with the correct row totals.</div>
''')
chapter('08-data','Learning from empirical data','What can be estimated, what stays uncertain, and how to avoid false precision.',r'''
## Four different empirical objects
A dataset can tell us about (1) group sizes, (2) how many interactions people have, (3) the characteristics of their partners, and (4) characteristics of the interactions themselves. These are not interchangeable. A dataset containing only respondents' meeting contexts cannot directly estimate their partners' meeting contexts.

| Data source | Common contribution | Common limitation |
|---|---|---|
| Program records | Service-engaged population composition and outcomes | Selection into programs; variable missingness |
| Contact diary | Number and characteristics of recent contacts | Recall, reporting, and day-to-day variation |
| Partnership survey | Partner attributes, relationship counts, duration | Recall, stigma, nonresponse; absent partner reports |
| Network survey | Links, concurrency, connectivity | Boundary bias; incomplete networks |
| Census/demographic data | Population structure | May not measure contacts or sexual behavior |

[Mossong et al. (2008)](../references.html#mossong2008) provide an influential example of diary-based contact measurement. [Prem et al. (2017)](../references.html#prem2017) illustrate combining contact surveys with demographic information to project matrices to settings with less direct data.

## A transparent analysis pipeline
**First:** specify the target population, timescale and interaction unit. **Second:** estimate the joint group distribution `Nᵢ`. **Third:** estimate interaction rates `cᵢ`, ideally with uncertainty intervals. **Fourth:** compute the opportunity distribution `Qᵢ`. **Fifth:** if partner attributes are observed, estimate between-group interaction counts or conditional probabilities. **Sixth:** reconcile reporting asymmetries if the interaction is undirected. **Seventh:** assess whether the reconstructed matrix generalizes to your target population.

## Check the joint distribution before fitting anything
To compare high versus low activity across physical versus virtual context, construct a two-way table **of people**. Then, if rates are available, compute a two-way table **of partnership opportunities**. Test or describe their association separately. Do not assume independence merely because the activity and context parameters will be modeled separately.

## Why an empirical matrix may not balance
Group A may report more A–B encounters than group B reports B–A encounters. This can happen from sampling variability, weighting errors, recall, unobserved partners, or differing interpretations of an interaction. Reciprocity is a property of the modeled undirected interactions, not proof that an imperfect survey must be internally exact. Balancing or smoothing should respect the study design; simply averaging is not always adequate [Arregui et al., 2018](../references.html#arregui2018).

## A lesson for community-engaged work
Ask collaborators about *mechanisms*: where people encounter partners, who crosses contexts, whether relationships persist, which partnerships may fall outside the modeled population, and whether the survey asks about respondents or their partners. Do not ask people to guess a numerical “ε = 0.6.” Use different perspectives to design and prioritize structural sensitivity analyses.

## The five-column evidence register
For each mixing assumption, record **claim → source → data support → uncertainty → analysis action**. Example: “Partner contexts overlap” → community discussion → qualitative plausibility → cross-context frequency unknown → compare low, moderate and high cross-context mixing scenarios.

<details><summary>Can calibration identify the mixing matrix from HIV prevalence alone?</summary><p>Usually not uniquely. Different mixing assumptions and transmission parameters can produce similar prevalence histories. This is a structural identifiability problem and should motivate sensitivity analyses and, where possible, partner-specific data.</p></details>
''')
chapter('09-frameworks','Mixing beyond compartmental models','A shared idea implemented differently in ODEs, networks, agents, and stochastic processes.',r'''
## Compartmental models
A stratified deterministic model uses a matrix to average infectious exposure across groups. Typically, `cᵢ Mᵢⱼ` specifies how many partnership opportunities a person in group i directs toward j, and a transmission term then weights the prevalence or availability of infectious partners in group j. Care is needed to avoid double-counting sex acts or protection modifiers.

<div class="equation" role="math">λ<sub>i</sub>(t) = c<sub>i</sub>(t) Σ<sub>j</sub> M<sub>ij</sub>(t) × infectious-risk-from-group-j</div>

This is a generic schematic, not a universal force-of-infection formula. In some models contact frequency and transmission probability are combined differently.

## Individual-based and agent-based models
Instead of storing only expected flows, agents each carry attributes. The model may draw partner groups using `M` and then sample a particular partner, respecting availability, partnership duration, and venue constraints. It can represent individual histories and heterogeneous behavior, but incurs computational and data demands. A mixing matrix can still be an aggregate **target** or diagnostic for simulated links.

## Static network models
Represent people as nodes and relationships as edges. Mixing can be summarized by counting edges linking types. Two populations can have the same group-level mixing matrix yet very different clustering, degree distributions, and bridge structures. Therefore, a matrix does **not** fully specify a network [Keeling & Eames, 2005](../references.html#keeling2005); [Bansal et al., 2007](../references.html#bansal2007).

## Temporal networks and partnerships
Partnerships form, last, and dissolve. Concurrency—overlap in the timing of partnerships—can influence HIV transmission even when aggregate counts are unchanged. A static matrix does not contain partnership timing [Kretzschmar & Morris, 1996](../references.html#kretzschmar1996).

## Stochastic epidemic simulations
Within a stochastic model, the matrix may define **event probabilities** rather than deterministic mean flows. Individual realizations will not necessarily satisfy exact reciprocity at every moment unless the simulation explicitly creates whole undirected pairs. Long-run expected patterns and realized link counts are distinct.

## Metapopulation and spatial models
Here mixing may mean commuting, visitation, migration, or contact between patches. Movement matrices can be *directed* and should not automatically be forced into reciprocal partnership form. A commuter departing A for B does not imply a simultaneous departure from B to A.

## Vector-borne infections
Human-to-mosquito and mosquito-to-human encounters represent a two-population transmission system. The relevant host–vector biting totals must be consistent, but a single symmetric human–human contact matrix is not the correct abstraction.

| Framework | What is explicitly represented? | Mixing's role |
|---|---|---|
| Stratified ODE | Group-level counts | Expected cross-group exposure |
| Agent-based | Individual agents | Partner-selection rule or emergent summary |
| Network | Specific links | Edge structure and cross-type connections |
| Temporal network | Links over time | Formation, dissolution, concurrency |
| Spatial/metapopulation | Patches and movement | Mobility or interpatch contacts |

**Rule:** decide what an interaction means in the framework *before* borrowing a mixing formula.
''')
chapter('10-time','When mixing changes over time','Populations evolve, behaviors respond, and matrices must remain coherent.',r'''
## Three things can change
Over time, (1) group sizes `Nᵢ(t)` may change; (2) contact rates `cᵢ(t)` may change; and (3) partner preferences may change. Each changes the mixing system for a different reason.

<div class="equation" role="math">Q<sub>i</sub>(t) = N<sub>i</sub>(t)c<sub>i</sub>(t), &nbsp; M<sub>ij</sub>(t) = f(Q(t), preference-parameters(t))</div>

With proportionate or standard preferred mixing, recalculating `M` from current opportunities preserves reciprocity automatically. With a fixed empirically estimated matrix, changing `N` and `c` generally changes the implied flows, so reciprocity may no longer hold.

## Three distinct interpretations of change
**Population turnover:** people enter and exit activity groups. **Behavior change:** an individual changes their rate or partner selection. **Network rewiring:** relationships break and new relationships form even if group assignments remain constant. These may require different state transitions or network rules.

## Worked thought experiment
At baseline, Group A contributes 100 ends and B contributes 100. In proportionate mixing, half the ends from either group go to A. Suppose B later contributes 300 ends while A stays at 100. Its opportunity share rises to 75%. Without any new preference, the proportionate mixing matrix must change. Keeping the old 50/50 matrix produces `F_AB = 50` and `F_BA = 150`, violating reciprocity.

The point is **not** that the true population instantly and perfectly rebalances all partnerships. It is that an equilibrium partnership-rate model with current opportunities needs a coherent matching rule. Short-term constraints, limited matching pools and partnership persistence may require a dynamic pair-formation model instead.

## When should you recalculate?
Possible choices include every solver step, monthly, annually, or after meaningful behavioral shifts. The appropriate interval depends on whether partnerships are modeled as instantaneous matching opportunities or persistent relationships. Document the choice and test sensitivity to it.

## Empirical perspective
[Arregui et al. (2018)](../references.html#arregui2018) highlight the challenge of transferring empirical contact matrices across demographic structures. [Edeling et al. (2021)](../references.html#edeling2021) highlight broader model uncertainty; even mathematically valid dynamics do not guarantee empirically accurate forecasts.

<details><summary>If ε stays constant, can M change?</summary><p>Yes. In preferred mixing, the proportionate part depends on Q(t). As group sizes or contact rates change, the same ε can yield different numerical matrices.</p></details>
''')
chapter('11-transmission','From mixing to transmission','Understand exactly where the matrix enters—and what it cannot tell you.',r'''
## A generic group-level transmission equation
After constructing the mixing matrix, the model can combine partner-selection probabilities with the infectious state of potential partners. Consider a generic partnership-based force of infection:

<div class="equation" role="math">λ<sub>i</sub>(t) = c<sub>i</sub>(t) Σ<sub>j</sub> M<sub>ij</sub>(t) B<sub>ij</sub>(t) I<sub>j</sub>(t)/N<sub>j</sub>(t)</div>

Here `cᵢ` is partnership opportunities/person/time; `Mᵢⱼ` is their destination share; `Bᵢⱼ` is a *per-partnership* transmission probability under the specified transmission-state assumptions; and `Iⱼ/Nⱼ` is the infectious proportion among eligible group-j partners. This expression is **illustrative**: real models may need separate disease stages, assortativity by infection state, concurrent partnerships, or partner availability.

## Interpret one term
For an HP person, the HP→LV contribution is proportional to their total partnership formation rate, the fraction of ends directed to LV, the probability an LV partner is infectious, and transmission conditional on such a partnership. Changing the mixing structure changes the second factor, not automatically the other three.

## Contact versus act versus partnership
Suppose a partnership contains multiple acts. If per-act transmission risk is `β` and there are `n` conditionally independent acts with constant risk, the per-partnership probability is `B = 1 − (1−β)ⁿ`. If condoms or sexual positions vary by act, the product must represent those distinctions. **Do not multiply a partnership formation rate by a transmission probability already defined for a different unit of exposure.**

## A source of hidden confounding
If high-activity people have higher HIV prevalence, an epidemic can be more concentrated among high-activity people even under proportionate mixing. Adding activity assortativity may intensify or redirect transmission, but the direction and size of the effect depend on the epidemic state and biology.

## Do intervention rankings depend on mixing?
They can. Two structurally different mixing assumptions can fit similar historical prevalence yet imply different transmission pathways, hence different projected effects of targeting prevention to groups. For an allocation question, mixing uncertainty is not just a technical footnote—it may be decision-relevant.

## Beyond HIV
For respiratory infection, mixing can combine with susceptibility and infectiousness by age, contact duration and setting [Wallinga et al., 2006](../references.html#wallinga2006). For sexually transmitted infections, partnership timing and concurrency may matter [Kretzschmar & Morris, 1996](../references.html#kretzschmar1996). The logic is general; the transmission term is disease-specific.

<div class="callout"><strong>Model-building discipline:</strong> validate M alone first, then connect M to the force of infection, then test the epidemic system. This isolates errors.</div>
''')
chapter('12-decisions','Choosing a mixing structure','A reusable research workflow, not a universal one-size-fits-all formula.',r'''
## First choose the interaction unit and boundary
Ask whether the model represents undirected partnerships among modeled people, daily social contacts, directed movement, or a bipartite host–vector process. This determines whether standard reciprocity applies and how the rows should be normalized.

## Then apply the decision table

| Evidence and objective | Sensible starting approach | What to test next |
|---|---|---|
| Group-specific contact rates but little partner detail | Joint proportionate mixing | Structural preference scenarios |
| Plausible preference for exact same strata | Standard preferred mixing | Range of ε and population rates |
| Distinct preferences for two characteristics | Reciprocal two-axis construction | Separate preference strengths and correlation |
| High-quality partner-by-partner data | Estimated matrix, reconciled as needed | Sampling bias and transportability |
| Persistence, concurrency, network clustering matter | Dynamic partnership/network model | Sensitivity to timing and degree structure |
| Directed travel flows | Directional movement matrix | Flow balance appropriate to movement, not symmetric partnering |

## A seven-step practical recipe
1. Write your scientific question, population boundary, and timescale.
2. Define each group and the contact/partnership unit.
3. Estimate or posit `Nᵢ`, `cᵢ`, and joint opportunities `Qᵢ`.
4. Choose the simplest mathematically appropriate baseline.
5. Validate row sums, nonnegativity, reciprocity **where appropriate**, and limiting behavior.
6. Compare plausible structural scenarios and parameter uncertainty.
7. Report which conclusions change and which remain robust.

## Pitfalls worth checking before a simulation

| Symptom | Likely issue | First response |
|---|---|---|
| Rows do not sum to one | Invalid kernel | Inspect normalization of conditional terms |
| Flows do not balance | Unchecked preference construction | Use reciprocal formulation or constrained balancing |
| Zero-assortativity limit wrong | Marginals multiplied despite association | Use the joint opportunity distribution |
| ε > 1 in a mixture | Parameter interpreted inconsistently | Revisit parameterization |
| Outcomes change unrealistically with group sizes | Frozen matrix transported to new margins | Recalculate or adapt the matrix |
| Different code implementations disagree | Index order or unit mismatch | Verify names, dimensions and time units |

## What belongs in a methods appendix?
Define strata, contact units and rates, preferred mixing assumptions, equations and their sources, reciprocity definition, data provenance, time updating, uncertainty ranges, and code validation tests. Show at least one example matrix and explain which numbers are assumed rather than observed.

## What can be inferred from a fit?
Calibration to prevalence or incidence can help assess whether the full epidemic system reproduces observations. It does **not** by itself establish that the contact mechanism is uniquely identified. [Edeling et al. (2021)](../references.html#edeling2021) provide a broader warning about structural and parametric uncertainty in epidemiological simulations.

<div class="callout"><strong>Recommended order for a beginner:</strong> proportionate → exact-group preferred → two-axis reciprocal affinities → empirically informed or temporal alternatives, only as the scientific question requires.</div>
''')
chapter('13-ai','AI as a modeling assistant','Where AI helps, where it fails, and how to keep the science reproducible.',r'''
## A useful collaborator, not a mathematical authority
AI tools can explain notation, sketch code, translate between R and Python, suggest unit tests, organize literature, and help prepare plain-language explanations. They can also generate equations that look credible while quietly violating probability normalization or reciprocity. Treat each equation as a claim to verify.

## A reproducible AI workflow
**1. Specify the task precisely.** “Construct a 4×4 partner mixing matrix for undirected partnerships, positive Q, two strata, and exact reciprocity.” **2. Ask for invariants.** Require rows to sum to one and `QᵢMᵢⱼ=QⱼMⱼᵢ`. **3. Require limit cases.** Verify that zero preferences recover joint proportionate mixing. **4. Execute tests independently.** Generate unequal and correlated opportunity distributions. **5. Audit assumptions.** Ask whether a parameter is a mixture weight, log-affinity, or direct data estimate. **6. Preserve provenance.** Commit code, test results, sources, and relevant AI-assisted development decisions.

## A worked failure you can recognize
An AI assistant suggests `Mᵣₘ,ᵣ′ₘ′ = P(r′|r)P(m′|m)` with separate partially assortative kernels built from marginal opportunity shares. This seems intuitive; rows sum to one. But if activity and meeting context are correlated, the zero-preference limit fails to recover `Qᵣ′ₘ′/Q`. If the opportunity distribution factorizes exactly and each one-axis kernel is reciprocal with respect to its own marginal opportunities, their product is reciprocal. But that special condition generally fails when the two characteristics are associated. **The fix is not a prettier explanation; it is a mathematically valid construction with tests.**

## An evaluation checklist

| Question | Required evidence |
|---|---|
| Does the citation exist? | Resolve DOI/publisher page and confirm the actual claim |
| Does the equation normalize? | Numerical test across varied group sizes |
| Is reciprocity correct? | Check flow equality, not probability equality |
| Are units coherent? | Explicit dimension analysis |
| Is the code reproducible? | Versioned files, test inputs, expected outputs |
| Is evidence distinguished from invention? | Mark synthetic examples, assumptions and extrapolations |

## AI in data-intensive modeling
It can assist with schema matching, data cleaning suggestions, imputation strategies and computational debugging, but human investigators must assess bias, confidentiality, consent and scientific appropriateness. Do not send identifiable partner or patient records into unapproved tools. WHO guidance on large multimodal models emphasizes governance and risk assessment in health applications [WHO, 2025](../references.html#who2025).

## Prompt template
> Explain the mixing model for a beginner. Define every symbol and unit, derive its zero-preference limit, prove or numerically check normalization and reciprocity, then supply independent R and Python unit tests. Identify which claims are supported by citations and which are new modeling assumptions. Do not invent data or references.

**Practical rule:** AI can accelerate the work of checking mathematics, but cannot replace checking mathematics.
''')
chapter('14-applications','Four case studies','Transfer the principles without pretending all interactions are identical.',r'''
## Case A: HIV partnerships across activity and meeting context
**Question:** How would targeting prevention differ if partnerships are proportionate, exact-group assortative, or assortative separately by activity and context? **Data:** population distribution, estimated partnership rates, some individual meeting-context variables, incomplete partner attributes. **Structure:** start with `Q=Nc`; compare joint proportionate, preferred, and two-axis reciprocal alternatives. **Key limitation:** respondent meeting context does not reveal partner typology, and a mixing matrix cannot represent concurrency by itself.

## Case B: Respiratory infection across age and setting
**Question:** How might closing schools alter transmission? **Data:** contact diaries with age and school/home/work settings. **Structure:** age-specific contact-rate matrices, optionally setting-specific components. **Validation:** use population-weighted reciprocal contacts, taking care with survey weights and demographics. **Key limitation:** a reported conversation is not an infection; duration and setting change per-contact risks. Contact-based work by [Mossong et al. (2008)](../references.html#mossong2008) and [Wallinga et al. (2006)](../references.html#wallinga2006) provides a grounding.

## Case C: An agent-based urban network
**Question:** Does connectivity between neighborhoods allow a pathogen to spread despite local clustering? **Data:** household membership, workplaces, commuting patterns, contact rates. **Structure:** explicit agents and encounters with emergent mixing matrices as diagnostics. **Validation:** compare simulated group-to-group contacts with targeted rates; examine degree distribution, clustering and bridges. **Key limitation:** a matching matrix alone cannot reproduce network topology [Keeling & Eames, 2005](../references.html#keeling2005).

## Case D: Vector-host contact system
**Question:** Which human groups receive more bites from vectors? **Data:** mosquito density, host attractiveness/exposure, biting behavior. **Structure:** host–vector interactions, with distinct host-to-vector and vector-to-host transmission stages. **Validation:** ensure the modeled biting totals agree, while recognizing that a directed movement or transmission matrix need not be symmetric. **Key limitation:** copying human–human partnership reciprocity into a host–vector transmission probability matrix is inappropriate.

## Compare assumptions, not only fit statistics
Across all four cases, the central modeling questions persist: what is the unit of contact, what distinguishes groups, what measurements support the structure, which constraints are mathematical, and how sensitive are conclusions to plausible alternatives? The answers—and the right equations—change with the process being modeled.

<div class="callout"><strong>Remember:</strong> a contact matrix is a structured summary of exposure opportunities. It is not a universal substitute for explicit relationships, movement, behavior, or biology.</div>
''')
chapter('15-workbook','Exercises and worked answers','Practice the decisions that catch the most common mistakes.',r'''
## Exercise 1 — opportunity totals
Group A has `N_A=80` people with `c_A=5` ends/person/year. Group B has `N_B=300` and `c_B=1`. Find `Q_A`, `Q_B`, and their proportionate partner shares.
<details><summary>Answer and reasoning</summary><p>Q_A = 400; Q_B = 300; Q = 700. Both source rows assign 400/700 ≈ 57.14% to A and 300/700 ≈ 42.86% to B. Source populations alone would give the wrong proportions.</p></details>

## Exercise 2 — reciprocity
Suppose `Q_A=400`, `Q_B=100`, and `M_AB=0.10`. Which `M_BA` balances between-group partnership ends?
<details><summary>Answer and reasoning</summary><p>The A→B flow is 40. B must send 40 ends to A, requiring M_BA = 40/100 = 0.40. The mixing probabilities need not be equal.</p></details>

## Exercise 3 — zero preference with correlated strata
Suppose `Q_HP=80`, `Q_LP=20`, `Q_HV=20`, `Q_LV=80`. Find the correct proportionate destination probability for HP and compare it with the product of marginal high-activity and physical-context shares.
<details><summary>Answer and reasoning</summary><p>Q = 200, so the correct joint probability is 80/200 = 0.40. High activity accounts for 100/200 and physical context for 100/200, so their marginal product is 0.25. The difference arises from association between activity and context.</p></details>

## Exercise 4 — why symmetry alone fails
Start with `Q_A=100`, `Q_B=200`, `M_AB=M_BA=0.40`. The cross-flows are 40 and 80. Suppose someone averages them to 60 in both directions but leaves within-group flow totals unchanged. What happens?
<details><summary>Answer and reasoning</summary><p>The cross-flows become symmetric, but each group's total flow changes by ±20. The row sums no longer equal Q_A and Q_B unless all other flows are adjusted as part of a constrained balancing construction.</p></details>

## Exercise 5 — interpret ε
In standard preferred mixing `ε=0.3`, and group A contributes 60% of opportunities. What is `M_AA`? Is it equal to 30%?
<details><summary>Answer and reasoning</summary><p>M_AA = 0.3 + (1−0.3)×0.6 = 0.72. The observed within-group probability is 72%, not 30%; ε is the mixing-component weight.</p></details>

## Exercise 6 — structure before calculation
You have detailed age-specific contact diaries but no partner duration information. Should you begin with an age mixing matrix or a dynamic partnership network?
<details><summary>Answer and reasoning</summary><p>An age-specific contact matrix is the better-supported starting point. A dynamic partnership network may still be scientifically useful, but its duration and dissolution parameters would need additional evidence and sensitivity analyses.</p></details>

## Exercise 7 — a prompt you should reject
An AI assistant claims that multiplying separately normalized activity and typology kernels is always reciprocal because every row sums to one. What is the logical error?
<details><summary>Answer and reasoning</summary><p>Row normalization is not reciprocity. Reciprocity compares Q_i M_ij with Q_j M_ji. A row-stochastic product construction can fail this equality, especially with correlated joint opportunities or unequal opportunity totals.</p></details>

## Capstone: construct and defend your model
Use the [mixing explorer](../explorer.html) to compare proportionate, preferred and two-axis reciprocal models on a correlated distribution. Export or copy the results, run the [Python/R examples](../resources.html), and write a one-page decision note: why this model, which parameters come from data, which assumptions remain, and which conclusions require sensitivity analysis.
''')
refs=[
('garnett1993','Garnett GP, Anderson RM','1993','Factors controlling the spread of HIV in heterosexual communities in developing countries: patterns of mixing between different age and sexual activity classes','Philosophical Transactions of the Royal Society B','10.1098/rstb.1993.0143','Foundational sexual partnership mixing and partnership-demand balancing.'),
('mossong2008','Mossong J, et al.','2008','Social contacts and mixing patterns relevant to the spread of infectious diseases','PLoS Medicine','10.1371/journal.pmed.0050074','Empirical social contact diaries and age assortativity.'),
('wallinga2006','Wallinga J, Teunis P, Kretzschmar M','2006','Using data on social contacts to estimate age-specific transmission parameters for respiratory-spread infectious agents','American Journal of Epidemiology','10.1093/aje/kwj317','Connection between contact patterns and respiratory transmission.'),
('prem2017','Prem K, Cook AR, Jit M','2017','Projecting social contact matrices in 152 countries using contact surveys and demographic data','PLoS Computational Biology','10.1371/journal.pcbi.1005697','Generalizing contact patterns using demographic data.'),
('arregui2018','Arregui S, Aleta A, Sanz J, Moreno Y','2018','Projecting social contact matrices to different demographic structures','PLoS Computational Biology','10.1371/journal.pcbi.1006638','Reciprocity and transporting empirical matrices between demographic structures.'),
('keeling2005','Keeling MJ, Eames KTD','2005','Networks and epidemic models','Journal of the Royal Society Interface','10.1098/rsif.2005.0051','Why networks contain information beyond group-level mixing.'),
('bansal2007','Bansal S, Grenfell BT, Meyers LA','2007','When individual behaviour matters: homogeneous and network models in epidemiology','Journal of the Royal Society Interface','10.1098/rsif.2007.1100','Comparing homogeneous and network representations.'),
('kretzschmar1996','Kretzschmar M, Morris M','1996','Measures of concurrency in networks and the spread of infectious disease','Mathematical Biosciences','10.1016/0025-5564(95)00093-3','Why relationship overlap and timing matter.'),
('kucharski2020','Kucharski AJ, et al.','2020','Effectiveness of isolation, testing, contact tracing, and physical distancing on reducing transmission of SARS-CoV-2 in different settings: a mathematical modelling study','The Lancet Infectious Diseases','10.1016/S1473-3099(20)30457-6','Example of combining contact changes and intervention scenarios.'),
('edeling2021','Edeling W, et al.','2021','The impact of uncertainty on predictions of the CovidSim epidemiological code','Nature Computational Science','10.1038/s43588-021-00028-9','Structural and parameter uncertainty and model sensitivity.'),
('rothblum1989','Rothblum UG, Schneider H','1989','Scalings of matrices which have prespecified row sums and column sums via optimization','Linear Algebra and its Applications','10.1016/0024-3795(89)90491-6','Mathematical foundations for prescribed-margin matrix scaling.'),
('who2025','World Health Organization','2025','Ethics and governance of artificial intelligence for health: Guidance on large multi-modal models','WHO guidance','9789240084759','Governance and risk management when using generative AI in health research.'),
]
entries=list(chapters.items())
nav=[{'slug':k,'title':v[0]} for k,v in entries]
links=''.join(f'<a href="{{{{base}}}}chapters/{k}.html" class="{{{{\'active\' if page==\'{k}\' else \'\'}}}}"><span>{i:02}</span> {html.escape(v[0])}</a>' for i,(k,v) in enumerate(entries,1))
# Jinja templating with simple context.
page_template=Template('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="{{ desc }}"><title>{{ title }} · Mixing Matters</title><link rel="stylesheet" href="{{ base }}assets/style.css"><link rel="icon" href="{{base}}assets/favicon.svg" type="image/svg+xml"></head><body><a class="skip" href="#content">Skip to content</a><div class="layout"><aside class="sidebar"><div class="side-top"><a class="brand" href="{{base}}index.html"><span class="brand-icon">∿</span> Mixing Matters</a><p>Understanding how populations connect—and why the equations work.</p></div><details class="mobile-nav"><summary>☰ &nbsp; Browse lessons & tools</summary><div class="mobile-nav-content"><a href="{{base}}explorer.html">Matrix explorer</a><a href="{{base}}walkthrough.html">Guided derivation</a><a href="{{base}}decision.html">Decision guide</a><a href="{{base}}cheatsheet.html">Cheat sheet</a><a href="{{base}}technical.html">Technical derivations</a><a href="{{base}}references.html">References</a>{% for s,t in nav %}<a href="{{base}}chapters/{{s}}.html">{{loop.index}}. {{t}}</a>{% endfor %}</div></details><div class="side-label">LEARN · 15 CHAPTERS</div><nav aria-label="Chapter navigation">{% for s,t in nav %}<a href="{{base}}chapters/{{s}}.html" {% if s==active %}aria-current="page" class="active"{% endif %}><span class="navnum">{{"%02d"|format(loop.index)}}</span><span>{{t}}</span></a>{% endfor %}</nav><div class="side-label">TOOLS & REFERENCE</div><nav aria-label="Tools navigation"><a href="{{base}}explorer.html">▦ &nbsp; Matrix explorer</a><a href="{{base}}walkthrough.html">▶ &nbsp; Guided derivation</a><a href="{{base}}cheatsheet.html">▤ &nbsp; Cheat sheet</a><a href="{{base}}technical.html">∑ &nbsp; Technical derivations</a><a href="{{base}}decision.html">◇ &nbsp; Decision guide</a><a href="{{base}}glossary.html">Aa &nbsp; Glossary</a><a href="{{base}}resources.html">⌘ &nbsp; R & Python</a><a href="{{base}}references.html">↗ &nbsp; Bibliography</a></nav><p class="side-foot">Free educational resource. No accounts, tracking, or personal data.</p></aside><main id="content" class="main"><div class="topbar"><a href="{{base}}index.html">Home</a><span> / </span><span>{{crumb}}</span><a class="top-tool" href="{{base}}explorer.html">Open explorer ↗</a></div>{{content}}<footer><div><strong>Mixing Matters</strong><br>Learn the mechanism. Check the mathematics. Document the assumptions.</div><div><a href="{{base}}references.html">Sources</a> · <a href="{{base}}resources.html">Reproducibility</a> · <a href="{{base}}README.md">README</a></div></footer></main></div><script src="{{base}}assets/site.js" defer></script></body></html>''')
# easiest formatting via jinja global filter zfill
page_template.environment.filters['zfill']=lambda s,n:str(s).zfill(n)
def page(title,body,base='',active='',crumb='',desc='Interactive guide to mixing in infectious disease models.'):
 return page_template.render(title=title,content=body,base=base,active=active,crumb=crumb or title,desc=desc,nav=[(k,v[0]) for k,v in entries])

def write(path,txt):
 p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(txt,encoding='utf-8')
for i,(slug,(title,subtitle,body)) in enumerate(entries):
 prev=entries[i-1][0] if i else None
 nxt=entries[i+1][0] if i<len(entries)-1 else None
 intro=f'<div class="eyebrow">CHAPTER {i+1:02} / {len(entries):02} <span class="dot">•</span> CORE LEARNING</div><h1>{html.escape(title)}</h1><p class="lead">{html.escape(subtitle)}</p>'
 sequence=f'<div class="chapter-nav">{f"<a href=\"{prev}.html\">← Previous chapter</a>" if prev else "<a href=\"../index.html\">← Overview</a>"}{f"<a href=\"{nxt}.html\">Next chapter →</a>" if nxt else "<a href=\"../explorer.html\">Try the explorer →</a>"}</div>'
 write(f'chapters/{slug}.html',page(title,intro+'<article class="prose">'+md.render(body)+'</article>'+sequence,base='../',active=slug,crumb=f'Chapter {i+1:02}',desc=subtitle))

home='''<section class="hero"><div class="eyebrow">AN OPEN, INTERACTIVE LEARNING RESOURCE</div><h1>Who connects with whom <em>changes everything.</em></h1><p class="lead">A plain-language introduction to mixing in infectious-disease models, followed by the equations, practical decisions, and code you need to build defensible models.</p><div class="actions"><a class="button" href="chapters/01-why-mixing.html">Start learning →</a><a class="button outline" href="walkthrough.html">Watch the derivation</a></div><p class="subtle">No prior mathematical modeling experience required · Synthetic teaching examples · Original explanations with linked scientific sources</p></section><section class="feature-row"><div><span class="metric">15</span><strong>structured chapters</strong><p>From intuition to applications, verification, and AI.</p></div><div><span class="metric">3</span><strong>reciprocal formulations</strong><p>Test proportionate, preferred, and two-axis mixing.</p></div><div><span class="metric">2</span><strong>code languages</strong><p>Reproducible Python and R with numerical checks.</p></div></section><section><div class="eyebrow">TWO WAYS TO LEARN</div><h2>Choose your path</h2><div class="path-grid"><a class="path" href="chapters/01-why-mixing.html"><span class="path-icon">01</span><h3>Beginner's textbook</h3><p>Start with people, simple counts, and visual examples. Encounter each equation only after its meaning is clear.</p><span>Begin with the foundations →</span></a><a class="path" href="decision.html"><span class="path-icon">02</span><h3>Practitioner's handbook</h3><p>Already building a model? Use the decision guide, diagnostic tests, reproducible code, and source-linked reference table.</p><span>Jump to the decisions →</span></a></div></section><section class="hero-slab"><div><div class="eyebrow">LIVE MATRIX EXPLORER</div><h2>Change a preference. Watch partnership flows respond.</h2><p>Try unequal group sizes, different activity distributions, and separate preferences for matching activity versus typology. See row sums and reciprocity checked in real time.</p><a class="button" href="explorer.html">Launch interactive explorer →</a></div><svg viewBox="0 0 350 220" role="img" aria-label="Illustration of partnerships between four grouped nodes"><g stroke="#6d9aa0" stroke-width="2.2" opacity=".6"><path d="M60 55 L290 55 M60 55 L60 165 M60 55 L290 165 M290 55 L60 165 M290 55 L290 165 M60 165 L290 165"/></g><g><circle cx="60" cy="55" r="29" fill="#d0ece0"/><circle cx="290" cy="55" r="29" fill="#d5e4fa"/><circle cx="60" cy="165" r="29" fill="#d5e4fa"/><circle cx="290" cy="165" r="29" fill="#d0ece0"/></g><g font-size="16" font-weight="700" fill="#16384b" text-anchor="middle"><text x="60" y="61">HP</text><text x="290" y="61">HV</text><text x="60" y="171">LP</text><text x="290" y="171">LV</text></g></svg></section><section><div class="eyebrow">THE LEARNING MAP</div><h2>Build confidence, one decision at a time</h2><div class="chapter-grid">'''+''.join(f'<a href="chapters/{s}.html"><small>{i:02}</small><strong>{html.escape(t[0])}</strong><span>{html.escape(t[1])}</span></a>' for i,(s,t) in enumerate(entries,1))+'''</div></section><section class="ethos"><h2>Three labels you'll see throughout</h2><div class="trio"><div><span>DATA</span><p>What we measured, and how reliable it is.</p></div><div><span>ASSUMPTION</span><p>What the modeler deliberately chose.</p></div><div><span>CONSTRAINT</span><p>What the mathematics requires.</p></div></div><p>These distinctions are especially important for reciprocity: it is not an unknown biological parameter to guess, but a consistency condition for a specified class of undirected partnerships.</p></section>'''
write('index.html',page('Home',home,crumb='Welcome'))

ref_html='<div class="eyebrow">EVIDENCE & ATTRIBUTION</div><h1>References and source notes</h1><p class="lead">A curated foundation for the concepts taught here. Each DOI links to the underlying publication. This is a selective teaching bibliography, not a systematic review.</p><div class="callout"><strong>Attribution standard:</strong> numerical examples and the symmetric two-axis affinity teaching construction are explicitly presented as illustrative; they are not estimates from any named population. The literature motivates the general methods and empirical claims—not every example or formula verbatim.</div><div class="ref-list">'
for key,authors,year,title,journal,doi,why in refs:
 url='https://www.who.int/publications/i/item/9789240084759' if key=='who2025' else 'https://doi.org/'+doi
 ref_html+=f'<section class="reference" id="{key}"><div class="eyebrow">{year}</div><h3>{html.escape(title)}</h3><p>{html.escape(authors)}. <em>{html.escape(journal)}</em>.</p><p class="subtle">Why it appears here: {html.escape(why)}</p><a href="{url}" target="_blank" rel="noopener">{"WHO publication" if key=="who2025" else "doi:"+doi} ↗</a></section>'
ref_html+='</div><h2>How this resource handles sources</h2><p>Sources were cross-checked against PubMed, journal pages, or WHO publication records at drafting. Claims of mathematical validity are separately checked in executable Python tests. A citation to a general class of models is not a claim that a specific illustrative equation originated in that publication.</p>'
write('references.html',page('References',ref_html))

glossary={'Assortativity':'Preference to interact with a similar group beyond what the baseline opportunities predict.','Contact matrix':'A table of contact rates or interaction shares between groups; always specify the unit.','Joint distribution':'Distribution across combinations of characteristics, such as activity and meeting context.','Mixing matrix':'A numerical rule for how interactions or partner opportunities are allocated between groups.','Partnership end':'One side of an undirected two-person partnership.','Proportionate mixing':'Destination group selected according to its share of available interaction opportunities.','Preferred mixing':'A specified blend of assortative selection and proportionate selection.','Reciprocity':'For undirected cross-group interactions, both groups count the same total between-group interactions.','Row stochastic':'Each matrix entry is nonnegative and every row sums to one.','Structural uncertainty':'Uncertainty about the form of the model, not merely its numerical parameter values.','Log-affinity θ':'A parameter multiplying symmetric partnership weights by exp(θ) for a matching characteristic; not a preferred-mixing ε.','ε (epsilon)':'A mixture weight between 0 and 1 in the standard preferred-mixing example.','Conditional probability':'A probability after restricting to a known condition, such as activity given a selected network.','Force of infection':'Instantaneous hazard of infection for susceptible people under a specified transmission model.','Balancing':'Solving for a matrix with required symmetry and row totals without changing the intended interaction totals.','Model boundary':'Which people and interactions are represented, and which lie outside the simulated system.'}
gloss='<div class="eyebrow">QUICK REFERENCE</div><h1>Glossary</h1><p class="lead">Plain-language definitions for the terms that often appear before anyone explains them.</p><div class="glossary">'+''.join(f'<section><h3>{html.escape(k)}</h3><p>{html.escape(v)}</p></section>' for k,v in sorted(glossary.items(),key=lambda p:p[0].casefold()))+'</div>'
write('glossary.html',page('Glossary',gloss))

resources='''<div class="eyebrow">REPRODUCIBILITY LAB</div><h1>Code, tests and datasets</h1><p class="lead">Every model construction demonstrated in the explorer has a corresponding Python implementation. R examples are provided for independent replication.</p><h2>Download the examples</h2><div class="download-grid"><a href="code/mixing.py" download><strong>Python · mixing.py</strong><span>Proportionate, preferred, and balanced two-axis mixing</span></a><a href="code/mixing.R" download><strong>R · mixing.R</strong><span>Companion code and reciprocity checks</span></a><a href="tests/test_mixing.py" download><strong>Python tests</strong><span>Multiple distributions and parameter combinations</span></a><a href="data/example_opportunities.csv" download><strong>Example data</strong><span>Synthetic four-group populations and rates</span></a></div><h2>Run locally</h2><pre><code>python tests/test_mixing.py
python code/mixing.py
Rscript code/mixing.R</code></pre><p>The Python example uses only the standard library. R examples use base R. The two-axis implementation uses a symmetric iterative scaling algorithm and raises an error if it cannot achieve the requested numerical tolerance.</p><h2>Numerical validation is not epidemiological validation</h2><p>Passing reciprocity and normalization tests confirms specific mathematical properties. It does not show that the selected mixing structure matches actual partnerships, correctly identifies causal pathways, or predicts incidence. That requires empirical calibration, transparent assumptions, and sensitivity analyses.</p><div class="callout"><strong>Repository status:</strong> illustrative teaching implementation. Do not substitute these examples for project-specific model calibration or external scientific review.</div>'''
write('resources.html',page('Reproducible code',resources))

# Generate machine-readable references; DOI-only BibTeX metadata is manually transcribed from validated citation pages.
bib='\n'.join(f'@article{{{key},\n  author = {{{authors}}},\n  title = {{{title}}},\n  year = {{{year}}},\n  journal = {{{journal}}},\n  doi = {{{doi}}}\n}}\n' for key,authors,year,title,journal,doi,why in refs if key!='who2025')
write('references.bib',bib)
write('data/example_opportunities.csv','group,activity,context,population,rate,partnership_ends\nHP,H,P,100,4,400\nLP,L,P,200,1,200\nHV,H,V,50,4,200\nLV,L,V,300,1,300\n')
print('Generated chapters:',len(entries),'written files:',len(list(root.rglob('*.html'))))
explorer='''<div class="eyebrow">INTERACTIVE MATHEMATICS LAB</div><h1>Build a mixing matrix</h1><p class="lead">Change population sizes, partnership rates, and preferences. The site calculates the resulting probabilities and partnership flows—and checks their mathematics immediately.</p><div class="callout"><strong>Teaching example:</strong> HP = high activity/physical context; LP = low activity/physical; HV = high activity/virtual; LV = low activity/virtual. These are synthetic groups, not observed HEKA data.</div><div class="tool-panel"><h2>1. Define the opportunity pool</h2><p class="mini-note">Q = N × c. Rates are partnership ends per person per year.</p><div class="preset-row"><button type="button" data-preset="original">Unequal activity composition</button><button type="button" data-preset="independent">Same composition across contexts</button><button type="button" data-preset="correlated">Strong association</button></div><div class="matrix"><table><thead><tr><th>Group</th><th>People N</th><th>Rate c</th><th>Ends Q</th><th>Share of Q</th></tr></thead><tbody id="opportunity-rows"></tbody></table></div><p id="joint-info" class="mini-note" aria-live="polite"></p></div><div class="tool-panel"><h2>2. Choose the mixing rule</h2><div class="field"><label for="mix-mode">Mixing structure</label><select id="mix-mode"><option value="proportionate">Proportionate — no group preferences</option><option value="preferred">Preferred — matching both characteristics</option><option value="twoaxis">Two-axis — separate activity and context affinities (balanced)</option><option value="naive">Demonstration: naive product of marginal kernels (may fail)</option></select></div><div class="inputs" style="margin-top:16px"><div class="field"><div class="control-head"><label for="epsilon">Preferred ε</label><output id="epsilon-value">0.40</output></div><input id="epsilon" type="range" min="0" max="1" step="0.05" value="0.4"></div><div class="field"><div class="control-head"><label for="theta-r">Activity log-affinity θᵣ</label><output id="theta-r-value">0.80</output></div><input id="theta-r" type="range" min="0" max="3" step="0.1" value="0.8"></div><div class="field"><div class="control-head"><label for="theta-m">Context log-affinity θₘ</label><output id="theta-m-value">1.20</output></div><input id="theta-m" type="range" min="0" max="3" step="0.1" value="1.2"></div></div><p class="mini-note" id="mix-explainer"></p><div class="preset-row"><button type="button" id="copy-matrix">Copy mixing probabilities (CSV)</button><button type="button" id="reset-matrix">Reset example</button></div></div><div class="toolsplit"><div class="tool-panel"><h2>3. Probability matrix M</h2><p class="mini-note">Each cell shows the percentage of a starting group's partnership ends aimed at a destination group.</p><div class="matrix" id="prob-matrix"></div></div><div class="tool-panel"><h2>4. Partnership flows F</h2><p class="mini-note">Fᵢⱼ = Qᵢ Mᵢⱼ. Compare cell i→j with its transpose j→i; they must match for undirected partnerships.</p><div class="matrix" id="flow-matrix"></div></div></div><div class="status" id="matrix-diagnostics" aria-live="polite">Calculating…</div><div class="tool-panel"><h2>What do these flows imply?</h2><p class="mini-note">The following are actual aggregate shares implied by the current model, not input ε or θ values.</p><div class="feature-row" style="margin:14px 0 0"><div><span class="metric" id="same-group">—</span><strong>Same joint group</strong></div><div><span class="metric" id="same-activity">—</span><strong>Same activity</strong></div><div><span class="metric" id="same-context">—</span><strong>Same context</strong></div></div></div><div class="tool-panel"><h2>5. Examine one pair</h2><p>Compare HP→LV with LV→HP. The <strong>probabilities can differ</strong>; the resulting flows must match.</p><div id="pair-demo"></div></div><div class="prose"><h2>How to interpret your experiment</h2><p><strong>Proportionate mixing:</strong> every row is the joint destination opportunity distribution, even when activity proportions differ between contexts. <strong>Preferred mixing:</strong> an ε-weighted exact-group matching component is added without violating reciprocity. <strong>Two-axis mixing:</strong> separate activity and context affinities are balanced to the same group opportunity totals. <strong>Naive marginal product:</strong> included deliberately to demonstrate why an intuitive equation can be normalized but still scientifically and mathematically wrong.</p><p>The two-axis θ values are <em>log-affinities</em>, not preferred-mixing mixture weights. Equal numerical θ values do not mean equal observed within-activity and within-context probabilities. See <a href="chapters/07-two-axes.html">Chapter 7</a> and <a href="resources.html">reproducible code</a>.</p><div class="callout"><strong>Interpretation boundary:</strong> these are expected partnership-end allocations. Integer realized partnership counts, age structure, partnership duration, and epidemic outcomes require additional modeling.</div></div><script src="assets/explorer.js" defer></script>'''
write('explorer.html',page('Interactive matrix explorer',explorer))
decision='''<div class="eyebrow">PRACTICAL DECISION SUPPORT</div><h1>Which mixing structure should I start with?</h1><p class="lead">Answer a few conceptual questions. The recommendation is a teaching aid—not an automated scientific judgment or substitute for model validation.</p><div class="tool-panel"><h2>1. What interaction are you modeling?</h2><div class="choice" data-question="unit"><button type="button" data-value="undirected">Two-person undirected contacts or partnerships</button><button type="button" data-value="directed">Directed movement, exposure, or flows</button><button type="button" data-value="network">Persistent relationships or network links</button></div><h2>2. What evidence do you have?</h2><div class="choice" data-question="evidence"><button type="button" data-value="margins">Group sizes and interaction rates; limited partner attributes</button><button type="button" data-value="preferences">Qualitative or literature-based group preferences</button><button type="button" data-value="matrix">Detailed observed contacts or partner types</button></div><h2>3. How many preference dimensions matter?</h2><div class="choice" data-question="axes"><button type="button" data-value="none">No additional preferences justified</button><button type="button" data-value="one">Exact same-group preference is sufficient</button><button type="button" data-value="two">Two separate characteristics may influence preferences</button></div></div><div id="decision-output" class="decision-output" aria-live="polite"><h2>Your recommended starting point</h2><p>Select an answer to each question to see a transparent recommendation.</p></div><div class="prose"><h2>Never skip the common checks</h2><ol><li>Define the interaction unit and target population boundaries.</li><li>Write the population–rate product in matching units.</li><li>Check mathematical properties appropriate to the process, including reciprocity for undirected partnerships.</li><li>Evaluate limiting cases and differences across correlated subgroup distributions.</li><li>Compare scenarios if empirical evidence cannot identify the structure.</li></ol><p>More detail in <a href="chapters/12-decisions.html">Chapter 12</a> and the <a href="explorer.html">matrix explorer</a>.</p></div><script src="assets/decision.js" defer></script>'''
write('decision.html',page('Mixing decision guide',decision))
walk='''<div class="eyebrow">GUIDED DERIVATION · 7 STEPS</div><h1>See how a mixing matrix is built</h1><p class="lead">An interactive explanation of how we go from group sizes and preferences to a valid mathematical representation—one decision at a time.</p><div class="tool-panel"><div style="display:flex;align-items:center;justify-content:space-between;gap:10px"><div class="eyebrow">PART <span id="lesson-number">1</span> / 7</div><span class="mini-note" id="lesson-time">Step-by-step</span></div><div style="display:grid;grid-template-columns:repeat(7,1fr);gap:5px;margin:16px 0" id="lesson-progress" aria-label="Lesson progress"></div><h2 id="lesson-title">Begin with four groups</h2><p id="lesson-body" aria-live="polite"></p><div class="equation" id="lesson-formula"></div><div class="toolsplit"><div class="tool-panel" id="lesson-table"></div><div class="tool-panel" id="lesson-interpretation"></div></div><div class="preset-row" style="justify-content:space-between"><button id="lesson-prev" type="button">← Previous</button><button id="lesson-next" type="button">Next step →</button></div></div><div class="prose"><h2>Why this matters</h2><p>It is easy to memorize a formula without realizing that a probability matrix and a partnership-flow matrix answer different questions. Here you can see every intermediate object, identify what was assumed, and understand precisely why reciprocity is checked in flows.</p><p>Continue in <a href="chapters/05-reciprocity.html">Chapter 5</a> or open the <a href="explorer.html">live explorer</a> to change the numerical assumptions yourself.</p></div><script src="assets/walkthrough.js" defer></script>'''
write('walkthrough.html',page('Guided derivation',walk))
cheat='''<div class="eyebrow">PRINTABLE QUICK REFERENCE</div><h1>The mixing cheat sheet</h1><p class="lead">A compact reference for choosing equations, checking them, and explaining what each quantity means.</p><div class="prose"><h2>Definitions</h2><table><thead><tr><th>Object</th><th>Definition</th><th>Units</th></tr></thead><tbody><tr><td>Nᵢ</td><td>Number of modeled people in i</td><td>People</td></tr><tr><td>cᵢ</td><td>Partnership ends offered per person per time</td><td>Ends/person/year</td></tr><tr><td>Qᵢ = Nᵢcᵢ</td><td>Group's opportunity margin</td><td>Ends/year</td></tr><tr><td>Mᵢⱼ</td><td>Fraction of i's ends directed to j</td><td>Unitless</td></tr><tr><td>Fᵢⱼ = Qᵢ Mᵢⱼ</td><td>Partnership flow, i to j</td><td>Ends/year</td></tr></tbody></table><h2>Choose a construction</h2><table><thead><tr><th>Structure</th><th>Core rule</th><th>Constraints</th></tr></thead><tbody><tr><td>Proportionate</td><td>Mᵢⱼ = Qⱼ/Q</td><td>Works with any positive joint Q; reciprocal.</td></tr><tr><td>Exact-group preferred</td><td>Mᵢⱼ = ε1(i=j)+(1−ε)Qⱼ/Q</td><td>0≤ε≤1; reciprocal for any positive Q.</td></tr><tr><td>Separate two-axis affinities</td><td>Wᵢⱼ ∝ QᵢQⱼ exp(θᵣ1(same r)+θₘ1(same m)); symmetrically balance</td><td>Numerical balancing must converge; check row sums and reciprocity.</td></tr><tr><td>Empirical matrix</td><td>Estimate contact/partner flows</td><td>Sampling uncertainty, reporting bias, population transport and boundary.</td></tr></tbody></table><h2>Always run the diagnostics</h2><div class="equation">Mᵢⱼ ≥ 0 &nbsp; | &nbsp; Σⱼ Mᵢⱼ = 1 &nbsp; | &nbsp; QᵢMᵢⱼ = QⱼMⱼᵢ</div><p>For undirected partnerships, check **each pair** of flows. For directed movement or exposure, do not impose symmetry without justification.</p><h2>Answers to frequent questions</h2><details><summary>Do unequal activity distributions across contexts make mixing invalid?</summary><p>No. They only mean that you should retain the joint opportunity distribution, rather than multiplying marginal distributions by default.</p></details><details><summary>Can I estimate reciprocity from the data?</summary><p>The observations inform contact rates and partner preferences. Reciprocity is a structural consistency condition for modeled undirected partnerships; noisy empirical observations may require appropriate adjustment.</p></details><details><summary>Should I always choose typology first?</summary><p>No. A sequential factorization is a mathematical identity, and behavioral ordering requires separate justification.</p></details><details><summary>Does passing numerical tests validate the model?</summary><p>No. It establishes internal mathematical consistency—not empirical realism, identifiability, or intervention validity.</p></details><div class="callout"><strong>Teaching order:</strong> understand interaction units → compute joint opportunities → construct a simple matrix → test reciprocity → add preferences → examine sensitivity.</div><p><a href="resources.html">Download reproducible R and Python examples</a> · <a href="references.html">Read the scientific sources</a></p></div>'''
write('cheatsheet.html',page('Mixing cheat sheet',cheat))
technical=r'''<div class="eyebrow">OPTIONAL ADVANCED REFERENCE</div><h1>Technical derivations and proofs</h1><p class="lead">For readers who want to verify—not merely accept—the algebra behind the teaching constructions.</p><div class="prose"><h2>1. Define the model system precisely</h2><p>Index joint groups by i=(r,m). Let Qᵢ&gt;0 denote partnership ends supplied per unit time by group i; set Q=ΣᵢQᵢ. Let M be a nonnegative row-stochastic matrix of partner-group probabilities, and F=diag(Q)M its flow matrix.</p><div class="equation">Σⱼ Mᵢⱼ = 1 &nbsp; ⇔ &nbsp; Σⱼ Fᵢⱼ = Qᵢ</div><p>For reciprocal undirected partnerships, impose Fᵢⱼ=Fⱼᵢ. Thus the mathematical task is to construct a <strong>symmetric nonnegative flow matrix with prescribed row margins</strong>. This framing converts “why does reciprocity keep failing?” into a standard matrix-construction problem.</p><h2>2. Proportionate mixing is reciprocal</h2><p>Choose Fᵢⱼ=QᵢQⱼ/Q. The row total is Σⱼ QᵢQⱼ/Q=Qᵢ, and Fᵢⱼ=Fⱼᵢ. Therefore Mᵢⱼ=Qⱼ/Q satisfies both normalization and reciprocity.</p><h2>3. Exact-group preferred mixing is reciprocal</h2><p>For 0≤ε≤1, choose Fᵢⱼ = ε Qᵢ1(i=j)+(1−ε)QᵢQⱼ/Q. The diagonal term is symmetric, and the proportionate term is symmetric. Row totals are εQᵢ+(1−ε)Qᵢ=Qᵢ, hence Mᵢⱼ = ε1(i=j)+(1−ε)Qⱼ/Q.</p><h2>4. When does a product of two one-axis kernels work?</h2><p>Suppose the joint opportunity distribution factorizes exactly into independent margins:</p><div class="equation">Qᵣₘ/Q = (Qᵣ/Q)(Qₘ/Q)</div><p>Let Aᵣᵣ′ be a row-stochastic activity kernel reciprocal with respect to activity margins Qᵣ, and let Bₘₘ′ be a row-stochastic typology kernel reciprocal with respect to typology margins Qₘ. Define the product kernel Mᵣₘ,ᵣ′ₘ′ = Aᵣᵣ′ Bₘₘ′.</p><p>Because the joint group weight is QᵣQₘ/Q, the forward flow becomes:</p><div class="equation">Qᵣₘ Mᵣₘ,ᵣ′ₘ′ = (QᵣAᵣᵣ′)(QₘBₘₘ′)/Q</div><p>Each parenthesized factor is symmetric under reversing its own indices. Their product is therefore symmetric, so the joint kernel is reciprocal. Normalization also follows because Σᵣ′Σₘ′Aᵣᵣ′Bₘₘ′=(Σᵣ′Aᵣᵣ′)(Σₘ′Bₘₘ′)=1.</p><div class="callout"><strong>Precise conclusion:</strong> the product of two marginal preferred-mixing kernels is a valid reciprocal construction when the joint opportunity distribution factorizes and the constituent kernels are themselves reciprocal with respect to the correct margins. Without those conditions, do not assume validity.</div><p>For the correlated teaching distribution Q=[400,200,200,300] and ε=0.4 in both marginal kernels, the product formula gives HP→LP ≈79.34 ends/year but LP→HP ≈47.60 ends/year. Rows still sum to one. This concrete counterexample shows that <strong>normalization alone does not guarantee reciprocity</strong>.</p><h2>5. A symmetric construction for correlated groups</h2><p>If the opportunity distribution does not factorize, one possible construction places positive symmetric affinities on each potential group pair:</p><div class="equation">Wᵢⱼ=(QᵢQⱼ/Q) exp[θᵣ1(rᵢ=rⱼ)+θₘ1(mᵢ=mⱼ)]</div><p>We seek positive factors aᵢ such that Fᵢⱼ=aᵢWᵢⱼaⱼ and ΣⱼFᵢⱼ=Qᵢ. If the numerical solver reaches the requested tolerance, F is symmetric by construction and has the correct margins; Mᵢⱼ=Fᵢⱼ/Qᵢ is consequently reciprocal and row-stochastic. This is a prescribed-margin scaling problem related to the general theory developed by <a href="references.html#rothblum1989">Rothblum &amp; Schneider (1989)</a>.</p><p>At θᵣ=θₘ=0, W=QᵢQⱼ/Q already has margins Q, so aᵢ=1 works and the baseline reduces exactly to proportionate mixing. The θ values are not probabilities or ε values; θ&gt;0 increases relative unbalanced weight for matching that dimension. Once margins are enforced, the <em>realized</em> matching proportions reflect the entire joint population.</p><h2>6. Why “just symmetrize the flows” is insufficient</h2><p>Given an arbitrary flow matrix G, define H=(G+Gᵀ)/2. H is symmetric, but in general ΣⱼHᵢⱼ≠Qᵢ. The original group partnership-rate totals are no longer respected. Further row normalization would break symmetry. A valid balancing method must satisfy both types of constraints simultaneously.</p><h2>7. Dynamic model implication</h2><p>If Qᵢ(t)=Nᵢ(t)cᵢ(t) changes with time, a fixed M may cease to be reciprocal. Recompute or otherwise adapt the flows whenever the matching margins change, or use an explicit partner formation/dissolution model with its own mechanics. The relevant mathematical consistency check depends on what the modeled encounters mean and which populations are inside the boundary. See <a href="references.html#arregui2018">Arregui et al. (2018)</a>.</p><h2>8. A reproducible numerical diagnostic</h2><pre><code>F = diag(Q) @ M
assert all(abs(M.sum(axis=1) - 1) &lt; tol)
assert all(M &gt;= 0)
assert max(abs(F - F.T)) &lt; tol_flow</code></pre><p>The short code above is pseudocode using NumPy-like matrix notation. Working dependency-free implementations and tests are available in <a href="resources.html">Resources</a>. Always report tolerances relative to the flow scale, especially when some groups offer many more partnership opportunities than others.</p><p><strong>Limitations:</strong> these proofs apply to the specified row-stochastic partner-share setup with positive opportunities and undirected partnership ends. Directed contacts, external partners, heterogeneous pair capacities, structured pair formation, and integer realization require adaptations.</p></div>'''
write('technical.html',page('Technical derivations',technical))
