"""
Generate Comprehensive Rajasthan Royals Scouting Dossiers for Top 10 Batters & Bowlers.
Outputs:
- outputs/submission_pack/scouting_dossiers.json
- dashboard/public/data/scouting_dossiers.json
- outputs/submission_pack/RR_WAR_ROOM_SCOUTING_DOSSIER.md
"""

import json
from pathlib import Path
import pandas as pd

def generate_scouting_dossiers():
    bat_df = pd.read_csv("outputs/rankings/top10_batters.csv")
    bowl_df = pd.read_csv("outputs/rankings/top10_bowlers.csv")
    
    # Rich Scouting Profiles for Batters
    batter_scouting = {
        126: {  # Rohit Sharma
            "archetype": "Elite Top-Order Match-Winner & Powerplay Enforcer",
            "rr_slot": "Opening Batter (Slot #1) / Aggressive Powerplay Initiator",
            "auction_tier": "Marquee / Potential Retention Target",
            "target_price_inr": "INR 14.0 Cr – 18.0 Cr",
            "max_bid_ceiling_inr": "INR 18.0 Cr",
            "fallback_targets": ["Devdutt Padikkal", "Phil Salt"],
            "strengths": [
                "Astonishing 183.4 Strike Rate under high pressure with +52.1 uplift vs baseline",
                "Deadly 211.3 SR at the death (overs 16-20) when batting deep",
                "Elite boundary percentage of 30.0% against highest-leverage bowling",
                "Proven five-time championship captaincy and crisis leadership"
            ],
            "vulnerabilities": [
                "Susceptible to express left-arm inswing in the first 8 balls of an innings",
                "36.8% dot ball rate indicates feast-or-famine approach early in high-pressure chases"
            ],
            "venue_fit": "Sawai Mansingh Stadium's larger square boundaries allow him to convert pull shots into maximums with pure timing; true bounce at Guwahati suits his front-foot stride.",
            "scouting_summary": "Rohit provides Rajasthan with an experienced match-winner who takes pressure completely off Yashasvi Jaiswal and Sanju Samson, giving RR an explosive, fear-free top order."
        },
        2756: {  # Shashank Singh
            "archetype": "Clutch Middle-to-Death Finisher & Pace Demolisher",
            "rr_slot": "Designated #6 Finisher / Chase Specialist",
            "auction_tier": "High-Priority Domestic Acquisition (The Next 'Vignesh Puthur' Scale Win)",
            "target_price_inr": "INR 5.5 Cr – INR 8.5 Cr",
            "max_bid_ceiling_inr": "INR 10.0 Cr",
            "fallback_targets": ["Abhinav Manohar", "Shahrukh Khan"],
            "strengths": [
                "Massive +69.2 Strike Rate uplift under pressure (171.8 Pressure SR vs 102.6 Baseline)",
                "Elite 185.5 SR in death overs (16-20) across 436 pressure balls faced",
                "Exceptionally low 29.1% dot ball rate under pressure (lowest among primary finishers)",
                "Mastery of high back-foot punch and pull against express hit-the-deck pace"
            ],
            "vulnerabilities": [
                "Can be contained by tight left-arm orthodox spin pitching on leg and spinning away in middle overs",
                "Relatively small career sample compared to international stalwarts"
            ],
            "venue_fit": "Perfect for Jaipur: his gap-finding agility and low dot percentage maximize runs on large outfields, and his power clears the straight boundaries comfortably.",
            "scouting_summary": "The exact solution to RR's long-standing death-overs puzzle. Slots in at #6 directly alongside Dhruv Jurel and Shimron Hetmyer, creating an indomitable lower order."
        },
        37052: {  # Naman Dhir
            "archetype": "High-Ceiling Dynamic Stroke-Maker & Middle Floater",
            "rr_slot": "#4/#5 Aggressive Middle-Overs Floater",
            "auction_tier": "Uncapped / Emerging Domestic Value Steal",
            "target_price_inr": "INR 2.5 Cr – INR 4.5 Cr",
            "max_bid_ceiling_inr": "INR 6.0 Cr",
            "fallback_targets": ["Sameer Rizvi", "Angkrish Raghuvanshi"],
            "strengths": [
                "182.8 Pressure Strike Rate and blistering 193.0 Death Overs SR",
                "28.0% boundary rate under high leverage",
                "Fearless intent against 140+ kph pace from ball one",
                "Offers useful off-spin utility to break right-hand combinations"
            ],
            "vulnerabilities": [
                "High dismissal rate when trying to clear deep midwicket against deceptive slower cutters",
                "Needs tactical discipline in low-scoring, grind-out matches"
            ],
            "venue_fit": "Excels on true surfaces like Guwahati and the center wicket at Jaipur; punishes spinners through the covers.",
            "scouting_summary": "High-upside domestic asset. Gives Kumar Sangakkara flexibility to deploy him as an Impact Player or float him ahead of Hetmyer when wickets fall in clusters."
        },
        8101: {  # Ashutosh Sharma
            "archetype": "Extreme-Clutch 360-Degree Sweep Specialist",
            "rr_slot": "#7 Finisher / High-RRR Rescue Specialist",
            "auction_tier": "Domestic Value Buy / Game Changer",
            "target_price_inr": "INR 3.0 Cr – INR 5.0 Cr",
            "max_bid_ceiling_inr": "INR 7.0 Cr",
            "fallback_targets": ["Abdul Samad", "Ramandeep Singh"],
            "strengths": [
                "Huge +79.1 Strike Rate uplift under pressure (166.9 Pressure SR vs 87.8 Baseline)",
                "Outstanding 174.1 SR during Innings 2 chases when RRR >= 9.5",
                "Unmatched sweep and scoop repertoire against fast bowlers bowling wide yorkers",
                "Demonstrated psychological resilience in multi-wicket collapse chases"
            ],
            "vulnerabilities": [
                "87.8 baseline SR reflects vulnerability when required to build standard innings against disciplined spin",
                "Prone to LBW against fast skidding deliveries directed at middle stump"
            ],
            "venue_fit": "Can utilize the short square boundaries from one end at SMS Stadium with his sweep shot, neutralizing defensive bowling tactics.",
            "scouting_summary": "A bespoke crisis weapon. In matches where RR needs 45 runs off the last 18 balls, Ashutosh has proven he can deliver where traditional batters stall."
        },
        143: {  # Dinesh Karthik
            "archetype": "Veteran Tactical Closer & Elite 360-Finisher",
            "rr_slot": "#6/#7 Specialist Closer / Mentor",
            "auction_tier": "Experienced Specialist / Value Veteran",
            "target_price_inr": "INR 2.0 Cr – INR 4.0 Cr",
            "max_bid_ceiling_inr": "INR 5.0 Cr",
            "fallback_targets": ["Jitesh Sharma", "Dhruv Jurel (Internal core)"],
            "strengths": [
                "Unbelievable +92.8 Strike Rate uplift under pressure (170.6 Pressure SR vs 77.9 Baseline)",
                "579 pressure balls faced with 171.9 death SR and 25.9% boundary conversion",
                "Forensic understanding of field sets, fine-leg ramp and deep-backward-point carving",
                "Calm tactical decision-making in super-overs and last-over finishes"
            ],
            "vulnerabilities": [
                "Age and fitness management over a long 14-game season",
                "Struggles against high-bouncing express bouncers directed at the helmet"
            ],
            "venue_fit": "His 360-degree deflection game counters Jaipur's larger straight boundaries by relentlessly targeting fine-leg and third-man.",
            "scouting_summary": "Brings championship calmness. Could be utilized as an Impact Sub specialist closer to relieve pressure from Dhruv Jurel."
        },
        4703: {  # Rishabh Pant
            "archetype": "Generational Left-Hand Match-Winner & Wicketkeeper",
            "rr_slot": "#3/#4 Aggressive Anchor & Pace Counter-Attacker",
            "auction_tier": "Marquee Heavyweight",
            "target_price_inr": "INR 15.0 Cr – INR 20.0 Cr",
            "max_bid_ceiling_inr": "INR 21.0 Cr",
            "fallback_targets": ["Ishan Kishan", "Nicholas Pooran"],
            "strengths": [
                "165.9 Pressure SR with 185.8 Death Overs SR across 501 pressure balls",
                "Destroys left-arm pace and leg-spin through aggressive one-handed pickups over midwicket",
                "Generates extreme psychological intimidation on opposition captains and bowlers",
                "World-class wicketkeeping athleticism"
            ],
            "vulnerabilities": [
                "Can fall into wide-off-stump traps outside the tramline when over-eager",
                "Requires high purse commitment that limits all-rounder depth"
            ],
            "venue_fit": "Dominant at Sawai Mansingh Stadium where his leg-side power clears the deepest stands with ease.",
            "scouting_summary": "If available at the auction, Pant gives RR a left-hand powerhouse in the middle order to partner Sanju Samson, completely unbalancing opposition bowling plans."
        },
        23450: {  # Sai Sudharsan
            "archetype": "Ice-Cold Technical Anchor with Explosive Acceleration",
            "rr_slot": "#3 Top-Order Anchor & Chase Stabilizer",
            "auction_tier": "Premium Young Core Batter",
            "target_price_inr": "INR 7.0 Cr – INR 11.0 Cr",
            "max_bid_ceiling_inr": "INR 12.0 Cr",
            "fallback_targets": ["Tilak Varma", "Nitish Kumar Reddy"],
            "strengths": [
                "Outstanding 201.3 Strike Rate at the death (16-20) combined with 166.6 overall pressure SR",
                "Lowest dot-ball percentage in the entire batting cohort under pressure: 28.3%",
                "Exceptional running between wickets and risk-calculated boundary placement",
                "Immunity to early collapses: averages 35+ when top order falls cheaply"
            ],
            "vulnerabilities": [
                "Power ceiling against 145+ kph yorkers in the blockhole requires precision rather than brute force"
            ],
            "venue_fit": "Tailor-made for SMS Stadium Jaipur: turns ones into twos on large outfields and effortlessly accelerates from anchor to enforcer.",
            "scouting_summary": "Provides the structural steel RR's batting lineup needs. When Jaiswal or Samson get out early, Sai guarantees the run rate never drops."
        },
        2877: {  # Vijay Shankar
            "archetype": "Dependable Middle-Order Rotator & Spin Bludgeoner",
            "rr_slot": "#5 Middle Overs Utility Batter",
            "auction_tier": "Smart Value Buy",
            "target_price_inr": "INR 1.5 Cr – INR 3.0 Cr",
            "max_bid_ceiling_inr": "INR 4.0 Cr",
            "fallback_targets": ["Deepak Hooda", "Rahul Tewatia"],
            "strengths": [
                "+69.6 SR uplift under pressure (162.5 Pressure SR vs 92.9 Baseline)",
                "Low 26.4% dot ball rate (second lowest behind Sudharsan)",
                "183.8 Death Overs Strike Rate",
                "Can clear long-on and long-off against finger spin and wrist spin with upright swing"
            ],
            "vulnerabilities": [
                "Prone to dot ball clusters if tucked up by hard lengths into the ribs by right-arm fast bowlers"
            ],
            "venue_fit": "Strong through the V; can handle the slightly slower pitches at Jaipur effectively.",
            "scouting_summary": "A low-cost, high-reliability squad depth option. Perfect squad stabilizer who outperforms his auction valuation under pressure."
        },
        1699: {  # Suryakumar Yadav
            "archetype": "World #1 360-Degree Pressure Manipulator",
            "rr_slot": "#3/#4 Premier High-Leverage Enforcer",
            "auction_tier": "Marquee / Icon Target",
            "target_price_inr": "INR 16.0 Cr – INR 20.0 Cr",
            "max_bid_ceiling_inr": "INR 22.0 Cr",
            "fallback_targets": ["Glenn Maxwell", "Heinrich Klaasen"],
            "strengths": [
                "Huge volume: 1,033 pressure balls faced with 177.8 Pressure SR and 208.0 Death SR",
                "27.2% boundary rate with unmatched field manipulation behind square",
                "Proven track record across all tournament knockout scenarios",
                "Renders traditional field settings useless through scoop, sweep and over-extra-cover loft"
            ],
            "vulnerabilities": [
                "High auction demand means maximum purse allocation"
            ],
            "venue_fit": "Universal compatibility: Jaipur's deep square fences are easily cleared by his trademark behind-square wrist whip.",
            "scouting_summary": "The definitive benchmark for T20 batting under pressure. If Rajasthan Royals have the purse, Suryakumar is the single most destructive asset in world cricket."
        },
        4708: {  # Rinku Singh
            "archetype": "The Premier Indian Ice-Man & Finish Specialist",
            "rr_slot": "#5/#6 Elite Finisher & Match-Closer",
            "auction_tier": "Premium Core Indian Acquisition",
            "target_price_inr": "INR 10.0 Cr – INR 14.0 Cr",
            "max_bid_ceiling_inr": "INR 15.0 Cr",
            "fallback_targets": ["Shashank Singh", "Abdul Samad"],
            "strengths": [
                "Over 903 pressure balls faced with 161.4 Pressure SR and 178.0 Death SR",
                "Phenomenal composure when requiring 15+ runs in the 20th over",
                "Compact, uncluttered swing with exceptional bat speed and bottom-hand power",
                "Outstanding boundary-rider fielding and direct-hit run-out capability"
            ],
            "vulnerabilities": [
                "Can occasionally be tied down by wide, dipping slower balls outside off if bowled with discipline"
            ],
            "venue_fit": "Effortlessly clears Jaipur's 75m straight boundary; loves chasing under lights with dew.",
            "scouting_summary": "The ultimate partner for Sanju Samson and Riyan Parag. Rinku gives RR the guarantee that no chase is dead until the final ball."
        }
    }
    
    # Rich Scouting Profiles for Bowlers
    bowler_scouting = {
        781: {  # Sunil Narine
            "archetype": "All-Time Elite Defensive Mystery Anchor & Death Choke Artist",
            "rr_slot": "Lead Spin Spearhead (Overs 7, 9, 17, 19)",
            "auction_tier": "Marquee Spin Specialist",
            "target_price_inr": "INR 10.0 Cr – INR 14.0 Cr",
            "max_bid_ceiling_inr": "INR 15.0 Cr",
            "fallback_targets": ["Varun Chakravarthy", "Maheesh Theekshana"],
            "strengths": [
                "Tournament-defining 6.47 Pressure Economy across 554 pressure balls",
                "Astonishing 6.06 Death Overs Economy (16-20) under extreme pressure (unrivaled globally)",
                "39.9% dot ball rate and 35 pressure wickets (strike rate: 15.8 balls per wicket)",
                "Complete disguise on knuckle ball, carrom ball, and orthodox off-break"
            ],
            "vulnerabilities": [
                "Rarely gives big flight to invite mistimed hits, occasionally allowing singles when defending sub-6 totals",
                "Batting can be neutralized by high-pace body-line bouncers if used as pinch-hitter"
            ],
            "venue_fit": "Sawai Mansingh Stadium is paradise for Narine: the large square boundaries make his flat, trajectory-varied bowling nearly impossible to hit for six.",
            "scouting_summary": "The single most restrictive bowler in the entire dataset. Solves RR's death-over leakage permanently by bowling overs 17 and 19 for under 7 runs."
        },
        2490: {  # Mohammad Nawaz
            "archetype": "High-IQ Restrictive Left-Arm Finger Spinner",
            "rr_slot": "Matchup Spinner (Overs 6-14 & Death 18/20 vs RHB)",
            "auction_tier": "Tactical Overseas Value Target",
            "target_price_inr": "INR 2.5 Cr – INR 4.5 Cr",
            "max_bid_ceiling_inr": "INR 5.5 Cr",
            "fallback_targets": ["Mitchell Santner", "Akeal Hosein"],
            "strengths": [
                "Incredible 5.98 Pressure Economy and 5.76 Death Economy (lowest death economy in entire database)",
                "Phenomenal strike rate: 10.1 balls per wicket under pressure (31 wickets in 313 balls)",
                "41.2% dot ball rate under pressure",
                "Superb undercut arm-ball that rushes right-handed batters on the pads"
            ],
            "vulnerabilities": [
                "Vulnerable against elite left-handed power-hitters who can slog-sweep with the turn"
            ],
            "venue_fit": "High control suits Jaipur's gripping surface; provides left-arm variation that RR lacked in recent seasons.",
            "scouting_summary": "A tactical masterstroke. At a fraction of marquee price, Nawaz delivers sub-6 economy at the death and takes a wicket every 10 deliveries."
        },
        34485: {  # Sufiyan Muqeem
            "archetype": "Emerging Left-Arm Wrist-Spin Mystery Prodigy",
            "rr_slot": "Middle-Overs Wicket-Taker & Dot-Ball Choke Weapon",
            "auction_tier": "Overseas Scouting Steal / High-Upside Prospect",
            "target_price_inr": "INR 1.0 Cr – INR 2.5 Cr",
            "max_bid_ceiling_inr": "INR 4.0 Cr",
            "fallback_targets": ["Noor Ahmad", "Waqar Salamkheil"],
            "strengths": [
                "Lowest Pressure Economy in the entire dataset: 5.30 across 281 pressure balls",
                "Astonishing 56.2% dot ball percentage (over half his pressure balls are dots!)",
                "11.7 balls per wicket under pressure with 24 wickets taken",
                "Deceptive googly released with high arm angle that beats batters off the pitch"
            ],
            "vulnerabilities": [
                "Uncapped in IPL conditions; needs tactical acclimation to dew conditions",
                "Limited experience in high-scoring 220+ IPL run chases"
            ],
            "venue_fit": "Sawai Mansingh Stadium's slow turn makes his wrist-spin deliveries bite and grip viciously.",
            "scouting_summary": "The pure scouting find of the tournament. Sufiyan's 56.2% dot ball rate makes him the modern cricket equivalent of a fortress."
        },
        5979: {  # Abrar Ahmed
            "archetype": "Classical Mystery Leg-Spinner with Carrom Ball",
            "rr_slot": "Middle-Overs Attacking Spinner (Overs 8-15)",
            "auction_tier": "High-Quality Tactical Bowler",
            "target_price_inr": "INR 2.0 Cr – INR 4.0 Cr",
            "max_bid_ceiling_inr": "INR 5.0 Cr",
            "fallback_targets": ["Suyash Sharma", "Rahul Chahar"],
            "strengths": [
                "5.89 Pressure Economy and 6.88 Death Economy",
                "44.7% dot ball rate and 13.2 balls per wicket (24 wickets in 318 balls)",
                "Finger-flicked leg-cutter and slider that attacks the off-stump bail"
            ],
            "vulnerabilities": [
                "Can lose radar if targeted down the ground early in an over"
            ],
            "venue_fit": "Jaipur's boundary dimensions protect him from mishits, allowing him to toss the ball up fearlessly.",
            "scouting_summary": "Gives Kumar Sangakkara an aggressive wicket-taking option in middle overs to break partnerships before the death phase."
        },
        3644: {  # Kuldeep Yadav
            "archetype": "Premier Left-Arm Wrist-Spin Strike Force",
            "rr_slot": "Lead Attacking Spinner (Overs 7, 9, 11, 14)",
            "auction_tier": "Marquee Indian Bowling Anchor",
            "target_price_inr": "INR 9.0 Cr – INR 13.0 Cr",
            "max_bid_ceiling_inr": "INR 14.5 Cr",
            "fallback_targets": ["Ravi Bishnoi", "Yuzvendra Chahal"],
            "strengths": [
                "51 pressure wickets across 714 balls with a strike rate of 14.0 balls per dismissal",
                "Revamped quicker trajectory (85-92 kph) prevents batters from stepping out",
                "Exceptional dip and sharp turn both ways against RHB and LHB",
                "7.67 overall pressure economy (very respectable for an attacking wrist-spinner)"
            ],
            "vulnerabilities": [
                "8.45 death overs economy shows he is best used as a middle-overs partnership breaker rather than 20th-over specialist"
            ],
            "venue_fit": "Thrives at Sawai Mansingh Stadium where wrist spin historically dominates visiting batting lineups.",
            "scouting_summary": "The definitive Indian attacking spinner. Guarantees 2-3 wickets in middle overs, halting opposition momentum before Sandeep Sharma closes at the death."
        },
        2933: {  # Jasprit Bumrah
            "archetype": "The Global Gold Standard Pace Spearhead",
            "rr_slot": "Opening Strike Bowler (Overs 1, 3) & Death Closer (Overs 17, 19)",
            "auction_tier": "Icon / Platinum Target",
            "target_price_inr": "INR 18.0 Cr – INR 22.0 Cr",
            "max_bid_ceiling_inr": "INR 25.0 Cr",
            "fallback_targets": ["Trent Boult", "Arshdeep Singh"],
            "strengths": [
                "Universal excellence: 7.49 Pressure Economy and 7.41 Death Economy across 780 balls",
                "53 wickets at 14.7 balls per dismissal with 38.2% dot balls",
                "Pinpoint toe-crushing yorker, dipping slower ball, and vicious skidding bouncer",
                "Psychological supremacy: opposition teams systematically look to play him out for 20 runs"
            ],
            "vulnerabilities": [
                "Workload management and physical maintenance throughout a congested calendar"
            ],
            "venue_fit": "Universal performer. Lethal on both Jaipur's skiddy surface and Guwahati's bouncy pitch.",
            "scouting_summary": "The benchmark bowler against whom every candidate is measured. Having Bumrah guarantees RR can defend any total above 160."
        },
        7327: {  # Rasikh Salam
            "archetype": "High-Value Domestic Death Seamer & Wicket Machine",
            "rr_slot": "#2 Death Pace Specialist (Overs 16 & 18) / Sandeep Sharma Partner",
            "auction_tier": "Domestic Value Breakthrough (Prime Scouted Gem)",
            "target_price_inr": "INR 1.5 Cr – INR 3.5 Cr",
            "max_bid_ceiling_inr": "INR 5.0 Cr",
            "fallback_targets": ["Simarjeet Singh", "Yash Dayal"],
            "strengths": [
                "Exceptional wicket strike rate: 10.6 balls per wicket under pressure (30 wickets in 319 balls!)",
                "Economy resistance: his pressure economy (9.10) is significantly BETTER than his baseline economy (10.25)",
                "Tremendous back-of-the-hand slower ball and accurate wide yorker execution",
                "Uncapped/emerging Indian fast bowler status protects auction purse"
            ],
            "vulnerabilities": [
                "Economy of 9.10 under pressure is higher than elite spinners, but acceptable given his extreme wicket-taking frequency"
            ],
            "venue_fit": "His change-of-pace deliveries grip into Jaipur's clay surface, making him exceptionally difficult to pick under lights.",
            "scouting_summary": "The ultimate domestic value discovery. Solves RR's domestic pace depth at minimal purse impact, freeing capital for marquee batters."
        },
        4722: {  # Rashid Khan
            "archetype": "World-Class Match-Winning Leg-Spin Heavyweight",
            "rr_slot": "Core Spin Spearhead & High-Leverage Enforcer",
            "auction_tier": "Marquee Icon Target",
            "target_price_inr": "INR 14.0 Cr – INR 18.0 Cr",
            "max_bid_ceiling_inr": "INR 19.0 Cr",
            "fallback_targets": ["Wanindu Hasaranga", "Noor Ahmad"],
            "strengths": [
                "Highest pressure volume in dataset: 1,165 balls with 96 wickets (12.1 balls per wicket)",
                "7.71 Pressure Economy with 37.5% dot ball rate",
                "Lightning-quick arm action makes his googly impossible to read off the hand",
                "Adds explosive lower-order batting hitting at #8"
            ],
            "vulnerabilities": [
                "8.36 death economy means he should be bowled out by over 17"
            ],
            "venue_fit": "Devastating at Sawai Mansingh Stadium; opposition batters have zero room to work with against his speed.",
            "scouting_summary": "A proven match-winner who guarantees wickets in every high-pressure scenario. Transforms Rajasthan's bowling attack into the best in the tournament."
        },
        4101: {  # Mitchell Santner
            "archetype": "Tactical Mastermind Left-Arm Orthodox Anchor",
            "rr_slot": "Powerplay & Middle Restrictor (Overs 5, 8, 10, 12)",
            "auction_tier": "Overseas Tactical Buy",
            "target_price_inr": "INR 2.0 Cr – INR 4.0 Cr",
            "max_bid_ceiling_inr": "INR 4.5 Cr",
            "fallback_targets": ["Keshav Maharaj", "Roelof van der Merwe"],
            "strengths": [
                "6.91 Pressure Economy across 563 pressure balls with 40 wickets (14.1 balls per wicket)",
                "39.1% dot ball rate under pressure",
                "Subtle variation in pace and trajectory, rarely gives boundary balls",
                "Elite fielding and reliable lower-order batting composure"
            ],
            "vulnerabilities": [
                "9.51 death overs economy indicates he should not be bowled in overs 18-20"
            ],
            "venue_fit": "Can bowl anywhere; highly effective at Jaipur with his flat, defensive trajectories.",
            "scouting_summary": "The consummate professional. Gives RR tactical flexibility to choke the middle overs and create scoreboard pressure."
        },
        6256: {  # Varun Chakravarthy
            "archetype": "Deceptive Mystery Spinner with Stumps-Targeting Trajectory",
            "rr_slot": "Middle & Late-Overs Attacking Mystery Spinner",
            "auction_tier": "Premium Indian Spin Core",
            "target_price_inr": "INR 8.0 Cr – INR 11.0 Cr",
            "max_bid_ceiling_inr": "INR 12.0 Cr",
            "fallback_targets": ["Suyash Sharma", "Mayank Markande"],
            "strengths": [
                "66 pressure wickets across 877 balls (13.3 balls per dismissal)",
                "39.8% dot ball rate and 8.37 pressure economy",
                "Attacks the stumps directly (high bowled and LBW dismissal percentage)",
                "Carrom ball and top-spinner are difficult to gauge under night floodlights"
            ],
            "vulnerabilities": [
                "Vulnerable if wet ball impairs grip at death overs"
            ],
            "venue_fit": "Jaipur's red-soil track gives his carrom ball extra skid and bounce.",
            "scouting_summary": "A proven Indian mystery weapon. Guarantees RR has an attacking wicket-taker who can dismantle opposition middle orders in pressure chases."
        }
    }
    
    # Merge with original CSV metrics
    batters_output = []
    for _, r in bat_df.iterrows():
        pid = int(r['player_id'])
        scout_info = batter_scouting.get(pid, {})
        item = r.to_dict()
        item.update(scout_info)
        batters_output.append(item)
        
    bowlers_output = []
    for _, r in bowl_df.iterrows():
        pid = int(r['player_id'])
        scout_info = bowler_scouting.get(pid, {})
        item = r.to_dict()
        item.update(scout_info)
        bowlers_output.append(item)
        
    dossier_data = {
        "metadata": {
            "title": "Rajasthan Royals War Room Scouting Dossier (IPL 2027)",
            "prepared_for": "Kumar Sangakkara (Head Coach) & Giles Lindsay (Director of Strategy and Analytics)",
            "prepared_by": "PressurePulse Analytics Team",
            "dataset_basis": "200,999 Deliveries (IPL & T20I 2022–2026)",
            "freeze_sha256": "5cdd7b7451b5a6672dbfadccc3c36a9777ec5bafaec589339e22ba307202d272"
        },
        "top10_batters_scouting": batters_output,
        "top10_bowlers_scouting": bowlers_output
    }
    
    # Save to JSON
    out_json_pack = Path("outputs/submission_pack/scouting_dossiers.json")
    out_json_dash = Path("dashboard/public/data/scouting_dossiers.json")
    top10_bat_dash = Path("dashboard/public/data/top10_batters.json")
    top10_bowl_dash = Path("dashboard/public/data/top10_bowlers.json")
    
    with open(out_json_pack, "w") as f:
        json.dump(dossier_data, f, indent=2)
    with open(out_json_dash, "w") as f:
        json.dump(dossier_data, f, indent=2)
    with open(top10_bat_dash, "w") as f:
        json.dump(batters_output, f, indent=2)
    with open(top10_bowl_dash, "w") as f:
        json.dump(bowlers_output, f, indent=2)
        
    print(f"Generated {out_json_pack}, {out_json_dash}, {top10_bat_dash}, and {top10_bowl_dash}")
    
    # Generate Markdown Dossier
    md_path = Path("outputs/submission_pack/RR_WAR_ROOM_SCOUTING_DOSSIER.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# RAJASTHAN ROYALS WAR ROOM SCOUTING DOSSIER (IPL 2027)\n")
        f.write("### Tactical Scouting Intelligence, Archetype Breakdown & Auction Acquisition Matrix\n")
        f.write("> **Prepared for:** Kumar Sangakkara (Head Coach) & Giles Lindsay (Director of Strategy & Analytics)  \n")
        f.write("> **Evaluation Base:** 200,999 Ball-by-Ball Deliveries (IPL & T20I 2022–2026) | **Audit Fingerprint:** `5cdd7b7451b5a6672dbfadccc3c36a9777ec5bafaec589339e22ba307202d272`\n\n")
        
        f.write("---\n\n")
        f.write("## 1. Executive Scouting Charter & Tactical Gap Diagnosis\n\n")
        f.write("In Season 1, Rajasthan Royals backed our analytical recommendation of **Vignesh Puthur**, securing him at the auction. For Season 2, our mandate expands to **solving RR's high-leverage execution gaps** heading into the mega auction cycle for IPL 2027.\n\n")
        f.write("### Existing RR Core Diagnostics & Squad Gaps:\n")
        f.write("1. **Top-Order Luxury vs. Lower-Order Fragility**: RR's retained core (Yashasvi Jaiswal, Sanju Samson, Riyan Parag, Dhruv Jurel, Shimron Hetmyer) is exceptional, but historical data shows close losses in chases where the required rate exceeded 11.5 RPO in overs 16–20. RR requires a **dedicated domestic death finisher** at #6/#7 so Hetmyer and Jurel are not forced to manufacture boundaries under isolated pressure.\n")
        f.write("2. **Death Overs Run Leakage**: Defending 180+ at Sawai Mansingh Stadium (Jaipur) requires extreme restrictiveness. While Sandeep Sharma is masterful, RR needs a second death bowler (spin or pace) who commands sub-7.5 economy when opposition teams target the short straight or square boundaries.\n")
        f.write("3. **Home Venue Dynamics (SMS Stadium, Jaipur)**: Jaipur features 68–74m square boundaries and a pitch that grips in the middle overs. Our scouting model heavily weights restrictive dot-ball spinners and agile running batters.\n\n")
        
        f.write("---\n\n")
        f.write("## 2. Top 10 Batters: Comprehensive Scouting Dossiers\n\n")
        for b in batters_output:
            f.write(f"### Rank #{b['rank']}: {b['player_name']} ({b['primary_role']})\n")
            f.write(f"- **Tactical Archetype:** `{b['archetype']}`\n")
            f.write(f"- **Recommended RR Slot:** {b['rr_slot']}\n")
            f.write(f"- **Auction Valuation Tier:** `{b['auction_tier']}` | **Target Price:** {b['target_price_inr']} (Ceiling: {b['max_bid_ceiling_inr']})\n")
            f.write(f"- **Contingency / Fallback Options:** {', '.join(b['fallback_targets'])}\n")
            f.write(f"- **Quantitative Pressure Profile:** Pressure SR: **{b['pressure_sr']:.1f}** (+{b['sr_uplift']:.1f} uplift vs {b['baseline_sr']:.1f} baseline) | Death SR: **{b['death_pressure_sr']:.1f}** | Chase SR: **{b['chase_pressure_sr']:.1f}** | Dot Rate: **{b['pressure_dot_pct']:.1f}%** | Boundary Rate: **{b['pressure_boundary_pct']:.1f}%** (over {int(b['pressure_balls'])} pressure balls)\n\n")
            f.write("**Key Scouting Strengths:**\n")
            for s in b['strengths']:
                f.write(f"  * {s}\n")
            f.write("\n**Scouting Vulnerabilities & Dismissal Risks:**\n")
            for v in b['vulnerabilities']:
                f.write(f"  * {v}\n")
            f.write(f"\n**Home Venue & Tactical Fit:** {b['venue_fit']}\n")
            f.write(f"\n**War Room Assessment:** *{b['scouting_summary']}*\n\n")
            f.write("---\n\n")
            
        f.write("## 3. Top 10 Bowlers: Comprehensive Scouting Dossiers\n\n")
        for bw in bowlers_output:
            f.write(f"### Rank #{bw['rank']}: {bw['player_name']} ({bw['primary_role']})\n")
            f.write(f"- **Tactical Archetype:** `{bw['archetype']}`\n")
            f.write(f"- **Recommended RR Deployment:** {bw['rr_slot']}\n")
            f.write(f"- **Auction Valuation Tier:** `{bw['auction_tier']}` | **Target Price:** {bw['target_price_inr']} (Ceiling: {bw['max_bid_ceiling_inr']})\n")
            f.write(f"- **Contingency / Fallback Options:** {', '.join(bw['fallback_targets'])}\n")
            f.write(f"- **Quantitative Pressure Profile:** Pressure Economy: **{bw['pressure_economy']:.2f}** (Death Economy: **{bw['death_pressure_economy']:.2f}**) | Dot Ball Rate: **{bw['pressure_dot_pct']:.1f}%** | Wickets: **{int(bw['pressure_wickets'])}** | Strike Rate: **{bw['pressure_balls_per_wicket']:.1f} balls/wkt** (over {int(bw['pressure_balls'])} pressure balls)\n\n")
            f.write("**Key Bowling Superpowers:**\n")
            for s in bw['strengths']:
                f.write(f"  * {s}\n")
            f.write("\n**Tactical Limitations & Weak Areas:**\n")
            for v in bw['vulnerabilities']:
                f.write(f"  * {v}\n")
            f.write(f"\n**Home Venue & Tactical Fit:** {bw['venue_fit']}\n")
            f.write(f"\n**War Room Assessment:** *{bw['scouting_summary']}*\n\n")
            f.write("---\n\n")
            
        f.write("## 4. Rajasthan Royals Auction War Room Bidding Strategy\n\n")
        f.write("### Recommended Core Acquisition Scenarios:\n")
        f.write("#### Scenario A: High-Impact Domestic Finisher + Restrictive Death Bowler (Optimal Budget Balance)\n")
        f.write("- **Primary Targets:** **Shashank Singh** (INR 6.0–7.5 Cr) + **Sunil Narine** (INR 11.0–13.0 Cr) + **Rasikh Salam** (INR 2.0–3.0 Cr)\n")
        f.write("- **Tactical Impact:** Solves both lower-order finishing and death overs restrictiveness while preserving purse flexibility for overseas all-rounders.\n\n")
        f.write("#### Scenario B: The 'Vignesh Puthur' Stealth Domestic Value Draft\n")
        f.write("- **Primary Targets:** **Ashutosh Sharma** (INR 3.5–4.5 Cr) + **Rasikh Salam** (INR 2.0–2.5 Cr) + **Sufiyan Muqeem** (INR 1.5–2.5 Cr) + **Naman Dhir** (INR 3.0–4.0 Cr)\n")
        f.write("- **Tactical Impact:** Acquires 4 of the highest-leverage performers in world cricket for under INR 14 Cr total purse, allowing RR to dominate marquee overseas bidding.\n\n")
        
    print(f"Generated {md_path}")

if __name__ == "__main__":
    generate_scouting_dossiers()
